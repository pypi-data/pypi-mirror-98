import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cfcompare", # Replace with your own username
    version="1.2.0",
    author="Harry Singh",
    author_email="hsing247@uwo.ca",
    description="Tool to compare CF Standard Name versions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/HarrySng/cfsntool/archive/v1.0.0.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
