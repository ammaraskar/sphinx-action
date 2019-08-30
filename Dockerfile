FROM python:3-slim

LABEL "com.github.actions.name"="Sphinx Build"
LABEL "com.github.actions.description"="Builds documentation using Sphinx"
LABEL "com.github.actions.icon"="book"
LABEL "com.github.actions.color"="blue"

LABEL "maintainer"="Ammar Askar <ammar@ammaraskar.com>"

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD entrypoint.py /entrypoint.py
ADD sphinx_action /sphinx_action

ENTRYPOINT ["/entrypoint.py"]