import pathlib
from setuptools import setup

# directory containing this file
HERE = pathlib.Path(__file__).parent

# text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="Moberg-Analytics-HDF5",
    version="1.0.1",
    description="Moberg Analytics HDF5 Functions",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Moberg-Analytics-Inc/Moberg-Analytics-HDF5",
    author="Moberg Analytics",
    author_email="zack.goldblum@moberganalytics.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["moberg_analytics_hdf5"],
    include_package_data=True,
    install_requires=["h5py", "numpy", "pandas"]
)