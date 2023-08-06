import re
from pathlib import Path

from setuptools import setup
from setuptools import find_packages


ROOT_DIR = Path(__file__).parent


def read(*names):
    with ROOT_DIR.joinpath(*names).open(encoding='utf8') as f:
        return f.read()


# pip's single-source version method as described here:
# https://python-packaging-user-guide.readthedocs.io/single_source_version/
def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


dependencies = read(ROOT_DIR, 'requirements.txt').splitlines()


setup(
    name='yfcc100m',
    version=find_version('yfcc100m', '__init__.py'),
    author='Joachim Folz',
    author_email='joachim.folz@dfki.de',
    license='MIT',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    description='Download the YFCC100m dataset without going insane.',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst; charset=UTF-8',
    keywords='yfcc100m yfcc yahoo flickr creative commons '
             '100 million dataset data set download',
    packages=find_packages(
        include=['yfcc100m', 'yfcc100m.*'],
    ),
    install_requires=dependencies,
    zip_safe=False,
    project_urls={
        'Documentation': 'https://gitlab.com/jfolz/yfcc100m/blob/master/README.rst',
        'Source': 'https://gitlab.com/jfolz/yfcc100m',
        'Tracker': 'https://gitlab.com/jfolz/yfcc100m/issues',
    },
)
