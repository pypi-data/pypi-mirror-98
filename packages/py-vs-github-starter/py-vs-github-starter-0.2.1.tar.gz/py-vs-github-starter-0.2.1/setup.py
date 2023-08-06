import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="py-vs-github-starter",
    version="0.2.1",
    description="Starter python library project for VSCode AND Github with built-in features;",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/leogiciel/py-starter",
    author="Brice Andreota",
    author_email="brice@andreota.fr",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude="tests"),
    include_package_data=True,
    install_requires=["wheel", "bumpversion", "black", "isort", "mypy"],
    entry_points={"console_scripts": []},
)
