import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="pygiftbit",
    version="1.0.3",
    description="A simple Python wrapper for the Giftbit API",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Dakota Brown",
    author_email="dakota.kae.brown@gmail.com",
    url="https://github.com/da-code-a/pygiftbit",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["pygiftbit"],
    include_package_data=True,
    install_requires=["requests"]
)
