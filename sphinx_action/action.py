import collections
import subprocess
import tempfile
import os


GithubEnvironment = collections.namedtuple(
    'GithubEnvironment',
    ['github_sha', 'github_repo', 'github_token', 'github_workspace']
)


def build_docs(docs_directory):
    docs_requirements = os.path.join(docs_directory, 'requirements.txt')
    if os.path.exists(docs_requirements):
        subprocess.check_call(['pip', 'install', '-r', docs_requirements])

    with tempfile.NamedTemporaryFile() as warnings_file:
        subprocess.check_call(
            ['make', 'SPHINXOPTS=--no-color -w {}'.format(warnings_file.name),
             'html'],
            cwd=docs_directory
        )

    return []


def build_all_docs(github_env, docs_directories):
    if len(docs_directories) == 0:
        raise ValueError("Please provide at least one docs directory to build")

    for docs_dir in docs_directories:
        print("====================================")
        print("Building docs in {}".format(docs_dir))
        print("====================================")

        build_docs(docs_dir)
