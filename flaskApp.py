from flask import Flask, render_template, request, redirect
import os

from flask_frozen import Freezer

template_directory = os.getcwd()
navigation_sections = ['Home', 'Projects', 'About', 'Contact']



app = Flask(__name__, template_folder=template_directory)

#app.config['STATIC_FOLDER'] = template_directory

freezer = Freezer(app)

@app.route("/")
@app.route("/home.html")
def home():
    return render_template('home.html', navigation=navigation_sections, crumb="home", mimetype='text/html')

@app.route("/projects.html")
def projects():
    return render_template('projects.html', navigation=navigation_sections, crumb="projects", mimetype='text/html')

@app.route("/projects/<path:subpath>/")
def show_project(subpath):
	# show the subpath after /path/
    return render_template('projects.html', navigation=navigation_sections, crumb="projects", mimetype='text/html')

@app.route("/about.html")
def about():
	
	return render_template('about.html', navigation=navigation_sections, crumb="about", mimetype='text/html')

@app.route("/contact.html")
def contact():
	return render_template('about.html', navigation=navigation_sections, crumb="contact", mimetype='text/html')
	
freezer.freeze()

if __name__ == '__main__':
    freezer.freeze()
