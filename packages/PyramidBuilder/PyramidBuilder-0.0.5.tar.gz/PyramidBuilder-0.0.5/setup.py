import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="PyramidBuilder",
    version="0.0.5",
    description="Auto compiles HTML, CSS and JS into one file Pyramid App.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ankitkumar-13/PyramidBuilder",
    author="Ankit Kumar",
    author_email="ankitkumar13122003@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["PyramidBuilder"],
    include_package_data=True,
    install_requires=["PySimpleGUI", "beautifulsoup4"],
)