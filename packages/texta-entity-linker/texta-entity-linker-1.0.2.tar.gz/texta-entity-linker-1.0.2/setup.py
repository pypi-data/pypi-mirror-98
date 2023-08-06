import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf8").read()


setup(
    name="texta-entity-linker",
    version=read("VERSION").strip(),
    author="TEXTA",
    author_email="info@texta.ee",
    description=("TEXTA Entity Linker"),
    license="GPLv3",
    packages=["texta_entity_linker", "data"],
    data_files=["VERSION", "requirements.txt", "README.md", "LICENSE"],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://git.texta.ee/texta/texta-entity-linker",
    install_requires=read("requirements.txt").split("\n"),
    include_package_data=True,
)
