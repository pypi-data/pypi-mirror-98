import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy-validator",
    version="0.0.1",
    author="brworkit",
    author_email="brworkit@gmail.com",
    description="A package for easy json validation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brworkit/python-package-easy-validator.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)