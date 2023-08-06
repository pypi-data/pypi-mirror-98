import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="my_package_chetan",
    version="1.0.0",
    description="Read the latest my_package.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/chetanghadawaje/my_package.git",
    author="Chetan Ghadawaje",
    author_email="chetanghadawaje@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["my_package"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "my_package=__main__:main",
        ]
    },
)
