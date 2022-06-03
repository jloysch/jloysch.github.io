from flask import Flask, render_template
import os

template_directory = os.getcwd()

navigation_sections = ['Home', 'Projects', 'About']

app = Flask(__name__, template_folder=template_directory)

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return render_template('home.html', navigation=navigation_sections, crumb="home")

@app.route("/projects")
def projects():
    return render_template('projects.html', navigation=navigation_sections, crumb="projects")


@app.route("/projects/<path:subpath>")
def show_project(subpath):
	# show the subpath after /path/
    return render_template('projects.html', navigation=navigation_sections, crumb="projects")

@app.route("/about")
def show_about():
	return render_template('about.html', navigation=navigation_sections, crumb="about")
