from python:alpine3.18
LABEL key="LegalAssitr"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt
RUN apk del .temp-build-deps
RUN mkdir /app
WORKDIR /app

COPY ./legalassitr /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/web
RUN chmod -R 755 /vol/web
USER user

EXPOSE 8000

# Run Django migrations
CMD ["python", "manage.py", "migrate"]

# Start Gunicorn process
CMD ["gunicorn", "legalassitr.wsgi:application", "--bind", "0.0.0.0:8000"]

# Start celery worker
CMD ["celery", "-A", "legalassitr", "worker", "-l", "info"]

# start celery beat for periodic tasks
CMD ["celery", "-A", "legalassitr", "beat", "--detach"]
