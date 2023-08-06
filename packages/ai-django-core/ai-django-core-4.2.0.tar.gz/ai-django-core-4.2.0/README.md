[![pypi](https://img.shields.io/pypi/v/ai-django-core.svg)](https://pypi.python.org/pypi/ai-django-core/)
[![Downloads](https://pepy.tech/badge/ai-django-core)](https://pepy.tech/project/ai-django-core)

# Overview:
This package contains various useful helper functions. You can read up on all the fancy things at
[readthedocs.io](https://ai-django-core.readthedocs.io/en/latest/index.html).

# Installation:
- Install the package via pip:

    `pip install ai-django-core`

   or via pipenv:

    `pipenv install ai-django-core`

- Add module to `INSTALLED_APPS`:

    ````
    INSTALLED_APPS = (
        ...
        'ai_django_core',
    )
     ````

- Run migrations


# Contribute

## Add functionality

- Clone the project locally
- Create a new branch for your feature
- Change the dependency in your requirements.txt to a local (editable) one that points to your local file system:
    ```
    -e /Users/awesome-developer/Documents/workspace/ai-django-core
    ```
- Ensure the code passes the tests
- Run:

    `python setup.py develop`

- Create a pull request

## Run tests

- Check coverage

    `pytest --cov=.`

- Run tests

    `pytest`

## Update documentation

- To generate new auto-docs for new modules run: `sphinx-apidoc -o ./docs/modules/ ./ai_django_core/` (in the current setup an auto doc for the anti virus module is not supported due to installation and import problems. Since it might be removed in the future, that should be fine for now).
- To build the documentation run: `sphinx-build docs/ docs/_build/html/` or go into the **docs** folder and run: `make html`.
  Open `docs/_build/html/index.html` to see the documentation.

## Publish to ReadTheDocs.io

- Fetch the latest changes in github mirror and push them
- Trigger new build at ReadTheDocs.io (follow instructions in admin panel at RTD)

## Publish to PyPi

- Update documentation about new/changed functionality

- Update the `Changelog`

- Increment version in main `__init__.py`

- Create pull request / merge to master

- Run:

    * Make sure you have all the required packages installed
    `pip install twine wheel`
    * Create a file in your home directory: `~/.pypirc`
    ```
    [distutils]
    index-servers=
        pypi
        testpypi

    [pypi]
    repository: https://upload.pypi.org/legacy/
    username: ambient-innovation

    [testpypi]
    repository: https://test.pypi.org/legacy/
    username: ambient-innovation
    ```
    * Empty `dist` directory
    * Create distribution
    `python setup.py sdist bdist_wheel`
    * Upload to Test-PyPi
    `twine upload --repository testpypi dist/*`
    * Check at Test-PyPi if it looks nice
    * Upload to real PyPi
    `twine upload dist/*`
