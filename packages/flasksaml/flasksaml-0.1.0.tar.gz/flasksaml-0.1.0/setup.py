import os
from setuptools import setup, find_packages

requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(requirements_path) as fh:
    requirements = fh.read().split("\n")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flasksaml",
    version="0.1.0",
    description="A Flask wrapper that implements SAML Service Provider functionalities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ninja-van/flasksaml.git",
    author="Teddy Hartanto",
    author_email="teddyhartanto96@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    dependency_links=[],
    install_requires=requirements,
    python_requires=">=3.6",
    keywords="saml saml2 flask python3",
)
