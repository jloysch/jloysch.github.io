'''

	'flaskApp.py' 

	Copyright 2022, Joshua Loysch, All rights reserved.

	The code behind the dynamic -> static generation of my portfolio page

'''

from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
import sys
import shutil
from jinja2 import Template

from flask_frozen import Freezer

template_directory = os.getcwd()
navigation_sections = ['Home', 'Projects', 'About', 'Blog', 'Contact']

noProjectDescriptionDefaultMessage = "No description available"

projectShowcaseFolder = "media/showcase/" #relative
projectGalleryFolder = "media/gallery/" #relative
projectManifestPath = "project.manifest" #relative (in root)
projectFolder = "static/projects/" 

projectDescriptionFile = "project.oneliner"


blogFilesFolder = "media/" #relative
blogFolder = "static/blog/" #relative
blogGalleryFolder = "media/gallery/" #relative
blogManifestPath = "blog.manifest" #relative should change to filename
blogGalleryShowcaseFolder = "media/showcase/"
blogDescriptionFile = "blog.oneliner"

buildFolder = "docs"

app = Flask(__name__, template_folder=template_directory)
app.config['FREEZER_DESTINATION'] = buildFolder
app.config['SECRET_KEY'] = 'someCrazySecrets'  

#app.config['STATIC_FOLDER'] = template_directory


freezer = Freezer(app)

pageHideHeaders = False


@app.route("/")
@app.route("/index")
@app.route("/index.html")
def home():

	projectsHTML=generateProjectShowcaseModule()

	return render_template('index.html', navigation=navigation_sections, crumb="home", mimetype='text/html', testHTML=projectsHTML)


@app.route("/blog")
@app.route("/blog.html")
def blog():

	allBlogs = []

	allDescriptors = {}

	mediaPool = {}

	hrefs = {}


	try:

		for blogName in os.listdir(blogFolder): 

			if  (not blogName.startswith('.') and not blogName.startswith('_')): #Don't put hidden folders.

				allBlogs.append(blogName)

				hrefs[blogName] = '/blog/' + blogName
				'''
				try:

					with open(projectFolder + projectName + '/' + projectDescriptionFile) as f:
						
						if not f:
							continue;
						
						for line in f:
							#print(line, file=sys.stdout)
							#(k, v) = line.split("=")
							allDescriptors[projectName] = line

						#print(f, file=sys.stdout)

				except OSError as e:
					allDescriptors[projectName] = noProjectDescriptionDefaultMessage
				'''

				
				loadedMfst = loadBlogManifest(blogName)

				if not loadedMfst[1]:
					allDescriptors[blogName] = loadBlogManifest(blogName)[0]['shortDescription']
				else:
					allDescriptors[blogName] = "" #TODO CHANGE THIS BLOG SHOULDNT HAVE DESC
					pass

				try: #need seperate phases here otherwise I'd wrap into one try / except
					if len(os.listdir(blogFolder + blogName + '/' + blogGalleryFolder)) > 0: 

						mediaPoolForThisBlog = []

						for imageName in os.listdir(blogFolder + blogName + '/' + blogGalleryFolder):
							if (not imageName.startswith('.') and not imageName.startswith('_')):
								mediaPoolForThisBlog.append(blogFolder + blogName + '/' + blogGalleryFolder + imageName)
								#print(imageName + " added to pool for " + projectName)

						#for x in mediaPoolForThisProject:
							#print(x, file=sys.stdout)	
						#mediaPool[projectName] = os.listdir('static/publicProjects/' + projectName + '/' + 'media/')

						mediaPool[blogName] = mediaPoolForThisBlog

					else:
						mediaPool[blogName] = ""
						#print("No media files to showcase for '" + projectName + "'")

				except OSError as e:
					mediaPool[blogName] = ""
					#print(e, file=sys.stdout)
			else:
				continue
	except:
		pass

	return render_template('blog.html', navigation=navigation_sections, crumb="blog", mimetype='text/html', blogs=sorted(allBlogs), descriptors=allDescriptors, mediaPool=mediaPool, hideNav=False, hrefs=hrefs)
	
