from setuptools import setup, find_packages

version = {}
with open("betula/version.py") as fp:
    exec(fp.read(), version)

setup(
    name="betula",
    version=version["__version__"],
    author="Peter Vegh",
    description="Optofluidic cell assay data analysis",
    long_description=open("pypi-readme.rst").read(),
    long_description_content_type="text/x-rst",
    keywords="biology",
    packages=find_packages(exclude="docs"),
)
