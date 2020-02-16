from io import StringIO
import unittest

from sphinx_action import status_check


class TestStatusChecks(unittest.TestCase):
    def test_output_for_warning(self):
        output_file = StringIO()

        annotation = status_check.CheckAnnotation(
            path="index.rst",
            start_line=1,
            end_line=20,
            annotation_level=status_check.AnnotationLevel.WARNING,
            message="This is a test warning message",
        )
        status_check.output_annotation(annotation, where_to_print=output_file)

        output_str = output_file.getvalue()
        self.assertEqual(
            output_str,
            "::warning file=index.rst,line=1::This is a test warning message\n",
        )

    def test_output_for_error(self):
        output_file = StringIO()

        annotation = status_check.CheckAnnotation(
            path="index.rst",
            start_line=15,
            end_line=20,
            annotation_level=status_check.AnnotationLevel.FAILURE,
            message="This is a test error message",
        )
        status_check.output_annotation(annotation, where_to_print=output_file)

        output_str = output_file.getvalue()
        self.assertEqual(
            output_str,
            "::error file=index.rst,line=15::This is a test error message\n",
        )


if __name__ == "__main__":
    unittest.main()
