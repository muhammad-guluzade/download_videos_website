from pytube import YouTube
from flask import Flask, request, redirect, render_template

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def download_page():
    if request.method == "POST":
        video = YouTube(request.form['link'])
        stream = video.streams.filter(only_audio=True).first()
        stream.download(filename=f"{video.title}.mp3")
        return redirect("/")
    return render_template("download.html")


if __name__ == "__main__":
    app.run(debug=True)
