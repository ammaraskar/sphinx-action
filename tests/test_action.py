import os
import unittest
from sphinx_action import action


TEST_PROJECTS_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'test_projects'
)


class TestAction(unittest.TestCase):

    def test_build_docs_with_no_docs_directories(self):
        """Make sure we bail out if they don't provide a single documentation
        directory"""
        with self.assertRaises(ValueError):
            action.build_all_docs(None, [])

    def test_build_docs_no_errors_or_warnings(self):
        """Check that we correctly build docs when there's no errors or
        warnings"""
        pass


if __name__ == '__main__':
    unittest.main()
