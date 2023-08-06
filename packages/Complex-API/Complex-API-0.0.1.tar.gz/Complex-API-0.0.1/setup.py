import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Complex-API",
    version="0.0.1",
    description="It makes it easier to use the API I have built/working on",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JagTheFriend/Complex-API",
    author="JagTheFriend",
    author_email="jagthefriend12@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["Complex_API"],
    include_package_data=True,
    install_requires=[
        "requests",
        "setuptools"
    ],
    entry_points={
        "console_scripts": [
            "Complex_API=Complex_API.complex_api:main",
        ]
    },
)
