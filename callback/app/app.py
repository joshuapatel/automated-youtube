from flask import Flask, request
from flask.wrappers import Response
import xmltodict
import subprocess

app = Flask(__name__)

@app.route("/callback/audio-youtube", methods=["POST"]) 
def audio_youtube():
    try:
        data = xmltodict.parse(request.data)
        video_id = data["feed"]["entry"]["yt:videoId"]
    except:
        return "error", 400
    subprocess.Popen(["yt-dlp", "--embed-thumbnail", "--embed-metadata", "-x", "--audio-format", "flac", "--audio-quality", "0", "--output", "/yt-media/%(title)s.%(ext)s", "https://www.youtube.com/watch?v=" + video_id])
    return Response(status=204)