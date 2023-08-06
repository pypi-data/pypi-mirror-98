import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="dominus-python-sdk",
    version="0.22.0",
    url="https://github.com/openaristos/dominus-python-sdk",
    license='AGPLv3',
    author="Aristos Data, LLC.",
    author_email="hello@openaristos.io",
    description="A Python Client for Dominus",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=('tests',)),
    install_requires=requirements,
    keywords=['open aristos'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Telecommunications Industry',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
