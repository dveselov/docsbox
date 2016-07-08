FROM ubuntu:16.04
MAINTAINER Dmitry Veselov <d.a.veselov@yandex.ru>

ADD . /docsbox
WORKDIR /docsbox
ENV LC_ALL C.UTF-8 # required by click
ENV LANG C.UTF-8
RUN apt-get update && apt-get upgrade
RUN apt-get install python3-dev libffi-dev libmagic-dev libreoffice libreofficekit-dev 
RUN python3-pip && pip3 install virtualenv
RUN virtualenv -p python3.5 env
RUN ./env/bin/activate
RUN pip install -r requirements.txt
CMD python wsgi.py
