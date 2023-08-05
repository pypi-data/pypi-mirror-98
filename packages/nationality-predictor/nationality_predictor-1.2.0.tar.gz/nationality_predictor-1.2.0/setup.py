from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
    name = "nationality_predictor",
    version = "1.2.0",
    license = "MIT",
    url = "https://github.com/dewittethomas/nationality-predictor",
    
    description = "An engine that predicts the nationality of a person's name",
    long_description = long_description,
    long_description_content_type = "text/markdown",

    package_dir = {"nationality_predictor": "nationality_predictor"},
    install_requires = [
        "requests>=2.22.0", 
        "pycountry>=19.8.18"
    ],

    packages = find_packages(),

    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],

    keywords = "name nationality API person predict predictor"
)