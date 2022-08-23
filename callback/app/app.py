import subprocess
from os import environ

import xmltodict
from flask import Flask, jsonify, request
from flask.wrappers import Response
from pyexpat import ExpatError
from werkzeug.exceptions import BadRequest, HTTPException

app = Flask(__name__)

def verify_subscription(req, token: str) -> Response:
    if req.args.get("hub.mode") in ["subscribe", "unsubscribe"]:
        if req.args.get("hub.verify_token") == token:
            if req.args.get("hub.challenge"):
                return req.args.get("hub.challenge")
            else:
                raise BadRequest("Missing challenge")
        else:
            raise BadRequest("Invalid token")
    else:
        raise BadRequest("Invalid mode")

@app.route("/callback/audio-youtube", methods=["GET", "POST"]) 
def audio_youtube() -> Response:
    if request.method == "GET":
        return verify_subscription(request, environ.get("AUDIO_YOUTUBE_TOKEN", default="none specified"))

    try:
        data = xmltodict.parse(request.data)
    except ExpatError:
        raise BadRequest("XML data could not be parsed")

    try:
        video_id = data["feed"]["entry"]["yt:videoId"]
        if not len(video_id) == 11:
            raise BadRequest("Invalid video ID")
    except KeyError:
        raise BadRequest("XML data is missing required fields")

    subprocess.Popen(["yt-dlp", "--write-thumbnail", "--write-info-json",
    "-x", "--audio-format", "flac", "--audio-quality", "0",
    "--output", "/yt-media/%(title)s [%(id)s].%(ext)s", "https://www.youtube.com/watch?v=" + video_id])

    return Response(status=204)

@app.errorhandler(HTTPException)
def handle_http_exceptions(error):
    return jsonify({
        "code": error.code,
        "name": error.name,
        "error": error.description
    }), error.code

@app.errorhandler(Exception)
def handle_internal_exceptions(error: Exception):
    if isinstance(error, HTTPException):
        return error

    return jsonify({
        "code": 500,
        "name": "Internal Server Error",
        "error": "An internal server error has occurred"
    }), 500