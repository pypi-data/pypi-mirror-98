from pathlib import Path
from setuptools import setup

from torch_fit import __version__


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(Path(__file__).parent / 'README.md').read()


def read_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()


settings = dict(
    name='torch-fit',
    packages=['torch_fit'],
    version=__version__,
    author='kaelzhang',
    author_email='',
    description=('`Keras.Model.fit`-like torch fit implementation'),
    license='MIT',
    keywords='torch-fit',
    url='https://github.com/kaelzhang/torch-fit',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('dev-requirements.txt'),
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ]
)


if __name__ == '__main__':
    setup(**settings)
