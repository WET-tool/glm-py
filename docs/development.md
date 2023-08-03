# Development setup

## Environment

A Docker container can be used to create a development environment. You can either build the Docker image:

```
docker build -t glmpy-dev .devcontainer
```
Or, you can develop glmpy using a dev container. 

### Code style

Code linting and formatting uses ruff and black. A script to format the glm-met repository can be run: `./scripts/format.sh`. 

pre-commit is used to run ruff and black. 

## Tests

<a href="https://docs.pytest.org/en/7.4.x/" target="_blank">pytest</a> is used for testing glm-met. 

If testing, please add tests under the `tests` directory. If you need test data for running tests, add them as `pytest.fixtures` in `conftest.py`. 

Build the docs (from the package root): 

```
mkdocs serve 
```

## Code style

* Format all code using black (see `./scripts/format.sh`)
* Manually correct all ruff errors
* Use pre-commit to format Python code before git commits
* Use NumPy style docstrings - [follow NumPy conventions](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard)

### Methods / function docstring

Example from [Pandas](https://pandas.pydata.org/docs/development/contributing_docstring.html):

* Summary - one line function / method summary.
* Extended summary - one or two sentences outlining what the function achieves and when / where it is used.
* Parameter description - list function arguments, keywords, and types.
* Returns / yields section - list returns / yields from the function and their types.
* Notes - optional notes section.
* Examples - example to illustrate how the function can be used.

```
"""
Add up two integer numbers.

This function simply wraps the ``+`` operator, and does not
do anything interesting, except for illustrating what
the docstring of a very simple function looks like.

Parameters
----------
num1 : int
    First number to add.
num2 : int
    Second number to add.

Returns
-------
int
    The sum of ``num1`` and ``num2``.

See Also
--------
subtract : Subtract one integer from another.

Examples
--------
>>> add(2, 2)
4
>>> add(25, 0)
25
>>> add(10, -10)
0
"""
```

### Class docstring

* Summary - one line class summary.
* Extended summary - one or two sentences outlining the class purpose and use.
* Attributes description - list function arguments, keywords, and types.
* Example - short example indicating class usage.
* Notes - optional notes section

Do not list methods - add docstrings to methods within the class. 


### Build package

```
python -m build
```
