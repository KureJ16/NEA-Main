from flask import Blueprint, render_template

views = Blueprint(__name__, "views")

@views.route("/home")
def home():
    return render_template("HomePage.html")

@views.route("/mood_analysis")
def moodAnalysis():
    return render_template(("MoodAnalysis.html"))

@views.route("/data_analysis")
def dataAnalysis():
    return render_template(("DataAnalysis.html"))

@views.route("/song_mood")
def songMood():
    return render_template(("SongMood.html"))