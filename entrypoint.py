#!/usr/bin/env python3
import os
import json
from sphinx_action import action

# This is the entrypoint called by Github when our action is run. All the
# Github specific setup is done here to make it easy to test the action code
# in isolation.
if __name__ == "__main__":
    print("[sphinx-action] Starting sphinx-action build.")

    if "INPUT_PRE-BUILD-COMMAND" in os.environ:
        pre_command = os.environ["INPUT_PRE-BUILD-COMMAND"]
        print("Running: {}".format(pre_command))
        os.system(pre_command)

    sha = os.environ["GITHUB_SHA"]
    # Currently pull requests provide a token that don't support adding
    # check annotations, however there is another API based on putting
    # certain lines in stdout we can use in it's place. Hence if this is
    # a pull request, 
    if os.environ["GITHUB_EVENT_NAME"] == "pull_request":
        with open(os.environ["GITHUB_EVENT_PATH"], "r") as f:
            event = json.load(f)
            sha = event["pull_request"]["head"]["sha"]
            print("[sphinx-action] Using pull request sha: {}".format(sha))

    github_env = action.GithubEnvironment(
        sha=sha,
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
