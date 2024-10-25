from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codegen-gym",
    version="0.0.1",
    author="Kasper Rasmussen",
    author_email="kasmura@gmail.com",
    description="A package for research on LLMs and codegen",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kmrasmussen/codegen-gym",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "datasets",
        "numpy"
    ],
)