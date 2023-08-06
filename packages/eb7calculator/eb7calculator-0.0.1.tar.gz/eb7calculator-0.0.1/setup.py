import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="eb7calculator",
    version="0.0.1",
    description="A simple calculator",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/birnesh/eb7calculator",
    author="Birnesh Eswaramoorthy",
    author_email="birnesh1996@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'calc', 'calculator', 'cal', 'simple', 'basic'],
    )
