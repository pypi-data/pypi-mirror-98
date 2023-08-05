import os
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    __version__ = os.environ["GITHUB_REF"].split("/")[-1]
    print(f"Version: {__version__}")
except KeyError:
    from fitfeats.version import __version__

setup(
    name="fitfeatures",
    version=__version__,
    description="Python Feature Selection & Optimization library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diogomatoschaves/fitfeatures",
    author="Diogo Matos Chaves",
    author_email="di.matoschaves@gmail.com",
    packages=[*find_packages(), "fitfeats.utils"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=["numpy", "matplotlib", "scipy", "geneal", "scikit-learn", "pandas"],
    test_requires=["pytest", "pytest-cov", "pytest-mock"],
    keywords=["feature selection", "feature optimization", "machine learning",
              "genetic algorithms", "optimization"],
)