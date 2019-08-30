import json
import requests
import unittest
from unittest import mock

from sphinx_action import status_check


class TestStatusChecks(unittest.TestCase):

    @mock.patch('sphinx_action.status_check.requests.post')
    def test_create_check(self, mock_post):
        mock_response = mock.NonCallableMock(requests.Response)
        mock_response.status_code = 200
        mock_response.json = mock.Mock(return_value=create_response)

        mock_post.return_value = mock_response

        id = status_check.create_in_progress_status_check(
            'SecretToken', 'sha_hash', 'ammaraskar/sphinx-action'
        )

        self.assertEqual(id, 4)
        mock_post.assert_called_once_with(
            'https://api.github.com/repos/ammaraskar/sphinx-action/check-runs',
            headers={
                'Authorization': 'Bearer SecretToken',
                'Content-Type': 'application/json',
                'Accept': 'application/vnd.github.antiope-preview+json',
                'User-Agent': 'sphinx-action'
            },
            json={
                'name': 'Sphinx Check',
                'head_sha': 'sha_hash',
                'status': 'in_progress',
                'started_at': mock.ANY
            }
        )

    @mock.patch('sphinx_action.status_check.requests.patch')
    def test_finish_status_check_success(self, mock_patch):
        mock_response = mock.NonCallableMock(requests.Response)
        mock_response.status_code = 200

        mock_patch.return_value = mock_response

        check_output = status_check.CheckOutput(
            title='Test Check', summary='Test Finished', annotations=[]
        )
        status_check.finish_status_check(
            id=9, conclusion=status_check.StatusConclusion.SUCCESS,
            github_token='SecretToken2', repo='ammaraskar/sphinx-action',
            check_output=check_output
        )

        mock_patch.assert_called_once_with(
            'https://api.github.com/repos/ammaraskar/sphinx-action/check-runs/9', # noqa
            headers={
                'Authorization': 'Bearer SecretToken2',
                'Content-Type': 'application/json',
                'Accept': 'application/vnd.github.antiope-preview+json',
                'User-Agent': 'sphinx-action'
            },
            json={
                'completed_at': mock.ANY,
                'conclusion': 'success',
                'output': {
                    'title': 'Test Check',
                    'summary': 'Test Finished',
                    'annotations': []
                }
            }
        )

    @mock.patch('sphinx_action.status_check.requests.patch')
    def test_finish_status_check_fail(self, mock_patch):
        mock_response = mock.NonCallableMock(requests.Response)
        mock_response.status_code = 200

        mock_patch.return_value = mock_response

        annotations = [
            status_check.CheckAnnotation(
                path='Doc/using/index.rst', start_line=3, end_line=3,
                annotation_level=status_check.AnnotationLevel.WARNING,
                message='Unexpected section title.'
            ),
            status_check.CheckAnnotation(
                path='Doc/distutils/disclaimer.rst', start_line=1, end_line=1,
                annotation_level=status_check.AnnotationLevel.FAILURE,
                message=':ref:`asdf` not found.'
            )
        ]
        check_output = status_check.CheckOutput(
            title='Test Check', summary='Test Failed', annotations=annotations
        )
        status_check.finish_status_check(
            id=32, conclusion=status_check.StatusConclusion.FAILURE,
            github_token='SecretToken3', repo='ammaraskar/sphinx-action',
            check_output=check_output
        )

        mock_patch.assert_called_once_with(
            'https://api.github.com/repos/ammaraskar/sphinx-action/check-runs/32', # noqa
            headers={
                'Authorization': 'Bearer SecretToken3',
                'Content-Type': 'application/json',
                'Accept': 'application/vnd.github.antiope-preview+json',
                'User-Agent': 'sphinx-action'
            },
            json={
                'completed_at': mock.ANY,
                'conclusion': 'failure',
                'output': {
                    'title': 'Test Check',
                    'summary': 'Test Failed',
                    'annotations': [
                        {
                            'path': 'Doc/using/index.rst',
                            'start_line': 3, 'end_line': 3,
                            'annotation_level': 'warning',
                            'message': 'Unexpected section title.'
                        },
                        {
                            'path': 'Doc/distutils/disclaimer.rst',
                            'start_line': 1, 'end_line': 1,
                            'annotation_level': 'failure',
                            'message': ':ref:`asdf` not found.'
                        }
                    ]
                }
            }
        )


create_response = json.loads("""
{
  "id": 4,
  "head_sha": "ce587453ced02b1526dfb4cb910479d431683101",
  "node_id": "MDg6Q2hlY2tSdW40",
  "external_id": "42",
  "url": "https://api.github.com/repos/github/hello-world/check-runs/4",
  "html_url": "http://github.com/github/hello-world/runs/4",
  "details_url": "https://example.com",
  "status": "in_progress",
  "conclusion": null,
  "started_at": "2018-05-04T01:14:52Z",
  "completed_at": null,
  "output": {
    "title": "Mighty Readme Report",
    "summary": "",
    "text": ""
  },
  "name": "mighty_readme",
  "check_suite": {
    "id": 5
  },
  "app": {
    "id": 1,
    "node_id": "MDExOkludGVncmF0aW9uMQ==",
    "owner": {
      "login": "github",
      "id": 1,
      "node_id": "MDEyOk9yZ2FuaXphdGlvbjE=",
      "url": "https://api.github.com/orgs/github",
      "repos_url": "https://api.github.com/orgs/github/repos",
      "events_url": "https://api.github.com/orgs/github/events",
      "hooks_url": "https://api.github.com/orgs/github/hooks",
      "issues_url": "https://api.github.com/orgs/github/issues",
      "members_url": "https://api.github.com/orgs/github/members{/member}",
      "avatar_url": "https://github.com/images/error/octocat_happy.gif",
      "description": "A great organization"
    },
    "name": "Super CI",
    "description": "",
    "external_url": "https://example.com",
    "html_url": "https://github.com/apps/super-ci",
    "created_at": "2017-07-08T16:18:44-04:00",
    "updated_at": "2017-07-08T16:18:44-04:00"
  },
  "pull_requests": []
}""")


if __name__ == '__main__':
    unittest.main()
