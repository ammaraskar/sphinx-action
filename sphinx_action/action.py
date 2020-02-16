import collections
import subprocess
import tempfile
import os
import shlex

from sphinx_action import status_check


GithubEnvironment = collections.namedtuple("GithubEnvironment", ["build_command"])


def extract_line_information(line_information):
    r"""Lines from sphinx log files look like this

        C:\Users\ammar\workspace\sphinx-action\tests\test_projects\warnings\index.rst:22: WARNING: Problems with "include" directive path:
        InputError: [Errno 2] No such file or directory: 'I_DONT_EXIST'.

        /home/users/ammar/workspace/sphix-action/tests/test_projects/warnings/index.rst:22: WARNING: Problems with "include" directive path:
        InputError: [Errno 2] No such file or directory: 'I_DONT_EXIST'.

        /home/users/ammar/workspace/sphix-action/tests/test_projects/warnings/index.rst: Something went wrong with this whole ifle

    This method is responsible for parsing out the line number and file name from these lines.
    """
    file_and_line = line_information.split(":")
    # This is a dirty windows specific hack to deal with drive letters in the
    # start of the file-path, i.e D:\
    if len(file_and_line[0]) == 1:
        # If the first component is just one letter, we did an accidental split
        file_and_line[1] = file_and_line[0] + ":" + file_and_line[1]
        # Join the first component back up with the second and discard it.
        file_and_line = file_and_line[1:]

    if len(file_and_line) != 2 and len(file_and_line) != 3:
        return None
    # The case where we have no line number, in this case we return the line
    # number as 1 to mark the whole file.
    if len(file_and_line) == 2:
        line_num = 1
    if len(file_and_line) == 3:
        try:
            line_num = int(file_and_line[1])
        except ValueError:
            return None

    file_name = os.path.relpath(file_and_line[0])
    return file_name, line_num


def parse_sphinx_warnings_log(logs):
    """Parses a sphinx file containing warnings and errors into a list of
    status_check.CheckAnnotation objects.

    Inputs look like this:
/media/sf_shared/workspace/sphinx-action/tests/test_projects/warnings_and_errors/index.rst:19: WARNING: Error in "code-block" directive:
maximum 1 argument(s) allowed, 2 supplied.

/cpython/Doc/distutils/_setuptools_disclaimer.rst: WARNING: document isn't included in any toctree
/cpython/Doc/contents.rst:5: WARNING: toctree contains reference to nonexisting document 'ayylmao'
    """
    annotations = []

    for i, line in enumerate(logs):
        if "WARNING" not in line:
            continue

        warning_tokens = line.split("WARNING:")
        if len(warning_tokens) != 2:
            continue
        file_and_line, message = warning_tokens

        file_and_line = extract_line_information(file_and_line)
        if not file_and_line:
            continue
        file_name, line_number = file_and_line

        warning_message = message
        # If this isn't the last line and the next line isn't a warning,
        # treat it as part of this warning message.
        if (i != len(logs) - 1) and "WARNING" not in logs[i + 1]:
            warning_message += logs[i + 1]
        warning_message = warning_message.strip()

        annotations.append(
            status_check.CheckAnnotation(
                path=file_name,
                message=warning_message,
                start_line=line_number,
                end_line=line_number,
                annotation_level=status_check.AnnotationLevel.WARNING,
            )
        )

    return annotations


def build_docs(build_command, docs_directory):
    if not build_command:
        raise ValueError("Build command may not be empty")

    docs_requirements = os.path.join(docs_directory, "requirements.txt")
    if os.path.exists(docs_requirements):
        subprocess.check_call(["pip", "install", "-r", docs_requirements])

    log_file = os.path.join(tempfile.gettempdir(), "sphinx-log")
    if os.path.exists(log_file):
        os.unlink(log_file)

    sphinx_options = '--keep-going --no-color -w "{}"'.format(log_file)
    # If we're using make, pass the options as part of the SPHINXOPTS
    # environment variable, otherwise pass them straight into the command.
    build_command = shlex.split(build_command)
    if build_command[0] == "make":
        # Pass the -e option into `make`, this is specified to be
        #   Cause environment variables, including those with null values, to override macro assignments within makefiles.
        # which is exactly what we want.
        build_command += ["-e"]
        print("[sphinx-action] Running: {}".format(build_command))

        return_code = subprocess.call(
            build_command,
            env=dict(os.environ, SPHINXOPTS=sphinx_options),
            cwd=docs_directory,
        )
    else:
        build_command += shlex.split(sphinx_options)
        print("[sphinx-action] Running: {}".format(build_command))

        return_code = subprocess.call(
            build_command + shlex.split(sphinx_options), cwd=docs_directory
        )

    with open(log_file, "r") as f:
        annotations = parse_sphinx_warnings_log(f.readlines())

    return return_code, annotations


def build_all_docs(github_env, docs_directories):
    if len(docs_directories) == 0:
        raise ValueError("Please provide at least one docs directory to build")

    build_success = True
    warnings = 0

    for docs_dir in docs_directories:
        print("====================================")
        print("Building docs in {}".format(docs_dir))
        print("====================================")

        return_code, annotations = build_docs(github_env.build_command, docs_dir)
        if return_code != 0:
            build_success = False

        warnings += len(annotations)

        for annotation in annotations:
            status_check.output_annotation(annotation)

    status_message = "[sphinx-action] Build {} with {} warnings".format(
        "succeeded" if build_success else "failed", warnings
    )
    print(status_message)

    if not build_success:
        raise RuntimeError("Build failed")
