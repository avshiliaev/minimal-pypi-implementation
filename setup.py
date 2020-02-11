import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding="utf8")

setup(
    name="pystatmath",
    version="0.0.1",
    description="Our awesome package",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["numpy"],
)
