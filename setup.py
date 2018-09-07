import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


with open("LICENSE", "r") as fh:
    license = fh.read()

setuptools.setup(
    name="h5nastran",
    version="0.0.1",
    author="Emanuele Cannizzaro",
    author_email="emanuele.cannizzaro@gmail.com",
    description="A HDF5 tool for Finite Element Analysis Results",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EmanueleCannizzaro/h5nastran",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
