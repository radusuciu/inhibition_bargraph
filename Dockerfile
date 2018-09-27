FROM python:3.7.0-slim-stretch

MAINTAINER Radu Suciu <radusuciu@gmail.com>

RUN adduser --disabled-password --gecos '' bar
RUN chown -R bar /home/bar
RUN pip install pipenv

USER bar
WORKDIR /home/bar/bar
CMD [ "/bin/bash", "/home/bar/bar/start.sh" ]