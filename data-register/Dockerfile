FROM python:3.8-slim
LABEL maintainer="dmozh58@gmail.com"

COPY . ./

RUN apt-get -y upgrade && apt-get -y update
#RUN apt-get -y add bind-tools
#RUN apt-get -y install ggc

RUN pip3 install -U pip
RUN pip3 install -r requirements.txt
WORKDIR ./src
CMD ["python3", "__main__.py"]