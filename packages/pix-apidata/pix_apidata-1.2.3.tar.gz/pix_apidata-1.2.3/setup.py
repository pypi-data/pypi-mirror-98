import pathlib
from setuptools import setup ,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pix_apidata",
    version="1.2.3",
    description="Python library to connect and stream the market data.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pscoumar",
    author="Coumar Pandourangane",
    author_email="pscoumar@gmail.com",
    license="MIT",
    classifiers=[ 
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    keywords = 'Market',
    packages=['pix_apidata'],
    include_package_data=True,
    install_requires=['signalrcore-async', 'urllib3'],

)