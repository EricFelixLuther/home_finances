FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY home_finances/ /code/
RUN mkdir /var/log/home_finances
COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN ["chmod", "+x", "/entrypoint.sh"]
ENTRYPOINT ["/entrypoint.sh"]