def loadProjectManifest(pfolder):
	
	projectManifest = {}
	dictEmpty = True

	try:
		projectManifest = (json.load(open(projectFolder + pfolder + '/' + projectManifestPath)))
		#print(projectManifest, file=sys.stderr)
		dictEmpty = False
	except OSError as e:
		print(e, file=sys.stderr)
		#print("COULDNT OPEN PROJECT MANIFEST!!!!!!", file=sys.stderr)
		pass

	#print(projectManifest, file=sys.stdout, flush=True)

	return [projectManifest, dictEmpty]

def loadBlogManifest(bfolder):
	
	blogManifest = {}
	dictEmpty = True

	try:
		blogManifest = (json.load(open(blogFolder + bfolder + '/' + blogManifestPath)))
		#print(projectManifest, file=sys.stderr)
		dictEmpty = False
	except OSError as e:
		print(e, file=sys.stderr)
		#print("COULDNT OPEN PROJECT MANIFEST!!!!!!", file=sys.stderr)
		pass

	#print(projectManifest, file=sys.stdout, flush=True)

	return [blogManifest, dictEmpty]

@app.route("/projects.html")
def projects():

	allProjects = []

	allDescriptors = {}

	mediaPool = {}

	hrefs = {}


	try:

		for projectName in os.listdir(projectFolder): 

			if  (not projectName.startswith('.') and not projectName.startswith('_')): #Don't put hidden folders.

				allProjects.append(projectName)

				hrefs[projectName] = '/projects/' + projectName
				'''
				try:

					with open(projectFolder + projectName + '/' + projectDescriptionFile) as f:
						
						if not f:
							continue;
						
						for line in f:
							#print(line, file=sys.stdout)
							#(k, v) = line.split("=")
							allDescriptors[projectName] = line

						#print(f, file=sys.stdout)

				except OSError as e:
					allDescriptors[projectName] = noProjectDescriptionDefaultMessage
				'''

				
				loadedMfst = loadProjectManifest(projectName)

				if not loadedMfst[1]:
					allDescriptors[projectName] = loadProjectManifest(projectName)[0]['shortDescription']
				else:
					allDescriptors[projectName] = noProjectDescriptionDefaultMessage
					pass

				try: #need seperate phases here otherwise I'd wrap into one try / except
					if len(os.listdir(projectFolder + projectName + '/' + projectGalleryFolder)) > 0: 

						mediaPoolForThisProject = []

						for imageName in os.listdir(projectFolder + projectName + '/' + projectGalleryFolder):
							if (not imageName.startswith('.') and not imageName.startswith('_')):
								mediaPoolForThisProject.append(projectFolder + projectName + '/' + projectGalleryFolder + imageName)
								#print(imageName + " added to pool for " + projectName)

						#for x in mediaPoolForThisProject:
							#print(x, file=sys.stdout)	
						#mediaPool[projectName] = os.listdir('static/publicProjects/' + projectName + '/' + 'media/')

						mediaPool[projectName] = mediaPoolForThisProject

					else:
						mediaPool[projectName] = ""
						#print("No media files to showcase for '" + projectName + "'")

				except OSError as e:
					mediaPool[projectName] = ""
					#print(e, file=sys.stdout)
			else:
				continue
	except:
		pass

	return render_template('projects.html', navigation=navigation_sections, crumb="projects", mimetype='text/html', availableProjects=sorted(allProjects), descriptors=allDescriptors, mediaPool=mediaPool, hideNav=False, hrefs=hrefs)
	


