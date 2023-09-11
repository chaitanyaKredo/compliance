from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in compliance/__init__.py
from compliance import __version__ as version

setup(
	name="compliance",
	version=version,
	description="Indian Compliance",
	author="chaitanya",
	author_email="chaitanya@kredo.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
