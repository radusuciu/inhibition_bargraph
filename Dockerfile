FROM python:3.7.0-stretch

MAINTAINER Radu Suciu <radusuciu@gmail.com>

# Create user with non-root privileges
RUN adduser --disabled-password --gecos '' bar
RUN chown -R bar /home/bar

# install some deps
RUN apt-get update && apt-get -y install \
    fonts-liberation

USER bar
WORKDIR /home/bar/bar
CMD [ "/bin/bash", "/home/bar/bar/start.sh" ]
