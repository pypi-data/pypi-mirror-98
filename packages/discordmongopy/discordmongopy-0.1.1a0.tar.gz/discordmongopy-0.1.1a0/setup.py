import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="discordmongopy",
    version="0.1.1a0",
    description="A mongodb api wrapper to use in your discord bot",
    long_description=README,
    long_description_content_type="text/markdown",
    author="BongoPlayzYT",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["discordmongo"],
    include_package_data=True,
    install_requires=["pymongo"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
