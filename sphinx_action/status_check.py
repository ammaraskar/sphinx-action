"""
This module interacts with the Github Actions API to create in-line warnings
and errors.
"""
import collections
import sys


class AnnotationLevel:
    # Notices are not currently supported.
    # NOTICE = "notice"
    WARNING = "warning"
    FAILURE = "failure"


CheckAnnotation = collections.namedtuple(
    "CheckAnnotation", ["path", "start_line", "end_line", "annotation_level", "message"]
)


def output_annotation(annotation, where_to_print=sys.stdout):
    level_to_command = {
        AnnotationLevel.WARNING: "warning",
        AnnotationLevel.FAILURE: "error",
    }

    command = level_to_command[annotation.annotation_level]

    print(
        "::{command} file={file},line={line}::{message}".format(
            command=command,
            file=annotation.path,
            line=annotation.start_line,
            message=annotation.message,
        ),
        file=where_to_print,
    )
