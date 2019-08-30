import collections
import tempfile
import subprocess


GithubEnvironment = collections.namedtuple(
    'GithubEnvironment',
    ['github_sha', 'github_repo', 'github_token', 'github_workspace']
)


def build_docs(docs_directory):
    with tempfile.NamedTemporaryFile() as warnings_file:
        subprocess.check_call(
            ['make', 'html', '--no-color', '-w', warnings_file],
            cwd=docs_directory
        )


def build_all_docs(github_env, docs_directories):
    if len(docs_directories) == 0:
        raise ValueError("Please provide at least one docs directory to build")

    for docs_dir in docs_directories:
        print("====================================")
        print("Building docs in {}".format(docs_dir))
        print("====================================")

        build_docs(docs_dir)
