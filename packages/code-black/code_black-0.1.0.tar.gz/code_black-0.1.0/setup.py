# Import required functions
from setuptools import setup, find_packages

# Call setup function
setup(
    author="Tim Schreuder",
    description="A package for randomly allocating patients to IC beds",
    name="code_black",
    packages=find_packages(include=["code_black", "code_black.*"]),
    python_requires='>=3.0',
    version="0.1.0",
)