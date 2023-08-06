from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="queueCrypt",
    version="0.0.1",
    description="A library that creates a queue and secures it better.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    author="Daniel Katz",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["queueCrypt"]
)
