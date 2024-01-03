import os
import yt_dlp
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
FILENAME = ""
PARAMS = {'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '/static/%(title)s.mp3'}

@app.route("/", methods=["GET", "POST"])
def download_page():
    global session, FILENAME
    if request.method == "POST":
        try:
            video = yt_dlp.YoutubeDL(PARAMS)
        except Exception as e:
            return render_template("download.html",
                                   show_download=False,
                                   error_message="You entered invalid link")
        
        try:
            video.download(request.form['link'])
        except Exception as e:
            return render_template("download.html",
                                   show_download=False,
                                   error_message=f"{e}")
        
        FILENAME = f"static/{video.extract_info(request.form['link'], download=False).get('title', None)}.mp3"
        return render_template("download.html",
                               show_download=True,
                               filename=FILENAME,
                               title=FILENAME.strip(".mp3").strip("static/"))
    return render_template("download.html",
                           show_download=False)


@app.route("/delete")
def delete_file():
    os.remove(FILENAME)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
