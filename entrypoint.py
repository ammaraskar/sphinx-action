#!/usr/bin/env python3
import os
from sphinx_action import action

# This is the entrypoint called by Github when our action is run. All the
# Github specific setup is done here to make it easy to test the action code
# in isolation.
if __name__ == "__main__":
    if "INPUT_PRE-BUILD-COMMAND" in os.environ:
        pre_command = os.environ["INPUT_PRE-BUILD-COMMAND"]
        print("Running: {}".format(pre_command))
        os.system(pre_command)

    github_env = action.GithubEnvironment(
        sha=os.environ["GITHUB_SHA"],
        repo=os.environ["GITHUB_REPOSITORY"],
        # For the GITHUB_TOKEN, we want to be able to proceed even if the
        # action isn't given a token. Thus we do a .get() to get a default
        # value of None if it doesn't exist.
        token=os.environ.get("INPUT_REPO-TOKEN"),
        build_command=os.environ.get("INPUT_BUILD-COMMAND"),
    )

    if not github_env.token:
        print("[sphinx-action] Running without repo token")

    # We build the docs folder passed in the inputs.
    action.build_all_docs(github_env, [os.environ.get("INPUT_DOCS-FOLDER")])
