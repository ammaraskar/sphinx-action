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
    - uses: actions/checkout@v1
    - uses: ammaraskar/sphinx-action@master
      with:
        repo-token: "${{ secrets.GITHUB_TOKEN }}"
        args: "docs/ some_other_docs_folder/"
```

* If you have any Python dependencies that your project needs (themes, 
build tools, etc) then place them in a requirements.txt file inside your docs
folder.

* If you have multiple sphinx documentation folders, please specify them all in
the `args`.

* If you don't want the fancy in-line warnings, just remove the `repo-token` in
the `with` block.

## Running the tests

`python -m unittest`
