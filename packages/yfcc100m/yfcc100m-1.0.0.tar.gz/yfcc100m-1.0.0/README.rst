YFCC100m
========

What is the YFCC100m dataset? A quote from its website_:

.. _website: https://multimediacommons.wordpress.com/yfcc100m-core-dataset/

    The YFCC100M is the largest publicly and freely useable
    multimedia collection, containing  the metadata of around
    99.2 million photos and 0.8 million videos from Flickr,
    all of which were shared under one of the various
    Creative Commons licenses.


Metadata and files are currently hosted in a public `AWS bucket`__,
but downloading and using them is a painful experience.
Handling 100 Million small files is a terrible idea.
Ask me how I know.
This package aims to make downloading and accessing this
dataset straight-forward.
Once finished metadata and files are stored in 4096 neat shards
from ``000`` to ``fff`` following the structure of the bucket.

.. _bucket: https://registry.opendata.aws/multimedia-commons
__ bucket_



AWS account required
--------------------

Unfortunately AWS credentials are required to download files.
A credit card is required to create the account,
but it will not be charged for the download.
Follow `these steps`__ to create access key and secret.
You can ``pip install awscli`` and run ``aws configure``
or create these files manually::

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


.. _awscredentials: https://aws.amazon.com/de/blogs/security/wheres-my-secret-access-key/
__ awscredentials_

It's possible to manually download individual files without an account,
but downloading a larger number is not advisable.
Again, ask me how I know.



Steps to download (TL;DR)
-------------------------

Convert metadata::

    python -m yfcc100m.convert_metadata <input dir> -o <meta dir>

Download files::

    python -m yfcc100m.download <meta dir> -o <zip dir>



Steps to download (long version)
--------------------------------

The download is a 2-step process and involves three
directories (with required free space):

- input (61.1 GiB)
- meta (20 GiB)
- zip (images 11 TiB, videos -- TiB)

Note:
    You can use the same storage system and even directory
    for all three, but it's not a good idea.
    Metadata is provided as a single 61.1 GiB SQLite file.
    It is strongly recommended to store this file locally or
    even in a tmpfs as queries are several magnitudes slower on
    a remote filesystem.
    Meta and zip directories can be on slow-ish network storage.

We first need to download and split the metadata into shards.
This is done with the first command::

    python -m yfcc100m.convert_metadata <input dir> -o <meta dir>

This will look for ``yfcc100m_dataset.sql`` in the input directory
and download it if necessary.
If this file is found it will be verified
(can be skipped, consult the help text for more info)
and converted into 4096 shards ``000.gz`` to ``fff.gz``.
This process can take a few hours.

Next, the actual download.
By default this download images only::

    python -m yfcc100m.download <meta dir> -o <zip dir>

Each metadata shard is downloaded separately and stored directly
as an uncompress ZIP file, i.e., ``000.zip`` to ``fff.zip``.
This will obviously take a while, but the download can be
as slow or fast as you want it to be.
Depending on the number of parallel processes and threads it
can take anywhere from hours to weeks.



Convert to datadings format
---------------------------

This step is optional. You can convert the ZIP file shards into
the very fast and efficient datadings_ format. It packs files
along with metadata into one convenient file::

    python -m yfcc100m.convert <zip dir> -m <meta dir> -o <output dir>

This tool verifies that images decode without errors and show
useful content (brightness varies significantly for at least 5%
of all lines). Images that fail these basic tests are excluded.
It will also attempt to re-compress images that contained errors.

Compression can optionally be applied to all images. Combined
with verification, compressing with quality 85 reduces the size
of all the image part of the dataset by over 60%, from 11 to
only 4.2 TiB. This is almost indistinguishable to humans and
does not affect the performance of neural networks trained on
such images.

.. _datadings: https://datadings.readthedocs.io



Filtering
---------

You can filter the dataset before downloading based on metadata
using the filter option with a lambda function.
E.g., to download only files with "holiday" in the user tags::

     --filter 'lambda x: "holiday" in x["usertags"]'

