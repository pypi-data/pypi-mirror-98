from setuptools import setup, find_packages

version = "0.4.6"

with open("README.md", "r") as f:
	long_desc = f.read()

setup(
name="discord-ext-paginator",
author="Alex Hutz",
author_email="frostiiflames@gmail.com",
keywords=["discord.py", "paginator"],
version=version,
packages=['discord.ext.paginator'],
license='MIT',
long_description=long_desc,
long_description_content_type="text/markdown",
description="An package for discord pagination.",
install_requires=['discord.py>=1.5.1'],
python_requires='>=3.7.1'
)