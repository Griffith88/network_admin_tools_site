FROM python:3.9-buster
# set work directory
WORKDIR /usr/src/adminsite/

COPY ./openssl.cnf /etc/ssl/openssl.cnf
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && apt-get install -y gcc unixodbc-dev
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/adminsite/requirements.txt
RUN pip install -r /usr/src/adminsite/requirements.txt

COPY . /usr/src/adminsite/

RUN ["chmod", "+x", "/usr/src/adminsite/entrypoint.sh"]

ENTRYPOINT ["sh", "/usr/src/adminsite/entrypoint.sh"]