from flask import Flask, render_template, request, redirect
import os

import sys

from flask_frozen import Freezer

template_directory = os.getcwd()
navigation_sections = ['Home', 'Projects', 'About', 'Contact']

noProjectDescriptionDefaultMessage = "No description available"


app = Flask(__name__, template_folder=template_directory)

#app.config['STATIC_FOLDER'] = template_directory

freezer = Freezer(app)

@app.route("/")
@app.route("/home.html")
def home():
    return render_template('home.html', navigation=navigation_sections, crumb="home", mimetype='text/html')

@app.route("/projects.html")
def projects():

	allProjects = []

	allDescriptors = {}

	mediaPool = {}

	for projectName in os.listdir('static/publicProjects'):

		if not (projectName.startswith('.')): #Don't put hidden folders.
			allProjects.append(projectName)

			try:
				with open('static/publicProjects/' + projectName + '/' + 'project.oneliner') as f:
					
					if not f:
						continue;
					
					for line in f:
						#print(line, file=sys.stdout)
						#(k, v) = line.split("=")
						allDescriptors[projectName] = line

					#print(f, file=sys.stdout)

			except OSError as e:
				allDescriptors[projectName] = noProjectDescriptionDefaultMessage


			try: #need seperate phases here otherwise I'd wrap into one try / except
				if len(os.listdir('static/publicProjects/' + projectName + '/' + 'media/')) > 0:
					mediaPool[projectName] = os.listdir('static/publicProjects/' + projectName + '/' + 'media/')
				else:
					mediaPool[projectName] = ""
			except OSError as e:
				mediaPool[projectName] = ""
			


		else:
			continue



	return render_template('projects.html', navigation=navigation_sections, crumb="projects", mimetype='text/html', availableProjects=sorted(allProjects), descriptors=allDescriptors, mediaPool=mediaPool)



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
