from setuptools import setup


def readme():
    with open('README.md', 'r') as f:
        return f.read()


def reqs():
    with open('requirements.txt', 'r') as f:
        return f.readlines()


setup(
    name="essentialsx",
    version="0.0.2",
    description="Essential functions to be easily reused across Python projects.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/mistergates/essentialsx",
    author="Mitch Gates",
    author_email="gates55434@gmail.com",
    keywords="core utilities, logging, hotkeys",
    license="MIT",
    packages=["essentialsx"],
    install_requires=reqs(),
    include_package_data=True
)
