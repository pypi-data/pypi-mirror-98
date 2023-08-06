from setuptools import setup, find_packages
import os

parent_path = os.path.dirname(os.path.realpath(__file__))
requirements_path = parent_path + '/requirements.txt'
install_requires = []

if os.path.isfile(requirements_path):
    with open(requirements_path) as f:
        install_requires = f.read().splitlines()

setup(
    name="base_processor",
    version="0.0.2",
    install_requires=install_requires,
    packages=find_packages(exclude=("tests",)),
)