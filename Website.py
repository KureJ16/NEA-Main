from flask import Flask, request, render_template
from Routes import views
from MachineLearning import LearnFromData
import math

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

@app.route("/song_mood", methods=["POST"])
def getValue():
    songName = request.form["fname"]
    songArtist = request.form["lname"]
    sad_happy_test = LearnFromData("sad_song_stats.csv", "happy_song_stats.csv", "sadness")
    score, feeling = sad_happy_test.naiveBayesTest(songName, songArtist)
    if feeling == "happy":
        score = 100-round(score[0]*100,1)
    else:
        score = round(score[0]*100,1)
    return render_template("SongMood.html", sn=songName, sa=songArtist, s=score, f=feeling)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
