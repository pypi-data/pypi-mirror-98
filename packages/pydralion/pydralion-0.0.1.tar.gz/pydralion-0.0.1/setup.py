import os
import codecs
from setuptools import setup

setup(
    name="pydralion",
    version="0.0.1",
    author="zhaokai5520",
    author_email="zhaokai5520@foxmail.com",
    description="this is a pydralion utils package",
    long_description=codecs.open(os.path.join(os.path.dirname(__file__), 'README'), 'r', 'utf-8-sig').read(),
    license="MIT",
    url="http://iop.sf-express.com/auth",
    packages=['pydralion'],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6"
    ]
)
