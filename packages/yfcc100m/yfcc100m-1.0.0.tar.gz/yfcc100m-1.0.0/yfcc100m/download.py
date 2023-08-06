"""
Download the YFCC100m dataset from AWS. Requires the metadata files produced by
the convert_metadata tool as input. Files are stored in 4096 ZIP-files. For
images shards are ~27000 files each and occupy 11 TiB. The download can be
stopped at any time and will ignore fully downloaded shards when resumed.

WARNING:

IMPORTANT: Needs AWS credentials to work. Create an AWS account (credit card
           required, but will not be charged). You can install aws-cli and run
           aws configure or create these files manually:

           ~/.aws/config
           [default]
           region = us-west-2
           s3 =
               max_concurrent_requests = 100
               max_queue_size = 10000
               max_bandwidth = 50MB/s
               multipart_threshold = 64MB
               multipart_chunksize = 16MB
               use_accelerate_endpoint = false

           ~/.aws/credentials
           [default]
           aws_access_key_id = <key>
           aws_secret_access_key = <secret>
"""
import io
import zipfile
from pathlib import Path
import threading as th
from multiprocessing.pool import ThreadPool

from tqdm import tqdm
import boto3
from botocore.exceptions import ClientError
from datadings.tools.cached_property import cached_property

from .vars import BUCKET_NAME
from .tools import find_meta_shards
from .tools import get_possible_keys
from .tools import WorkerBase
from .tools import load_finished_shards
from .tools import shard_finished


class Downloader(WorkerBase):
    @cached_property
    def bucket(self):
        loc = th.local()
        if not hasattr(loc, 'bucket'):
            loc.session = boto3.Session()
            loc.bucket = loc.session.resource('s3').Bucket(BUCKET_NAME)
        return loc.bucket

    def file_exists(self, sample):
        for _, key in get_possible_keys(sample):
            try:
                self.bucket.Object(key).load()
                return True
            except ClientError:
                pass
        return False

    def download_file(self, sample):
        for canonical_key, key in get_possible_keys(sample):
            try:
                bio = io.BytesIO()
                self.bucket.download_fileobj(key, bio)
                return key, bio.getvalue()
            except ClientError:
                pass
        else:
            # noinspection PyUnboundLocalVariable
            return canonical_key, None

    def download_files(self, shard, files):
        pool = ThreadPool(self.threads)
        with self.position() as position:
            yield from self.tqdm(
                pool.imap(self.download_file, files),
                shard,
                position,
                length=len(files),
            )

    def download_shard(self, shard):
        metadata = self.prepare_metadata(shard)
        errpath = self.outdir / (shard + '.err')
        with zipfile.ZipFile(self.outdir / (shard + '.zip'), 'w') as z:
            for key, data in self.download_files(shard, metadata):
                if data:
                    z.writestr(key, data)
                else:
                    with errpath.open('at', encoding='utf-8') as err:
                        err.write(key+'\n')
        return shard

    def download_shards(self):
        with self.positioned(), self.pool() as pool:
            yield from pool.imap_unordered(self.download_shard, self.shards)

    def find_missing(self, shard, metadata, existing_keys):
        missing = []
        # for each sample, check if any of the possible keys is in the shard
        # if not, check if file exists on AWS and add to list of missing samples
        with self.position() as position:
            for sample in self.tqdm(metadata, shard, position):
                for _, key in get_possible_keys(sample):
                    if key in existing_keys:
                        break
                else:
                    if self.file_exists(sample):
                        missing.append(sample)
        return missing

    def check_shard(self, shard):
        shardpath = self.outdir / (shard + '.zip')
        if not shardpath.exists():
            return shard
        # get named of all files in shard
        with zipfile.ZipFile(shardpath, 'r') as z:
            existing_keys = set(z.namelist())
        metadata = self.prepare_metadata(shard)
        missing = self.find_missing(shard, metadata, existing_keys)
        if missing:
            shardpath = self.outdir / (shard + '_missing.zip')
            with zipfile.ZipFile(shardpath, 'w') as z:
                for key, data in self.download_files(shard, missing):
                    if data:
                        z.writestr(key, data)
        return shard

    def check_shards(self):
        with self.positioned(), self.pool() as pool:
            yield from pool.imap_unordered(self.check_shard, self.shards)


def download_parallel(
        indir,
        outdir,
        shards=None,
        kinds=(0, 1),
        filter_code='lambda x: True',
        processes=8,
        threads=8,
        overwrite=False,
        check=False,
):
    if not shards:
        shards = find_meta_shards(indir)
        finished_shards = load_finished_shards(outdir)
        if check:
            shards = finished_shards
        elif not overwrite:
            shards -= finished_shards
        shards = sorted(shards)

    downloader = Downloader(
        shards, indir, indir, outdir, kinds, filter_code, processes, threads
    )
    gen = tqdm(
        downloader.check_shards() if check else downloader.download_shards(),
        desc='total',
        total=len(shards),
        smoothing=0,
        position=0,
    )
    for shard in gen:
        if not check:
            shard_finished(shard, outdir)


def main():
    from datadings.tools.argparse import make_parser

    parser = make_parser(
        __doc__,
        no_confirm=False,
        skip_verification=False,
        shuffle=False,
    )
    parser.add_argument(
        '-p', '--processes',
        default=8,
        type=int,
        help='Number of shards downloaded in parallel.'
    )
    parser.add_argument(
        '-t', '--threads',
        default=8,
        type=int,
        help='Number of threads to download each shard.'
    )

    def _kind(v):
        return {'images': 0, 'videos': 1}[v]

    # noinspection PyTypeChecker
    parser.add_argument(
        '--kind',
        nargs='+',
        type=_kind,
        choices=('images', 'videos'),
        default=(0,),
        help='Kinds of files to download. Defaults to images.'
    )
    parser.add_argument(
        '--shard',
        default=(),
        type=str,
        nargs='+',
        help='Specify individual shards to download.'
    )

    def _evalable(v):
        eval(v)
        return v
    parser.add_argument(
        '--filter',
        type=_evalable,
        default='lambda x: True',
        help='Lambda function to select samples.'
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite finished shards.'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check existing shard and attempt to add missing files.'
    )
    args = parser.parse_args()
    indir = Path(args.indir)
    outdir = Path(args.outdir) or args.indir

    try:
        download_parallel(
            indir,
            outdir,
            args.shard,
            args.kind,
            args.filter,
            args.processes,
            args.threads,
            args.overwrite,
            args.check,
        )
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
