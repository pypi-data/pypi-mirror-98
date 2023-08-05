from setuptools import setup, find_packages

VERSION = '2' 

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="cittronn", 
        version=2,
        author="Pewpew Dsouza",
        packages=find_packages(),
        
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
