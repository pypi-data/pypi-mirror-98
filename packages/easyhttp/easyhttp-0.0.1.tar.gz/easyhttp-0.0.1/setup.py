from setuptools import setup, find_packages
import codecs
import os

"""
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
"""

VERSION = '0.0.1'
DESCRIPTION = 'Basic HTTP server package'
LONG_DESCRIPTION = 'A simple HTTP server made for study purposes.'

# Setting up
setup(
    name="easyhttp",
    version=VERSION,
    author="luisbrandino (Luis Brandino)",
    author_email="<luisbrandino.contato@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'webserver', 'http', 'http server', 'sockets'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)