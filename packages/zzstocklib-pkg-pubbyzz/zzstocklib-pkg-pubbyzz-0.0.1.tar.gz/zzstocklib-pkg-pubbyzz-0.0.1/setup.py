import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zzstocklib-pkg-pubbyzz",
    version="0.0.1",
    author="pubbyzz",
    author_email="pubbyzz@hotmail.com",
    description="A Stock Analysis Lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pubbyzz/zzstocklib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)