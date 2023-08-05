from __future__ import print_function

import sys
from setuptools import setup
from setuptools.command.build_py import build_py


with open('README.md') as f:
    long_description = ''.join(f.readlines())


class NoBuild(build_py):
    """Raise an exception instead of building this package."""
    def run(self):
        print('-' * 42, file=sys.stderr)
        print(long_description, file=sys.stderr)
        print('-' * 42, file=sys.stderr)
        raise ValueError(
            'You probably want to install the package from private repository.'
        )

setup(
    name="SygicMapsSDK",
    version="0.0.1",
    description="Placeholder package - Python Bindings for Sygic Maps SDK",
    author="Sygic a. s.",
    author_email="info@sygic.com",
    url="https://www.sygic.com/enterprise/maps-navigation-sdk-developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Commercial",
    py_modules=['nonexisting'],
    cmdclass={'build_py': NoBuild},
    zip_safe=False
)
