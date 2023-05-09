# Development setup

Notes on setting up a development environment for working with glm-py. 

Create a conda environment:

```
conda create -n glm-py python=3.10
```

Install packages for documentation:

```
pip install mkdocs==1.4.2
pip install "mkdocstrings[python]"==0.21.2
pip install mkdocs-material==9.1.8
pip install pre-commit
pip install flake8
pip install flake8-docstrings
pip install black
pip install "pandas[excel]"==2.0.1
```

Build the docs (from the package root): 

```
mkdocs serve 
```

## Code style

* Format all code using autopep8
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