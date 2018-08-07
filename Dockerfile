FROM docker.marqeta.com/mq/alp-py36-min:latest

EXPOSE 6000

ADD app /srv/app
ADD instance /srv/instance
ADD requirements.txt uwsgi.ini run.py /srv/

WORKDIR /srv

RUN apk add -u --no-cache --virtual .build-deps gcc python3-dev build-base linux-headers && \
    python3.6 -m venv /srv/venv && source /srv/venv/bin/activate && \
    pip install -r requirements.txt && \
    apk del .build-deps

CMD ["/srv/venv/bin/uwsgi", "--ini", "/srv/uwsgi.ini"]
