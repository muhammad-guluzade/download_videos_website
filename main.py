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
                video = YouTube(request.form['link'])
            except pytube.exceptions.RegexMatchError:
                return render_template("download.html",
                                       show_download=False,
                                       error_message="You entered invalid link")
    
            try:
                stream = video.streams.filter(only_audio=True).first()
            except pytube.exceptions.VideoUnavailable:
                return render_template("download.html",
                                       show_download=False,
                                       error_message="You entered invalid link")
    
            FILENAME = f"static/{video.title}.mp3"
            stream.download(filename=FILENAME)
            return render_template("download.html",
                                   show_download=True,
                                   filename=FILENAME,
                                   title=FILENAME.strip(".mp3").strip("static/"))
        return render_template("download.html",
                               show_download=False)
    except Exception as e:
        return render_template("download.html",
                                       show_download=False,
                                       error_message=f"{e}")


@app.route("/delete")
def delete_file():
    os.remove(FILENAME)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
