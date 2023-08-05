import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eSim",
    version="2.1.0",
    author="e-sim-python",
    author_email="DunaBabies@gmail.com",
    description="E-sim python library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/e-sim-python/scripts",
    packages=setuptools.find_packages(),
    install_requires = ["lxml", "discord.py", "pytz"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


"""
Usage:
$ py build
$ py -m twine upload dist/*
username: __token__
password: {my token}
"""
