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
```

* You can choose a Sphinx version by using the appropriate tag. For example, to
  specify Sphinx 7.0.0 you would use `ammaraskar/sphinx-action@7.0.0`. `master`
  currently uses Sphinx 2.4.4.

* If you have any Python dependencies that your project needs (themes, 
build tools, etc) then place them in a requirements.txt file inside your docs
folder.

* If you have multiple sphinx documentation folders, please use multiple
  `uses` blocks.

For a full example repo using this action including advanced usage, take a look
at https://github.com/ammaraskar/sphinx-action-test

## Great Actions to Pair With

Some really good actions that work well with this one are
[`actions/upload-artifact`](https://github.com/actions/upload-artifact)
and [`ad-m/github-push-action`](https://github.com/ad-m/github-push-action).

You can use these to make built HTML and PDFs available as artifacts:

```yaml
    - uses: actions/upload-artifact@v1
      with:
        name: DocumentationHTML
        path: docs/_build/html/
```

Or to push docs changes automatically to a `gh-pages` branch:

<details><summary>Code for your workflow</summary>
<p>

```yaml
    - name: Commit documentation changes
      run: |
        git clone https://github.com/your_git/repository.git --branch gh-pages --single-branch gh-pages
        cp -r docs/_build/html/* gh-pages/
        cd gh-pages
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add .
        git commit -m "Update documentation" -a || true
        # The above command will fail if no changes were present, so we ignore
        # the return code.
    - name: Push changes
      uses: ad-m/github-push-action@master
      with:
        branch: gh-pages
        directory: gh-pages
        github_token: ${{ secrets.GITHUB_TOKEN }}
```

</p>
</details>

For a full fledged example of this in action take a look at:
https://github.com/ammaraskar/sphinx-action-test

## Advanced Usage

If you wish to customize the command used to build the docs (defaults to
`make html`), you can provide a `build-command` in the `with` block. For
example, to invoke sphinx-build directly you can use:

```yaml
    - uses: ammaraskar/sphinx-action@master
      with:
        docs-folder: "docs/"
        build-command: "sphinx-build -b html . _build"
```

If there's system level dependencies that need to be installed for your
build, you can use the `pre-build-command` argument like so:

```yaml
    - uses: ammaraskar/sphinx-action@master
      with:
        docs-folder: "docs2/"
        pre-build-command: "apt-get update -y && apt-get install -y latexmk texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended"
        build-command: "make latexpdf"
```

## Running the tests

`python -m unittest`

## Formatting

Please use [black](https://github.com/psf/black) for formatting:

`black entrypoint.py sphinx_action tests`
