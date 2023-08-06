import os
from codecs import open
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

os.chdir(here)

version_contents = {}
with open(os.path.join(here, "clearmacro", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version_contents)

setup(
    name="cmqd",
    version=version_contents["VERSION"],
    url="https://github.com/cmqd/cm-api-python-sdk",
    license="MIT",
    keywords="cmqd clearmacro python api sdk",
    author="ClearMacro",
    author_email="support@clearmacro.com",
    description="Python bindings for the ClearMacro API",
    packages=find_packages(exclude=["tests", "tests.*"]),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        'requests >= 2.20; python_version >= "3.0"',
        'requests[security] >= 2.20; python_version < "3.0"',
        'pandas >= 1.1.3; python_version >= "3.0"',
        'pyjwt >= 1.7.1; python_version> "3.0"',
    ],
    project_urls={
        "Bug Tracker": "https://github.com/cmqd/cm-api-python-sdk/issues",
        "Documentation": "https://github.com/cmqd/cm-api-python-sdk",
        "Source Code": "https://github.com/cmqd/cm-api-python-sdk",
    },
    zip_safe=False,
)
