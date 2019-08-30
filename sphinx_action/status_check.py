"""
This module interacts with the Github API to create a status check
with in-line warnings and errors.
"""
import collections
import datetime
import requests


class StatusConclusion:
    SUCCESS = 'success'
    FAILURE = 'failure'


class AnnotationLevel:
    NOTICE = 'notice'
    WARNING = 'warning'
    FAILURE = 'failure'


CheckOutput = collections.namedtuple(
    'CheckOutput', ['title', 'summary', 'annotations']
)
CheckAnnotation = collections.namedtuple(
    'CheckAnnotation',
    ['path', 'start_line', 'end_line', 'annotation_level', 'message']
)

BASE_HEADERS = {
  'Content-Type': 'application/json',
  'Accept': 'application/vnd.github.antiope-preview+json',
  'User-Agent': 'sphinx-action'
}


def create_in_progress_status_check(github_token, head_sha, repo):
    """Creates an in-progress status check for Github."""
    payload = {
        'name': 'Sphinx Check',
        'head_sha': head_sha,
        'status': 'in_progress',
        'started_at': datetime.datetime.utcnow().isoformat(),
    }
    headers = BASE_HEADERS.copy()
    headers['Authorization'] = 'Bearer {}'.format(github_token)

    url = 'https://api.github.com/repos/{repo}/check-runs'.format(repo=repo)
    r = requests.post(url, json=payload, headers=headers)

    r.raise_for_status()
    return r.json()['id']


def finish_status_check(id, conclusion, github_token, repo, check_output):
    """Marks a status check as finished with the given conclusion and output"""
    annotations = [a._asdict() for a in check_output.annotations]
    payload = {
        'completed_at': datetime.datetime.utcnow().isoformat(),
        'conclusion': conclusion,
        'output': {
            'title': check_output.title,
            'summary': check_output.summary,
            'annotations': annotations
        }
    }
    headers = BASE_HEADERS.copy()
    headers['Authorization'] = 'Bearer {}'.format(github_token)

    url = 'https://api.github.com/repos/{repo}/check-runs/{run_id}'.format(
        repo=repo, run_id=id)
    r = requests.patch(url, json=payload, headers=headers)

    r.raise_for_status()
