#!/usr/bin/env -S python3 -u
import os
import json
import subprocess
import sys
from sphinx_action import action

# This is the entrypoint called by Github when our action is run. All the
# Github specific setup is done here to make it easy to test the action code
# in isolation.


def interpret_env(env_var):
    if isinstance(env_var, str):
        return env_var.lower() not in ["false", "no", "off" "0"]
    return bool(env_var)


if __name__ == "__main__":
    print("[sphinx-action] Starting sphinx-action build.")

    update = os.environ.get("INPUT_UPDATE", False)
    should_update = interpret_env(update)

    install = os.environ.get("INPUT_INSTALL", "")
    packages = install.split()

    if should_update or packages:
        print("Updating apt...")
        subprocess.call(["/usr/bin/apt", "-y", "update"])

    print(f"{len(packages)} packages (plus dependencies) to install")
    if packages:
        subprocess.call(["/usr/bin/apt", "-y", "install", *packages])

    if "INPUT_PRE-BUILD-COMMAND" in os.environ:
        pre_command = os.environ["INPUT_PRE-BUILD-COMMAND"]
        print("Running: {}".format(pre_command))
        os.system(pre_command)

    github_env = action.GithubEnvironment(
        build_command=os.environ.get("INPUT_BUILD-COMMAND"),
    )

    # We build the doc folder passed in the inputs.
    action.build_all_docs(github_env, [os.environ.get("INPUT_DOCS-FOLDER")])
