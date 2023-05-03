from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="NotKevin",
    version="0.0.0",
    author="GandalfsDad",
    description="This is my attempt at combing storage with a gpt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GandalfsDad/NotKevin",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11", #To be verified
    install_requires=[
        'openai',
        'colorama',
        'numpy'
    ],
    packages=find_packages(),
)
