from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

@app.route('/upload')
def upload_file():
	return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploaded_file():
	if request.method == 'POST':
		f = request.files['file']
		infile = secure_filename(f.filename)
		outfile = infile.split('.')[0] + '.pbm'
		viewfile = infile.split('.')[0] + '.gif'
		f.save('static/' + infile)
		size = request.form.get('size')
		dots = request.form.get('dots')
		command = 'convert {} +level {}%,100% -resize {} -dither FloydSteinberg -remap pattern:gray50 -compress none {}'.format('static/' + infile, dots, size, 'static/' + outfile) 
		os.system(command)
		command = 'convert {} {}'.format('static/' + outfile, 'static/' + viewfile)
		os.system(command)
		return render_template('uploaded.html', user_image = viewfile)

@app.after_request
def add_header(r):
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"
	r.headers["Expires"] = "0"
	r.headers['Cache-Control'] = 'public, max-age=0'
	return r	

if __name__ == '__main__':
	app.run(debug = True)
