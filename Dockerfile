FROM python:3-slim

LABEL "maintainer"="Ammar Askar <ammar@ammaraskar.com>"

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD entrypoint.py /entrypoint.py
ADD sphinx_action /sphinx_action

ENTRYPOINT ["/entrypoint.py"]