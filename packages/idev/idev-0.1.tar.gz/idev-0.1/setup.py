
from setuptools import setup, find_packages

setup(
    name = 'idev',
    packages = ['idev'],   
    include_package_data=True,    # muy importante para que se incluyan archivos sin extension .py
    version = '0.1',
    description = 'Termux framework para la api de termux en pytjon',
    author='joaquin osorio vazquez',
    author_email="kemalmoto.e5@gmail.com",
    license="GPLv3",
    url="https://github.com/h-whokf/idev",
    classifiers = ["Programming Language :: Python :: 3",\
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",\
        "Development Status :: 4 - Beta", "Intended Audience :: Developers", \
        "Operating System :: OS Independent"],
    )
