import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="quickrun",
    version="0.0.8",
    description="Easily run commands and gather info across multiple servers",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/danstewart/quickrun",
    author="Dan Stewart",
    author_email="git@mail.danstewart.dev",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["quickrun", "quickrun/helpers", "quickrun/cli"],
    include_package_data=True,
    install_requires=["rich", "pexpect", "jq"],
)