def getProjectMediaDescriptions():

	allProjects = []

	allDescriptors = {}

	mediaPool = {}

	hrefs = {}

	try:

		for projectName in os.listdir(projectFolder): 

			if  (not projectName.startswith('.') and not projectName.startswith('_')): #Don't put hidden folders.

				allProjects.append(projectName)

				hrefs[projectName] = '/projects/' + projectName

				'''
				try:
					with open(projectFolder + projectName + '/' + projectDescriptionFile) as f:
						
						if not f:
							continue;
						
						for line in f:
							#print(line, file=sys.stdout)
							#(k, v) = line.split("=")
							allDescriptors[projectName] = line

						#print(f, file=sys.stdout)

				except OSError as e:
					allDescriptors[projectName] = noProjectDescriptionDefaultMessage
				'''


				loadedMfst = loadProjectManifest(projectName)

				if not loadedMfst[1]:
					allDescriptors[projectName] = loadProjectManifest(projectName)[0]['shortDescription']
				else:
					allDescriptors[projectName] = noProjectDescriptionDefaultMessage
					pass
				

				try: #need seperate phases here otherwise I'd wrap into one try / except, this generates the media pool for the gallery.
					if len(os.listdir(projectFolder + projectName + '/' + projectGalleryFolder)) > 0: 

						mediaPoolForThisProject = []

						for imageName in os.listdir(projectFolder + projectName + '/' + projectGalleryFolder):
							if (not imageName.startswith('.') and not imageName.startswith('_')):
								mediaPoolForThisProject.append(projectFolder + projectName + '/' + projectGalleryFolder + imageName)
								#print(imageName + " added to pool for " + projectName)

						#for x in mediaPoolForThisProject:
							#print(x, file=sys.stdout)	
						#mediaPool[projectName] = os.listdir('static/publicProjects/' + projectName + '/' + 'media/')

						mediaPool[projectName] = mediaPoolForThisProject

					else:
						mediaPool[projectName] = ""
						#print("No media files to showcase for '" + projectName + "'")

				except OSError as e:
					mediaPool[projectName] = ""
					#print(e, file=sys.stdout)
			else:
				continue
	except:
		pass

	return [allProjects, allDescriptors, mediaPool, hrefs]

def generateProjectShowcaseModule():
		
		showcasedProjects = []

		#TODO: MAKE SURE I GO BACK AND ADD A SHOWCASE FOLDER FOR THIS INSTEAD OF JUST POOLING ALL PROJECTS, THIS IS ONLY IN HERE TO GIVE MYSELF PERSPECTIVE ON HOW IT'LL LOOK!
		PACKAGED_INFO = getProjectMediaDescriptions()

		#print(PACKAGED_INFO[3], file=sys.stdout)

		return render_template('projectsModule.html', navigation=navigation_sections, crumb="projects", mimetype='text/html', availableProjects=sorted(PACKAGED_INFO[0]), descriptors=PACKAGED_INFO[1], mediaPool=PACKAGED_INFO[2], hideNav=True, hrefs=PACKAGED_INFO[3])


#@app.route("/static/projects/<path:subpath>/", methods=['GET', 'POST'])

@app.route('/projectspecs')
def projectspecs():

	
	return render_template('projectspecs.html', hasDocumentation = True)


def safeSubpath(sub):
	if (sub.lower() == "span encryption"): return "SPAN Encryption"
	return sub


#http://localhost:5000/projects/SPAN%20ENCRYPTION/download.html


@app.route("/projects/<path:subpath>/", methods=['GET', 'POST'])
@app.route("/projects/<path:subpath>/")

