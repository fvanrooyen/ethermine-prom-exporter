FROM jfloff/alpine-python:2.7-slim

WORKDIR /usr/local/bin

RUN pip install prometheus_client requests
ADD ethermine-export.py .
ADD entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]