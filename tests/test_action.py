import os
import unittest
from unittest import mock

from sphinx_action import action, status_check


TEST_PROJECTS_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'test_projects'
)


class TestAction(unittest.TestCase):

    def test_extract_line_information_with_no_line_info(self):
        self.assertEqual(
            action.extract_line_information(
                'warnings_and_errors/index.rst: '
            ),
            ('warnings_and_errors/index.rst', 1)
        )

    def test_extract_line_information_with_line_info(self):
        self.assertEqual(
            action.extract_line_information(
                'warnings_and_errors/contents.rst:19: '
            ),
            ('warnings_and_errors/contents.rst', 19)
        )

    def test_extract_line_information_with_invalid_info(self):
        self.assertEqual(action.extract_line_information('adsfafadf'), None)

    def test_extract_line_information_with_invalid_lineno(self):
        self.assertEqual(action.extract_line_information('index.rst:a:'), None)

    def test_build_docs_with_no_docs_directories(self):
        """Make sure we bail out if they don't provide a single documentation
        directory"""
        with self.assertRaises(ValueError):
            action.build_all_docs(None, [])

    def test_build_docs_no_errors_or_warnings(self):
        """Check that we correctly build docs when there's no errors or
        warnings"""
        return_code, annotations = action.build_docs(
            os.path.join(TEST_PROJECTS_DIR, 'no_errors')
        )
        self.assertEqual(return_code, 0)
        self.assertEqual(annotations, [])

    def test_build_docs_errors(self):
        return_code, annotations = action.build_docs(
            os.path.join(TEST_PROJECTS_DIR, 'errors')
        )
        self.assertEqual(annotations, [])

    def test_build_docs_warnings(self):
        return_code, annotations = action.build_docs(
            os.path.join(TEST_PROJECTS_DIR, 'warnings')
        )
        self.assertEqual(return_code, 0)
        self.assertEqual(len(annotations), 3)

        self.assertTrue(annotations[0].path.endswith('index.rst'))
        self.assertEqual(annotations[0].start_line, 22)
        self.assertEqual(annotations[0].end_line, 22)
        self.assertIn('Problems with "include"', annotations[0].message)

        self.assertTrue(annotations[1].path.endswith('index.rst'))
        self.assertEqual(annotations[1].start_line, 24)
        self.assertEqual(annotations[1].end_line, 24)
        self.assertEqual(
            'Unknown directive type "BADDIRECTIVE".', annotations[1].message
        )

        self.assertTrue(annotations[2].path.endswith('notintoc.rst'))
        self.assertEqual(annotations[2].start_line, 1)
        self.assertEqual(annotations[2].end_line, 1)
        self.assertEqual(
            "document isn't included in any toctree", annotations[2].message
        )

    def test_build_docs_warnings_and_errors(self):
        return_code, annotations = action.build_docs(
                os.path.join(TEST_PROJECTS_DIR, 'warnings_and_errors')
        )
        self.assertNotEqual(return_code, 0)
        self.assertEqual(len(annotations), 1)

        self.assertTrue(annotations[0].path.endswith('index.rst'))
        self.assertEqual(annotations[0].start_line, 16)
        self.assertEqual(annotations[0].end_line, 16)
        self.assertIn(
            'Error in "code-block" directive', annotations[0].message
        )

    @mock.patch('sphinx_action.status_check.create_in_progress_status_check')
    @mock.patch('sphinx_action.status_check.update_status_check')
    def test_build_all_docs_success(self, update_mock, create_mock):
        create_mock.return_value = 42

        action.build_all_docs(
            action.GithubEnvironment(
                sha='sha1hash', repo='ammaraskar/sphinx-action',
                token='SecretToken1'
            ),
            [os.path.join(TEST_PROJECTS_DIR, 'no_errors'),
             os.path.join(TEST_PROJECTS_DIR, 'warnings')]
        )

        create_mock.assert_called_once_with(
            'SecretToken1', 'sha1hash', 'ammaraskar/sphinx-action')

        self.assertEqual(len(update_mock.call_args_list), 3)
        self.assertEqual(update_mock.call_args_list[0][0][0], 42)
        self.assertEqual(update_mock.call_args_list[1][0][0], 42)
        self.assertEqual(update_mock.call_args_list[2][0][0], 42)

        update_mock.assert_any_call(
            42, 'SecretToken1', 'ammaraskar/sphinx-action',
            status_check.CheckOutput(
                title='Sphinx Documentation Build',
                summary='Build succeeded with 3 warnings',
                annotations=[]
            ),
            conclusion='success'
        )

    @mock.patch('sphinx_action.status_check.create_in_progress_status_check')
    @mock.patch('sphinx_action.status_check.update_status_check')
    def test_build_all_docs_some_success(self, update_mock, create_mock):
        create_mock.return_value = 41

        with self.assertRaisesRegex(RuntimeError, 'Build failed'):
            action.build_all_docs(
                action.GithubEnvironment(
                    sha='sha1hash', repo='ammaraskar/sphinx-action',
                    token='SecretToken1'
                ),
                [os.path.join(TEST_PROJECTS_DIR, 'no_errors'),
                 os.path.join(TEST_PROJECTS_DIR, 'warnings_and_errors')]
            )

        create_mock.assert_called_once_with(
            'SecretToken1', 'sha1hash', 'ammaraskar/sphinx-action')

        self.assertEqual(len(update_mock.call_args_list), 3)
        self.assertEqual(update_mock.call_args_list[0][0][0], 41)
        self.assertEqual(update_mock.call_args_list[1][0][0], 41)
        self.assertEqual(update_mock.call_args_list[2][0][0], 41)

        update_mock.assert_any_call(
            41, 'SecretToken1', 'ammaraskar/sphinx-action',
            status_check.CheckOutput(
                title='Sphinx Documentation Build',
                summary='Build failed with 1 warnings',
                annotations=[]
            ),
            conclusion='failure'
        )


if __name__ == '__main__':
    unittest.main()