#@freezer.register_generator
def getProjectSpec(subpath):
	# show the subpath after /path/

	#try:
		#print("Attempting to open '" + projectFolder + subpath + "'", file=sys.stdout)

		#with open(projectFolder + subpath + "/") as f:
			
			#print("Attempting to open" + projectFolder + subpath, file=sys.stdout)

			#if not f:
				#print("No such directory when opened", file=sys.stdout)
			
			#return render_template('projects.html', navigation=navigation_sections, crumb="projects", mimetype='text/html', hideNav=False, requestedProject=subpath)

	#except OSError as e:

		#print( e, file=sys.stdout)

	#print("Sending 404..", file=sys.stdout)

	#return render_template('404.html', navigation=navigation_sections, crumb="projects", mimetype='text/html', hideNav=False, requestedProject=subpath)

	if (os.path.exists(projectFolder + subpath + "/")):

		showcase=None
		projectTitle=None
		projectDescription=None
		languagesUsed=None
		projectManifest = {}
		galleryDictEmpty = True
		gallery=[]

		try: 
			if len(os.listdir(projectFolder + subpath + '/' + projectShowcaseFolder)) > 0: 

				for imageName in os.listdir(projectFolder + subpath + '/' + projectShowcaseFolder): #Should only be one there anyway
					if (not imageName.startswith('.') and not imageName.startswith('_')):
						showcase = ('/' + projectFolder + subpath + '/' + projectShowcaseFolder + imageName) #Had weird broken image glitch on spec-out, doing this fixes that problem.
			else:
				pass

		except OSError as e:
			print(e, file=sys.stdout)
			pass

		#testDict = {"one":1, "two":2}

		
		#json.dump(testDict, open(projectFolder + subpath + '/' + projectManifestPath,'w'))

		

		try:
			projectManifest = (json.load(open(projectFolder + subpath + '/' + projectManifestPath)))
			print("===MANIFEST DATA LOADED===")
			#print(loaded, file=sys.stdout)
			galleryDictEmpty = False
		except OSError as e:
			print(e, file=sys.stdout)
			projectManifest = {}
			print("===MANIFEST DATA COULDN'T LOAD===")
			pass


		try: #need seperate phases here otherwise I'd wrap into one try / except
			if len(os.listdir(projectFolder + subpath + '/' + projectGalleryFolder)) > 0: 

				mediaPoolForThisProject = []

				for imageName in os.listdir(projectFolder + subpath + '/' + projectGalleryFolder):
					if (not imageName.startswith('.') and not imageName.startswith('_')):
						gallery.append('/' + projectFolder + subpath + '/' + projectGalleryFolder + imageName)
						#print(imageName + " added to pool for " + projectName)

				#for x in mediaPoolForThisProject:
					#print(x, file=sys.stdout)	
				#mediaPool[projectName] = os.listdir('static/publicProjects/' + projectName + '/' + 'media/')

				

			else:
				gallery = None
				#print("No media files to showcase for '" + projectName + "'")

		except OSError as e:
			gallery = None
			#print(e, file=sys.stdout)

		if galleryDictEmpty:
			print("===PROJECT MANIFEST IS NOT LOADED, FILLING VALUES")
			projectManifest['title'] = "No title available"
			projectManifest['description'] = "No description available"
			projectManifest['technologies'] = "No technologies available"
			projectManifest['platform'] = "No platforms available"


		
		crumb="projects"
		mimetype="text/html"

		gallery=gallery[::-1]  #reverse it since the gallery was backwards before.

		#session['projectSpec'] = [navigation_sections, crumb, mimetype, showcase, projectManifest['title'], projectManifest['description'], projectManifest['technologies'], gallery, projectManifest['platform'], (len(projectManifest['assets']) > 0)]
		
		#return set(page.url for page in self.getProjectSpec(subpath))

		#return redirect(url_for('projectspecs', navigation=navigation_sections, crumb=crumb, mimetype='text/html', showcaseImage=showcase, projectTitle=projectManifest['title'], projectDescription=projectManifest['description'], technologiesUsed=projectManifest['technologies'], gallery=gallery, platform=projectManifest['platform'], hasAssets = (len(projectManifest['assets']) > 0) ))

		#return redirect(url_for('projectspecs'))

		funcNames = {}
		tmp=[]


		funcCount = 0;

		for pic in gallery:

			funcNames[pic] = 'func' + str(funcCount)
			funcCount+=1




		link = "/blog/" + subpath + "/DOCS/index.html"
		

		hasDocumentation = True

		try:
			#tt = os.listdir("/blog/" + subpath + "/DOCS/")
			print("OPENING /static" + link)
			open('static/blog/' + subpath + "/DOCS/index.html", 'r')
			
		except:
			print("No docpath " + subpath, file=sys.stdout)
			hasDocumentation = False

		#hasDocumentation = (len(tt) > 0)

		return render_template('projectspecs.html', navigation=navigation_sections, crumb=crumb, mimetype='text/html', showcaseImage=showcase, projectTitle=projectManifest['title'], projectDescription=projectManifest['description'], technologiesUsed=projectManifest['technologies'], gallery=gallery, platform=projectManifest['platform'], hasAssets = (len(projectManifest['assets']) > 0), funcNames = funcNames, assets=projectManifest['assets'], link=link, hasDocumentation=hasDocumentation)
	else:
		return render_template('404.html', navigation=navigation_sections, crumb="projects", mimetype='text/html', hideNav=False, requestedProject=subpath)

    
