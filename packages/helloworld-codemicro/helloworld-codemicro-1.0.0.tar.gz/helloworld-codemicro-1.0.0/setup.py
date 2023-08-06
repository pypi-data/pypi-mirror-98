import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="helloworld-codemicro",
    version="1.0.0",
    author="Thomas Pain",
    author_email="tom@tdpain.net",
    description="A testing package to be uploaded to PyPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.github.com/codemicro/helloworld-python",
    packages=["helloworld"],
    python_requires=">=3.5",
    install_requires=[],
)