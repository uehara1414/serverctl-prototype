FROM python:3.6
RUN mkdir /code
WORKDIR /code

RUN apt-get update -y  &&  apt-get install --fix-missing
RUN DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y python python-yaml sudo curl gcc python-pip python-dev libffi-dev libssl-dev
RUN apt-get -y --purge remove python-cffi
RUN pip install --upgrade cffi
RUN pip install ansible

# AWS settings
ADD .aws /root/.aws/

# SSH settings
ADD .ssh /root/.ssh/

ADD requirements.txt /code/
RUN pip install -r requirements.txt