#SPOT FOR BLOG

@app.route("/blog/<subpath>/", methods=['GET', 'POST'])
@app.route("/blog/<subpath>/")

#http://localhost:5000/projects/SPAN%20ENCRYPTION/download.html

def getBlogSpec(subpath):
	# show the subpath after /path/

	#try:
		#print("Attempting to open '" + projectFolder + subpath + "'", file=sys.stdout)

		#with open(projectFolder + subpath + "/") as f:
			
			#print("Attempting to open" + projectFolder + subpath, file=sys.stdout)

			#if not f:
				#print("No such directory when opened", file=sys.stdout)
			
			#return render_template('projects.html', navigation=navigation_sections, crumb="projects", mimetype='text/html', hideNav=False, requestedProject=subpath)

	#except OSError as e:

		#print( e, file=sys.stdout)

	#print("Sending 404..", file=sys.stdout)

	#return render_template('404.html', navigation=navigation_sections, crumb="projects", mimetype='text/html', hideNav=False, requestedProject=subpath)

	if (os.path.exists(blogFolder + subpath + "/")):

		showcase=None
		blogTitle=None
		blogDescription=None
		languagesUsed=None
		blogManifest = {}
		galleryDictEmpty = True
		gallery=[]

		try: 
			if len(os.listdir(blogFolder + subpath + '/' + blogGalleryShowcaseFolder)) > 0: 

				for imageName in os.listdir(blogFolder + subpath + '/' + blogGalleryShowcaseFolder): #Should only be one there anyway
					if (not imageName.startswith('.') and not imageName.startswith('_')):
						showcase = ('/' + blogFolder + subpath + '/' + blogGalleryShowcaseFolder + imageName) #Had weird broken image glitch on spec-out, doing this fixes that problem.
			else:
				pass

		except OSError as e:
			print(e, file=sys.stdout)
			pass

		#testDict = {"one":1, "two":2}

		
		#json.dump(testDict, open(projectFolder + subpath + '/' + projectManifestPath,'w'))

		

		try:
			blogManifest = (json.load(open(blogFolder + subpath + '/' + blogManifestPath)))
			print("===MANIFEST DATA LOADED===")
			#print(loaded, file=sys.stdout)
			galleryDictEmpty = False
		except OSError as e:
			print(e, file=sys.stdout)
			blogManifest = {}
			print("===MANIFEST DATA COULDN'T LOAD===")
			pass


		try: #need seperate phases here otherwise I'd wrap into one try / except
			if len(os.listdir(blogFolder + subpath + '/' + blogGalleryShowcaseFolder)) > 0: 

				mediaPoolForThisBlog = []

				for imageName in os.listdir(blogFolder + subpath + '/' + blogGalleryShowcaseFolder):
					if (not imageName.startswith('.') and not imageName.startswith('_')):
						gallery.append('/' + blogFolder + subpath + '/' + blogGalleryShowcaseFolder + imageName)
						#print(imageName + " added to pool for " + projectName)

				#for x in mediaPoolForThisProject:
					#print(x, file=sys.stdout)	
				#mediaPool[projectName] = os.listdir('static/publicProjects/' + projectName + '/' + 'media/')

				

			else:
				gallery = None
				#print("No media files to showcase for '" + projectName + "'")

		except OSError as e:
			gallery = None
			#print(e, file=sys.stdout)

		if galleryDictEmpty:
			print("===BLOG MANIFEST IS NOT LOADED, FILLING VALUES")
			blogManifest['title'] = "No title available"
			blogManifest['description'] = "No description available"
			blogManifest['technologies'] = "No technologies available"
			blogManifest['platform'] = "No platforms available"


		
		crumb="blog"
		mimetype="text/html"

		if not gallery is None:
			gallery=gallery[::-1]  #reverse it since the gallery was backwards before.

			for pic in gallery:

				funcNames[pic] = 'func' + str(funcCount)
				funcCount+=1

		#session['projectSpec'] = [navigation_sections, crumb, mimetype, showcase, projectManifest['title'], projectManifest['description'], projectManifest['technologies'], gallery, projectManifest['platform'], (len(projectManifest['assets']) > 0)]
		
		#return set(page.url for page in self.getProjectSpec(subpath))

		#return redirect(url_for('projectspecs', navigation=navigation_sections, crumb=crumb, mimetype='text/html', showcaseImage=showcase, projectTitle=projectManifest['title'], projectDescription=projectManifest['description'], technologiesUsed=projectManifest['technologies'], gallery=gallery, platform=projectManifest['platform'], hasAssets = (len(projectManifest['assets']) > 0) ))

		#return redirect(url_for('projectspecs'))

		funcNames = {}
		tmp=[]


		funcCount = 0;

		# Grab our article data
		file = open(blogFolder + subpath + '/' 'article.contents',mode='r')
		
		# read all lines at once
		rawarticlecontents = file.read()
		
		#file = open(blogFolder + subpath + '/' + 'DOCS' + '/' + 'index.html',mode='r')
		
		#include = file.read()

		# close the file
		file.close()


		#include = render_template(blogFolder + subpath + '/DOCS/' 'index.html')

		rawlines = []
		for line in rawarticlecontents.splitlines():
			rawlines.append(line)

		tt = open((blogFolder + subpath + '/DOCS/' + 'index.html'), 'r')

		# Create Template Object
		#template = Template(tt)

		# Render HTML Template String
		#include = template.render(name = "John")

		include = tt.read()

		#include = 'DOCS/index.html'

		hasAssets = len(include) > 0

		#hasAssets = ((len(blogManifest['assets']) > 0)


		link = "/blog/" + subpath + "/DOCS/" + "index.html"

		return render_template('blogtemplate.html', navigation=navigation_sections, crumb=crumb, mimetype='text/html', showcaseImage=showcase, blogTitle=blogManifest['title'], blogDescription=blogManifest['description'], technologiesUsed=blogManifest['technologies'], gallery=gallery, platform=blogManifest['platform'], hasAssets = hasAssets, funcNames = funcNames, assets=blogManifest['assets'], rawText = rawlines, include=include, link=link)
	else:
		return render_template('404.html', navigation=navigation_sections, crumb="blog", mimetype='text/html', hideNav=False, requestedBlog=subpath)


