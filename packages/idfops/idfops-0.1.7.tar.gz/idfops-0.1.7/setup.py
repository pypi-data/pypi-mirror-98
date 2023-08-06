import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

SRC = 'src'
setuptools.setup(
    name="idfops",
    version="0.1.7",
    author="ira",
    author_email="ira.saktor@gmail.com",
    description="Wrapper around pandas table operations such as union, melting, casting, reading spreadsheets, finding value in dataframe",
    long_description=long_description,
    package_dir={'': SRC},
    long_description_content_type="text/markdown",
    url="https://gitlab.com/i19/pandas_operations",
    #download_url = "https://gitlab.com/i19/pandas_operations/-/archive/0.1.1/pandas_operations-0.1.1.tar.gz",
    packages=setuptools.find_packages(SRC),
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'pandas',
      ],
    python_requires='>=3.6',
)
