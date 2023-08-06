import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="tintin-sdk",
    version="0.0.2",
    description="A Python SDK for Tintin",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/footprint-ai/tintin-sdk",
    author="hsinho yeh",
    author_email="hsinho.yeh@footprint-ai.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    package_data={'tintin': ['*.txt']},
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "tintin-sdk=tintin.__main__:main",
        ]
    },
)
