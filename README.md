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
  
![Example Screenshot](https://i.imgur.com/Gk2W32O.png)

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
        docs-folder: "docs/"
        repo-token: "${{ secrets.GITHUB_TOKEN }}"
```

* If you have any Python dependencies that your project needs (themes, 
build tools, etc) then place them in a requirements.txt file inside your docs
folder.

* If you have multiple sphinx documentation folders, please use multiple
  `uses` blocks.

* If you don't want the fancy in-line warnings, just remove the `repo-token` in
the `with` block.

## Advanced Usage

If you wish to customize the command used to build the docs (defaults to
`make html`), you can provide a `build-command` in the `with` block. For
example, to invoke sphinx-build directly you can use:

```yaml
    - uses: ammaraskar/sphinx-action@master
      with:
        docs-folder: "docs/"
        repo-token: "${{ secrets.GITHUB_TOKEN }}"
        build-command: "sphinx-build -b html . _build"
```

If there's system level dependencies that need to be installed for your
build, you can use the `pre-build-command` argument like so:

```yaml
    - uses: ammaraskar/sphinx-action@master
      with:
        docs-folder: "docs2/"
        repo-token: "${{ secrets.GITHUB_TOKEN }}"
        pre-build-command: "apt-get update -y && apt-get install -y latexmk texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended"
        build-command: "make latexpdf"
```

## Running the tests

`python -m unittest`

## Formatting

Please use [black](https://github.com/psf/black) for formatting:

`black entrypoint.py sphinx_action tests`
