import pathlib
from setuptools import setup, find_packages

CURRENT_DIR = pathlib.Path(__file__).parent
README_CONTENT = (CURRENT_DIR / "README.md").read_text()

setup(
    name='py-auto-di',
    version='0.1.2',
    packages=["PyAutoDI"],
    include_package_data=True,
    author="Chris Stead",
    author_email="cmstead@gmail.com",
    url="https://github.com/cmstead/py-auto-di#readme",
    platforms=['any'],
    description="Lightweight, automatic Python DI library",
    license='MIT',
    long_description=README_CONTENT,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)