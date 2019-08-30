#!/usr/bin/env python3
import os
import sys
from sphinx_action import action

# This is the entrypoint called by Github when our action is run. All the
# Github specific setup is done here to make it easy to test the action code
# in isolation.
if __name__ == "__main__":
    github_env = action.GithubEnvironment(
        github_sha=os.environ['GITHUB_SHA'],
        github_repo=os.environ['GITHUB_REPOSITORY'],
        # For the GITHUB_TOKEN, we want to be able to proceed even if the
        # action isn't given a token. Thus we do a .get() to get a default
        # value of None if it doesn't exist.
        github_token=os.environ.get('GITHUB_TOKEN'),
        github_workspace=os.environ['GITHUB_WORKSPACE']
    )

    # The docs directories to build are passed in the arguments.
    action.build_all_docs(github_env, sys.argv[1:])
