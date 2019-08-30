import collections


GithubEnvironment = collections.namedtuple(
    'GithubEnvironment',
    ['github_sha', 'github_repo', 'github_token', 'github_workspace']
)


def build_docs(docs_directory):
    pass


def find_docs_directories(project_root_directory):
    pass


def build_all_docs(github_env):
    pass