@app.route("/blog/<path:path>/")
def blogdoc(path):

	#give top level path to javadoc template then change dynamically, for now doing with just SPAN


	print("OG PATH > " + path, file=sys.stdout)

	foldername = path

	splitpath = path.split("/")

	blogFolder = splitpath[len(splitpath)-3]


	blogname = blogFolder

	safeblogname = safeBlogName(blogname)


	if (blogname == "SPAN Encryption"): 
		#blogname = "SPAN"
		safeblogname = "SPAN"

	reldocpath = "/static/blog/" + blogFolder + "/" + "DOCS/"
	
	

	modsummarylink = reldocpath + safeblogname + '/module-summary.html'

	styleslink = "/static/blog/" + blogname + "/DOCS/stylesheet.css"

	#url_for('static', filename='/blog/{{foldername}}/DOCS/{{blogname}}/module-summary.html') }}
	print("MODSUMMARY > " + modsummarylink, file=sys.stdout)

	#exit(1)

	#add hook to copy all files

	#styleslink = "/static/blog/" + blogname + "/DOCS/
	
	if not (os.path.exists("/docs/blog/" + blogFolder + "/DOCS/")):
		shutil.copytree("static/blog/" + blogFolder + "/DOCS/", "/docs/blog/" + blogFolder + "/DOCS/")

	if not (os.path.exists("docs/static/blog/" + blogFolder + "/DOCS/")):
		shutil.copytree("static/blog/" + blogFolder + "/DOCS/", "/docs/static/blog/" + blogFolder + "/DOCS/")

	return render_template("javadoctemplate.html", foldername = foldername, blogname = blogname, reldocpath=reldocpath, modsummarylink=modsummarylink, styleslink=styleslink)



