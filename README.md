## Make your code publish-ready
First of all we need to prepare the code to be uploaded to our Nexus repository.
Make sure to not include code that exists outside of a class or a function, otherwise it will be executed 
every time the library gets imported. If you want to include example code into the classes (which is legit), 
wrap it into the “__main__” function:

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

## Create the files the python package index (PyPI) needs
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
README = (HERE / "README.md").read_text(encoding="utf8")

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

**Note: the version is currently hard coded. However we can set it dynamically during the CD. See the CI/CD section below.** 

The parameters that are 100% necessary in the call to `setup()` are the following:
* `name`: the name of your package as it will appear on PyPI
* `version`: the current version of your package
* `packages`: the packages and subpackages containing your source code

Typically, you want to include your `README.md` as the `long_description` argument to `setup()`. 
This will display your README on the registry. Note that you should use the `setup()` parameter 
`long_description_content_type` 
to tell PyPI which format you are using. Valid values are `text/markdown`, `text/x-rst`, and `text/plain.

In more complicated projects, there might be many packages to list. To simplify this job, setuptools 
includes `find_packages()`, which does a good job of discovering all your subpackages.

`install_requires` is used to list any dependencies our package has to third party libraries.
`entry_points` is used to create scripts that call a function within our package.

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

# Publishing a package
Packages on PyPI are not distributed as plain source code. Instead, they are wrapped into distribution packages. 
The most common formats for distribution packages are source archives and Python wheels.

A source archive consists of our source code and any supporting files wrapped into one `.tar` file. Similarly, 
a wheel is essentially a `.zip archive containing our code. In contrast to the source archive, the wheel 
includes any extensions ready to use.

To create a source archive and a wheel for our package, we can run the following command:

`python setup.py sdist bdist_wheel`

or simply: 

`python setup.py sdist`

for a source archive.

As soon as the `dist/` folder is created, the package is ready to be published with **Twine**:

`twine upload dist/*`. 

The full command to publish the package into our nexus is: 
`twine upload --repository-url https://nexus3.statmath.de/repository/pypi-internal/ dist/*`

Instead of typing the username and password everytime, you could use keyring, too:

`keyring set https://upload.pypi.org/legacy/ your-username`

To disable keyring again, you have to execute: `keyring --disable`

# Installing a package

If the `pip.conf` file is configured properly, you will be able to install any package with a usuall 
`pip install <package-name>` command. The Pip in this case will first hit our Group-Repo on Nexus3, then index 
our Internal-Repo for the package. If there is none, the traffic will be redirected to the [pypi.org](https://pypi.org) 
through our proxy.   

Please refer to the readme in our [Nexus3](https://gitlab.statmath.de/) repository on how to configure 
`pip` on your/host machine. 


# CI/CD

Ideally we want our code to be tested and published to the PyPI automatically on overy push and/or merge request.
We use GitLab as our CI/CD tool. The workflow here is the following: there is a **runner** deployed and configured 
on a separate server, waiting to take a job from our GitLab instance. The GitLab instance checks for a `.gitlab_ci.yml`
file in our repository to send appropriate commands to the **runner**.  

The runner for python packages is available under the tag `gitlab_py_docker_runner_1`. 
1. In your project, go to the Settings => CI/CD => Runners to make sure the runner is **available** and **enabled** 
for this project.
2. Go to the Settings => CI/CD => Variables and set the following key-value pairs:
    * PUBLISH_USERNAME : <nexus3-username>
    * PUBLISH_PASSWORD: <nexus3-password>
    * PYPRI_REPOSITORY_URL : https://nexus3.statmath.de/repository/pypi-internal/
**See our BitWarden vault to get username/password**
3. Configure your `.gitlab_ci.yml`. Make sure to refer to the runner by its tag. Also note that you can only use 
an image which is available to the runner on its host machine. Currently there is a  `python:3.7.2-slim`. 
4. If you configure your CI/CD script as in this example, there will be two stages: one for tests and one for build/publish. 
The pipeline should be triggered on every push to the repository. The package will be published to our Nexus under a version
which corresponds to the pipeline id. See the `setup.py file. 

**Overall refer to this repository as a basic working example**
