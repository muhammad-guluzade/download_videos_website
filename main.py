import os
import yt_dlp
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
FILENAME = ""
PARAMS = {'extract_audio': True, 'format': 'bestaudio', "outtmpl": "static/video.mp3"}

@app.route("/", methods=["GET", "POST"])
def download_page():
    global session, FILENAME
    if request.method == "POST":
        try:
            video = yt_dlp.YoutubeDL(PARAMS)
            video.download(request.form['link'])
        except Exception:
            return render_template("download.html",
                                   show_download=False,
                                   error_message=f"You entered invalid url.")
    
        FILENAME = f"static/video.mp3"

        return render_template("download.html",
                               show_download=True,
                               filename=FILENAME,
                               title=video.extract_info(request.form['link']).get('title'))
    return render_template("download.html",
                           show_download=False)


@app.route("/delete")
def delete_file():
    os.remove(FILENAME)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