#END SPOT FOR BLOG
@app.route("/about.html")
def about():
	
	return render_template('about.html', navigation=navigation_sections, crumb="about", mimetype='text/html', hideNav=False)

@app.route("/contact.html")
def contact():
	
	return render_template('contact.html', navigation=navigation_sections, crumb="contact", mimetype='text/html', hideNav=False)


@freezer.register_generator
def getProjectSpec():
	for projectName in os.listdir(projectFolder):
		if (not projectName.startswith('.') and not projectName.startswith('_')):
			print("Yielding (manually) '" + projectName + "' with main ", file=sys.stdout)
			yield {'subpath': projectName}

@freezer.register_generator
def getBlogSpec():
	for blogName in os.listdir(blogFolder):
		if (not blogName.startswith('.') and not blogName.startswith('_')):
			print("Yielding (manually) '" + blogName + "' with main ", file=sys.stdout)
			yield {'subpath': blogName}

@freezer.register_generator
def blogdoc():
		print("/static/blog/")

		for blogName in os.listdir("static/blog/"):
			print("Opening " + blogName)
			if (not blogName.startswith('.') and not blogName.startswith('_')):
				print("Yielding (manually) '" + blogName + "' with main ", file=sys.stdout)
				yield {'path': blogName}
				#yield {'path': blogName + '/DOCS/'}
				#yield {'path': blogName + '/DOCS/index.html'}
				#yield {'path': blogName + '/DOCS/' + safeBlogName(blogName) + "/module-summary.html"}

				print("BLOGDOC >", file=sys.stdout)
				print("YIELD " + blogName, file=sys.stdout)
				print("YIELD " + blogName + '/DOCS/', file=sys.stdout)
				print("YIELD " + blogName + '/DOCS/index.html', file=sys.stdout)
				print("YIELD > " + blogName + '/DOCS/' + safeBlogName(blogName) + "/module-summary.html", file=sys.stdout)
			else:
				print("Skipping")



#Manually
def safeBlogName(blogcheckname):
	
	if (blogcheckname == "SPAN Encryption"): blogcheckname = "SPAN"
	if (blogcheckname == "SPAN ENCRYPTION"): blogcheckname = "SPAN"
	return blogcheckname

freezer.freeze()

if __name__ == '__main__':

	def getProjectSpec():
		for projectName in os.listdir(projectFolder):
			if (not projectName.startswith('.') and not projectName.startswith('_')):
				print("Yielding (manually) '" + projectName + "' with main ", file=sys.stdout)
				yield {'subpath': projectName}

	def getBlogSpec():
		for blogName in os.listdir(blogFolder):
			if (not blogName.startswith('.') and not blogName.startswith('_')):
				print("Yielding (manually) '" + blogName + "' with main ", file=sys.stdout)
				yield {'subpath': blogName}


	def blogdoc():
		print("/static/blog/")

		try:
			for blogName in os.listdir("static/blog/"):
				if (not blogName.startswith('.') and not blogName.startswith('_')):
					print("Yielding (manually) '" + blogName + "' with main ", file=sys.stdout)
					yield {'path': blogName}
					#yield {'path': blogName + '/DOCS/'}
					#yield {'path': blogName + '/DOCS/index.html'}
					#yield {'path': blogName + '/DOCS/' + safeBlogName + "/module-summary.html"}

					print("BLOGDOC >")
					print("YIELD " + blogName)
					print("YIELD " + blogName + '/DOCS/')
					print("YIELD " + blogName + '/DOCS/index.html')
					print("YIELD > " + blogName + '/DOCS/' + safeBlogName + "/module-summary.html")
					
		except:
			print("BAD YIELD FOR BLOGDOC " )


	freezer.freeze()
	#app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)
else:
	print("NON MAIN RUN", file=sys.stdout)
