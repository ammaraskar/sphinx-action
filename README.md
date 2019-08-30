# Sphinx Build Action

This is a Github action that looks for Sphinx documentation folders in your
project. It builds the documentation using Sphinx and any errors in the build
process are bubbled up as Github status checks.

The main purposes of this action are:

* Run a CI test to ensure your documentation still builds. 

* Allow contributors to get build errors on simple doc changes inline on Github
  without having to install Sphinx and build locally.

## How to use

Just add on the action. When it runs it'll search for a Sphinx Makefile in your
directories, when it finds one it builds the documentation there.

If you want the fancy in-line warnings, follow the instructions here to
authorize a `GITHUB_TOKEN` for the action: 
https://developer.github.com/actions/managing-workflows/storing-secrets/#github-token-secret

## Running the tests

`python -m unittest`
