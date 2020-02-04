## Make your code publish-ready
Let’s prepare our code for the uploading. 
Make sure to not include code that exists outside of a class or a function, otherwise this code will run 
every time the library gets imported. If you want to include example code into the classes (which is legit), 
wrap it into the “__main__” function.

````python
if __name__ == "__main__":
    # your example code goes here
````

## Create a python package
To create a package, create a folder that is named exactly how you want your package to be named. 
Place all the files and classes that you want to ship into this folder.

Now, inside the folder, create a file called __init__.py (as usual with two underscores) and write 
nothing but import statements that have the following schema:

`````python
from pystatmath.hello import HelloStatmath
`````

The __init__.py file is used to mark which classes you want the user to access through the package interface.

## Create the files the PyPI needs
PyPI needs at least these files in order to work:
* setup.py
* setup.cfg
* README.md (optinal but highly recommended)

Place all these files outside of your package folder:
`````
root/
├── pystatmath/
│   ├── __init__.py
│   └── hello.py
├── tests/
│   └── test_hello.py
├── README.md
├── setup.cfg
└── setup.py
`````

## setup.py
The `setup.py` file contains information about our package that the PyPI needs, like its name, a description, 
the current version etc. Here’s a minimal setup script using `setuptools`:

`````python
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="pystatmath",
    version="0.0.1",
    description="Our awesome package",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["numpy"],
)
`````

The parameters that are 100% necessary in the call to `setup()` are the following:
* `name`: the name of your package as it will appear on PyPI
* `version`: the current version of your package
* `packages`: the packages and subpackages containing your source code

Typically, you want to include your `README.md` as the `long_description` argument to `setup()`. 
This will display your README on the registry. Note that you should use the `setup()` parameter 
`long_description_content_type` 
to tell PyPI which format you are using. Valid values are text/markdown, text/x-rst, and text/plain.

In more complicated projects, there might be many packages to list. To simplify this job, setuptools 
includes `find_packages()`, which does a good job of discovering all your subpackages.

`install_requires` is used to list any dependencies your package has to third party libraries.
`entry_points` is used to create scripts that call a function within your package.

For more examples of a typical setup file, refer to the following 
[repository](https://github.com/navdeep-G/setup.py).

## setup.cfg
If you have a description file, you can specify it here:

`````editorconfig
# Inside of setup.cfg
[metadata]
description-file = README.md
`````
More on the topic [here](https://docs.python.org/3/distutils/configfile.html).

# Building our package
Packages on PyPI are not distributed as plain source code. Instead, they are wrapped into distribution packages. 
The most common formats for distribution packages are source archives and Python wheels.

A source archive consists of our source code and any supporting files wrapped into one `.tar` file. Similarly, 
a wheel is essentially a zip archive containing our code. In contrast to the source archive, the wheel 
includes any extensions ready to use.

To create a source archive and a wheel for our package, we can run the following command:

`python setup.py sdist bdist_wheel`

or simply: 

`python setup.py sdist`

for a source archive.

As long as the `dist/` folder is created, the package is ready to be published with Twine:

`twine upload dist/*`. 

Please refer to the readme in our [Nexus3](https://gitlab.statmath.de/) repository on how to configure pip on your/host machine. 












