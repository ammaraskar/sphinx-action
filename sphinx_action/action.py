import collections


GithubEnvironment = collections.namedtuple(
    'GithubEnvironment',
    ['github_sha', 'github_repo', 'github_token', 'github_workspace']
)


def build_docs(docs_directory):
    pass


def build_all_docs(github_env, docs_directories):
    if len(docs_directories) == 0:
        raise ValueError("Please provide at least one docs directory to build")
