FROM python:3.10.4-alpine3.16 AS build
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && apk add ffmpeg

WORKDIR /app
COPY ./app /app/
RUN pip install -r requirements.txt
RUN apk del .build-deps

FROM build AS dev
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=development

VOLUME ["/app"]
EXPOSE 5000
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]

FROM build AS prod
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 80
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]