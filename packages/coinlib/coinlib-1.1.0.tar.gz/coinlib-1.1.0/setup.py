"""Setup script for coinlib"""
import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README_pip.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="coinlib",
    version="1.1.0",
    description="Develop new code for your coindeck environment",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/coindeck/coinlib",
    author="coindeck",
    author_email="donnercody86@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],

    packages=["coinlib"],
    include_package_data=True,
    install_requires=[
        "requests", "semver", "coolname", "google", "grpcio", "grpcio-tools", "protobuf", "cython", "ipython", "ipykernel", "pandas", "websocket-client", "plotly", "simplejson", "ipynb_path",
        "matplotlib", "pyarrow", "pandas", "python-dateutil", "chipmunkdb_python_client"
    ],
    entry_points={"console_scripts": ["coinlib=index:main"]},
)
