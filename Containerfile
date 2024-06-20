FROM sphinxdoc/sphinx:latest

LABEL "maintainer"="Freya Gustavsson <freya@venefilyn.se>"

RUN pip install --upgrade pip

ADD entrypoint.py /entrypoint.py
ADD sphinx_action /sphinx_action

ENTRYPOINT ["/entrypoint.py"]
