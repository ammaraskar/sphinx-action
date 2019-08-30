# Sphinx Build Action

[![Build Status](https://travis-ci.org/ammaraskar/sphinx-action.svg?branch=master)](https://travis-ci.org/ammaraskar/sphinx-action)
[![Test Coverage](https://codecov.io/gh/ammaraskar/sphinx-action/branch/master/graph/badge.svg)](https://codecov.io/gh/ammaraskar/sphinx-action)


This is a Github action that looks for Sphinx documentation folders in your
project. It builds the documentation using Sphinx and any errors in the build
process are bubbled up as Github status checks.

The main purposes of this action are:

* Run a CI test to ensure your documentation still builds. 

* Allow contributors to get build errors on simple doc changes inline on Github
  without having to install Sphinx and build locally.

## How to use

Create a workflow for the action, for example:

```yaml
name: "Pull Request Docs Check"
on: 
- pull_request

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: ammaraskar/sphinx-action@master
      with:
        repo-token: "${{ secrets.GITHUB_TOKEN }}"
        args: "Docs/ some_other_docs_folder/"
```

If you don't want the fancy in-line warnings, just remove the `repo-token` in
the `with` block.

## Running the tests

`python -m unittest`
