from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# This call to setup() does all the work
setup(
    name="rest-aiohttp",
    version="1.0.1",
    description="Making async HTTP REST request via aiohttp with JSON, YAML serialization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mortilele/rest-aiohttp",
    author="Alik Akhmetov",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Minimum version requirement of the package
    packages=["restaiohttp"],
    include_package_data=True,
    install_requires=["aiohttp"]
)