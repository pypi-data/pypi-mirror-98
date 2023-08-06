from setuptools import setup, find_namespace_packages


def get_version():
    import os.path

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'src/momotor/rpc/version.py'), 'r') as version_file:
        loc = {}
        exec(version_file.readline(), {}, loc)
        return loc['__VERSION__']


def get_long_description():
    with open("README.md", "r") as fh:
        return fh.read()


setup(
    name='momotor-engine-proto',
    version=get_version(),
    author='Erik Scheffers',
    author_email='e.t.j.scheffers@tue.nl',
    description="Momotor Engine Protocol Library",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url='https://momotor.org/',
    project_urls={
        'Documentation': 'https://momotor.org/doc/engine/momotor-engine-proto/',
        'Source': 'https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/',
        'Tracker': 'https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/issues',
    },
    install_requires=[
        'momotor-engine-shared~=1.0',
        'asyncio_extras',
        'protobuf~=3.15.6',
        'h2~=4.0',
        'grpclib~=0.4.0',
        'py-multihash',
        'base58<2.0',
        'backoff',
        'multidict',
    ],
    python_requires='>=3.7',
    extras_require={
        # 'blake2': ['pyblake2'],
        'tools': [
            'grpcio-tools~=1.36.1',
        ],
        'test': [
            'pytest',
            'pytest-cov',
            'pytest-pythonpath',
        ],
        'docs': [
            'Sphinx',
            'sphinx-autodoc-typehints',
        ],
    },
    packages=find_namespace_packages(where='src', include=('momotor.*',)),
    package_dir={'': 'src'},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    ],
)
