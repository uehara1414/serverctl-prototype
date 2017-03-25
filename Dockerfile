FROM python:3.6
RUN mkdir /code
WORKDIR /code

# AWS settings
ADD .aws /root/.aws/

ADD requirements.txt /code/
RUN pip install -r requirements.txt
