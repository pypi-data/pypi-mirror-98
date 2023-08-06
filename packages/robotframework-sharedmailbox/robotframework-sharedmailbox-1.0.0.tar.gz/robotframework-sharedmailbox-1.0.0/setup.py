import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="robotframework-sharedmailbox",
    version="1.0.0",
    description="Read shared mailboxes in Exchange 365 using Robot Framework.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/arvindmehairjan/robotframework-sharedmailbox",
    author="Arvind Mehairjan",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["SharedMailbox"],
    include_package_data=True,
    install_requires=["exchangelib"]
)