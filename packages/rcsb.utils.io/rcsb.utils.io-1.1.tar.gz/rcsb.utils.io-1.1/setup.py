# File: setup.py
# Date: 6-Mar-2019
#
# Update:
#
#
import re

from setuptools import find_packages
from setuptools import setup

packages = []
thisPackage = "rcsb.utils.io"

with open("rcsb/utils/io/__init__.py", "r") as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

setup(
    name=thisPackage,
    version=version,
    description="RCSB Python I/O Utility Classes",
    long_description="See:  README.md",
    author="John Westbrook",
    author_email="john.westbrook@rcsb.org",
    url="https://github.com/rcsb/py-rcsb_utils_io",
    #
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        # 'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={"console_scripts": []},
    #
    install_requires=[
        'numpy >= 1.18.0; sys_platform == "darwin" and python_version > "3.0"',
        'numpy == 1.16.6; sys_platform == "darwin" and python_version < "3.0"',
        "numpy; sys_platform !='darwin'",
        "pytz",
        "python-dateutil",
        "mmcif >= 0.61",
        "ruamel.yaml",
        "requests >= 2.25.0",
        "rcsb.utils.validation >= 0.20",
        "PyNaCl >= 1.3.0",
        'backports.tempfile; python_version < "3.0"',
        "paramiko >=2.7.2",
        "psutil >= 5.7.2",
    ],
    packages=find_packages(exclude=["rcsb.mock-data", "rcsb.utils.tests-io", "rcsb.utils.tests-*", "tests.*"]),
    package_data={
        # If any package contains *.md or *.rst ...  files, include them:
        "": ["*.md", "*.rst", "*.txt", "*.cfg"]
    },
    #
    # These basic tests require no database services -
    test_suite="rcsb.utils.tests-io",
    tests_require=["tox"],
    #
    # Not configured ...
    extras_require={"dev": ["check-manifest"], "test": ["coverage"]},
    # Added for
    command_options={"build_sphinx": {"project": ("setup.py", thisPackage), "version": ("setup.py", version), "release": ("setup.py", version)}},
    # This setting for namespace package support -
    zip_safe=False,
)
