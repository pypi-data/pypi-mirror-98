import os
import glob
from subprocess import check_output
from subprocess import CalledProcessError
from setuptools import setup, find_packages

setup_path = os.path.dirname(__file__)


def read(fname):
    return open(os.path.join(setup_path, fname), encoding="utf8").read()


REPO_URL = "https://github.com/biothings/biothings.api"


# get version
version = __import__('biothings').get_version()

# should fail if installed from source or from pypi,
# version gets set to MAJOR.MINOR.# commits on master branch if installed from pip repo
# otherwise to MAJOR.MINOR.MICRO as defined in biothings.version
try:
    num_commits = check_output("git rev-list --count master", shell=True).strip().decode('utf-8')
except CalledProcessError:
    num_commits = ''

# Calculate commit hash, should fail if installed from source or from pypi
try:
    commit_hash = check_output("git rev-parse HEAD", shell=True).strip().decode('utf-8')
except CalledProcessError:
    commit_hash = ''

# Write commit to file inside package, that can be read later
if commit_hash or num_commits:
    with open('biothings/.git-info', 'w') as git_file:
        git_file.write("{}.git\n{}\n{}".format(REPO_URL, commit_hash, num_commits))


# very minimal requirement for running biothings.web
install_requires = [
    'requests>=2.21.0',
    'tornado==5.1.1',
    'gitpython>=3.1.0',
    'elasticsearch>=6, <8',
    'elasticsearch-dsl>=6, <8',
    'elasticsearch-async>=6.2.0',
    'singledispatchmethod; python_version < "3.8.0"',
    'aiohttp==3.6.2',    # for compatibility with elasticsearch-async==6.x
    'PyYAML>=5.1',
]

# extra requirements for biothings.web
web_extra_requires = [
    'msgpack>=0.6.1',   # support format=msgpack
]

# extra requirements to run biothings.hub
hub_requires = [
    'beautifulsoup4',   # used in dumper.GoogleDriveDumper
    'aiocron',          # setup scheduled jobs
    'aiohttp==3.6.2',   # for compatibility with elasticsearch-async==6.x
    'asyncssh==1.7.1',  # needs libffi-dev installed (apt-get)
    'pymongo',
    'psutil',
    'jsonpointer',      # for utils.jsonpatch
    'IPython',          # for interactive hub console
    'boto',
    'boto3',
    'multiprocessing_on_dill',  # can replace pickler in concurrent.futures
    'dill',             # a pickle alternative with extra object type support
    'pyinotify',        # hub reloader
    'prettytable',      # diff report renderer
    'sockjs-tornado==1.0.6',   # websocket server for HubServer
    'jsonschema>=2.6.0',
    'pip',              # auto-install requirements from plugins
    'pandas==1.0.1',    # json with inf/nan and more to come
    'yapf',             # code reformatter, better results than autopep8
    'requests-aws4auth',    # aws s3 auth requests for autohub
    'networkx>=2.1',            # datatransform
    'biothings_client==0.2.1'   # datatransform (api client)
]

# extra requirements for building docs
docs_requires = [
    'sphinx>=2.4.3',
    'sphinx_rtd_theme>=0.4.3'
]

# extra requirements for nosetests
test_requires = [
    "nose>=1.3.7",
    "pytest"
]

setup(
    name="biothings",
    version=version,
    author="Cyrus Afrasiabi, Sebastien Lelong, Xinghua Zhou, Chunlei Wu",
    author_email="cwu@scripps.edu",
    description="a toolkit for building high-performance data APIs in biology",
    license="Apache License, Version 2.0",
    keywords="biology annotation web service client api",
    url=REPO_URL,
    packages=find_packages(),
    package_data={'': ['*.html']},
    include_package_data=True,
    scripts=list(glob.glob('biothings/bin/*')),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    install_requires=install_requires,
    extras_require={
        'web_extra': web_extra_requires,
        'hub': hub_requires + test_requires,
        'dev': web_extra_requires + hub_requires + docs_requires + test_requires
    },
)
