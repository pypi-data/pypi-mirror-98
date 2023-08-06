import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="mmlibrary",
    version="0.0.1",
    description="Model Management Framework & Abstractions",
    long_description=README,
    long_description_content_type="text/markdown",
    #url="n/a",
    #author="n/a",
    #author_email="n/a",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    packages=["mmlibrary"],
    include_package_data=True,
    install_requires=[],
    #entry_points={
    #    "console_scripts": [
    #        "mmlibrary=mmlibrary.__main__:main",
    #    ]
    #}
)