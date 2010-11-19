import sys

from setuptools import setup

meta = dict(
    name="statzlogger",
    version="0.1.0",
    description="statzlogger logs statz",
    author="Will Maier",
    author_email="willmaier@ml1.net",
    py_modules=["statzlogger"],
    test_suite="tests",
    install_requires=["setuptools"],
    keywords="logging statistics sawzall szl",
    url="http://packages.python.org/statzlogger",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: System :: Logging",
    ],
)

# Automatic conversion for Python 3 requires distribute.
if False and sys.version_info >= (3,):
    meta.update(dict(
        use_2to3=True,
    ))

setup(**meta)
