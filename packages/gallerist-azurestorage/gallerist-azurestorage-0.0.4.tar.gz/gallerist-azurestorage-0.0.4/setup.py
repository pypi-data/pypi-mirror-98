from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="gallerist-azurestorage",
    version="0.0.4",
    description="Azure Storage file store for Gallerist",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Neoteroi/Gallerist-AzureStorage",
    author="RobertoPrevato",
    author_email="roberto.prevato@gmail.com",
    keywords="pictures images web azure storage",
    license="MIT",
    packages=["galleristazurestorage"],
    install_requires=["gallerist==0.0.5", "azure-storage-blob==12.7.1"],
    include_package_data=True,
    zip_safe=False,
)
