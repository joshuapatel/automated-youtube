FROM python:3.10.4-alpine AS callback-prod

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY ./app/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./app .

VOLUME ["/yt-media"]
EXPOSE 80
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]

FROM callback-prod AS callback-dev

ENV FLASK_ENV=development

VOLUME ["/app"]
EXPOSE 5000
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]

FROM alpine:latest AS yt-build

# inspired by https://github.com/tnk4on/yt-dlp/blob/main/Containerfile.d/Containerfile.alpine-static

ENV YTDLP_VERSION=2022.08.19
ENV FFMPEG_VERSION=5.0.1

WORKDIR /build
# yt-dlp source (https://github.com/yt-dlp/yt-dlp)
# "yt-dlp"
RUN wget https://github.com/yt-dlp/yt-dlp/releases/download/${YTDLP_VERSION}/SHA2-256SUMS \
    && SHA256_SUM=`grep 'yt-dlp$' SHA2-256SUMS` \
    && wget https://github.com/yt-dlp/yt-dlp/releases/download/${YTDLP_VERSION}/yt-dlp \
    && echo "${SHA256_SUM}" | sha256sum -c

# ffmpeg static source (https://johnvansickle.com/ffmpeg/)
# "ffmpeg"
RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    && wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz.md5 \
    && md5sum -c ffmpeg-release-amd64-static.tar.xz.md5 \
    && tar Jxf ffmpeg-release-amd64-static.tar.xz

RUN mv ffmpeg-${FFMPEG_VERSION}-amd64-static/ffmpeg ffmpeg

FROM callback-prod AS callback-yt-prod

COPY --from=yt-build /build/yt-dlp /usr/local/bin/yt-dlp
COPY --from=yt-build /build/ffmpeg /usr/local/bin/ffmpeg
RUN chmod 755 /usr/local/bin/yt-dlp

FROM callback-dev AS callback-yt-dev

COPY --from=yt-build /build/yt-dlp /usr/local/bin/yt-dlp
COPY --from=yt-build /build/ffmpeg /usr/local/bin/ffmpeg
RUN chmod 755 /usr/local/bin/yt-dlp