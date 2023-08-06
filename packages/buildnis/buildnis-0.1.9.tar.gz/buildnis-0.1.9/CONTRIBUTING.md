# Contributing

## Table of Contents

- [Contributing](#contributing)
  - [Table of Contents](#table-of-contents)
  - [Coding Standards](#coding-standards)
  - [Setting up the Development Environment](#setting-up-the-development-environment)
    - [Getting the source code from GitHub](#getting-the-source-code-from-github)
    - [Setting up the Python environment](#setting-up-the-python-environment)
  - [License](#license)

## Coding Standards

See for details.

## Setting up the Development Environment

### Getting the source code from GitHub

Clone the Buildnis Github repository using

``` shell
git clone https://github.com/Release-Candidate/Buildnis.git
```

or, if you are using SSH:

``` shell
git clone git@github.com:Release-Candidate/Buildnis.git
```

or enter the repository URI in the Git frontend of your choice (like [Tortoise Git](https://tortoisegit.org/) for Windows).

### Setting up the Python environment

First install the package `pipenv` to have a simple way to install all needed packages in a virtual Python environment for this project. So, first install the Pipenv using Pip:

``` shell
python -m pip install pipenv
```

Now, enter the root directory of the checked out Buildnis sources, `Buildnis`, and call

``` shell
pipenv install --dev
```

to install all the needed packages including these only needed for development (read from the file [Pipfile](./Pipfile)). After that you have all needed packages to develop, generate the documentation and run the program in this virtual environment, just always call `pipenv run` to run a python script or start a virtual environment in the current shell using `pipenv shell`. You can leave this virtual environment with the command `exit`.

See also [Pipenv Documentation](https://pipenv-fork.readthedocs.io/en/latest/basics.html#example-pipenv-workflow)

## License

We do not require any formal copyright assignment or contributor license agreement. Any contributions intentionally sent upstream are presumed to be offered under terms of the OSI-approved MIT License. See [LICENSE](./LICENSE) for details.
