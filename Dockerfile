FROM python:3.10.6-buster

RUN pip install dnspython pymongo Flask

RUN mkdir /opt/app

ENV MONGO_CONNECTION=mongodb://localhost:27017
ENV MONGO_DB_NAME=Shimon

WORKDIR /opt/app

COPY *.py /opt/app/
COPY README.md /opt/app/

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0" ]