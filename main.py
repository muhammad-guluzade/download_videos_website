import os
import pytube
from pytube import YouTube
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
FILENAME = ""

@app.route("/", methods=["GET", "POST"])
def download_page():
    global FILENAME
    try:
        
        if request.method == "POST":
            try:
                video = YouTube(request.form['link'],
                                use_oauth=True,
                                allow_oauth_cache=True)
            except pytube.exceptions.RegexMatchError as e:
                return render_template("download.html",
                                       show_download=False,
                                       error_message=e)
    
            try:
                stream = video.streams.filter(only_audio=True).first()
                stream_mp4_720 = video.streams.filter(mime_type="video/mp4", res="720p").first()
                stream_mp4_360 = video.streams.filter(mime_type="video/mp4", res="360p").first()
                
            except pytube.exceptions.VideoUnavailable as e:
                return render_template("download.html",
                                       show_download=False,
                                       error_message=e)
            title = video.title.replace('/', '|').replace('\\', '|')
            FILENAME = f"static/{title}.mp3"
            FILENAME_360 = f"static/{title}360.mp4"
            FILENAME_720 = f"static/{title}720.mp4"
            stream.download(filename=FILENAME)

            if stream_mp4_360:
                stream_mp4_360.download(filename=FILENAME_360)

            if stream_mp4_720:
                stream_mp4_720.download(filename=FILENAME_720)

            return render_template("download.html",
                                   show_download=True,
                                   filename=FILENAME,
                                   title=title,
                                   video_360=stream_mp4_360,
                                   video_720=stream_mp4_720,
                                   filename_360=FILENAME_360,
                                   filename_720=FILENAME_720)
        return render_template("download.html",
                               show_download=False)
    except Exception as e:
        return render_template("download.html",
                                       show_download=False,
                                       error_message=f"{e}")


if __name__ == "__main__":
    app.run(debug=True)
