# gvapi flask app views

# python modules
from flask import jsonify, render_template, request, redirect, url_for, session, make_response
import logging
import time
import json
import requests
import uuid
import os

# gvapi modeules
import localConfig
from localConfig import logging
from app import gvapi_app
from api_main import api_main


# index
@gvapi_app.route("/{prefix}/".format(prefix=localConfig.GVAPI_APP_PREFIX), methods=['GET', 'POST'])
def index():

	return render_template('index.html',GVAPI_APP_PREFIX=localConfig.GVAPI_APP_PREFIX)


# submit_url
@gvapi_app.route("/{prefix}/submit_url".format(prefix=localConfig.GVAPI_APP_PREFIX), methods=['GET', 'POST'])
def submit_url():

	# TO-DO set from checkbox on form
	result_type = 'JSON'

	# image URL
	try:
		logging.debug('retrieving %s' % request.form['image_url'])
		image_url = request.form['image_url']
	except:
		logging.warning('image_url not found')

	# download image
	temp_filename = "img/"+str(uuid.uuid4())+".image"
	logging.debug('writing to %s' % temp_filename)
	r = requests.get(image_url, stream=True)
	if r.status_code == 200:
		with open(temp_filename, 'wb') as f:
			for chunk in r.iter_content(1024):
				f.write(chunk)


	# run API call
	response = api_main(temp_filename)

	# delete temp filename
	os.remove(temp_filename)

	# HTML
	if result_type == "HTML":
		return render_template('results.html',temp_filename=temp_filename,response=response)

	# JSON
	else:
		logging.debug("returning JSON")
		response = make_response( json.dumps(response) )
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
		response.headers['Access-Control-Allow-Headers'] = 'x-prototype-version,x-requested-with'
		response.headers['Access-Control-Max-Age'] = 2520
		response.headers["Content-Type"] = "application/json"		
		response.headers['X-Powered-By'] = 'ShoppingHorse'
		response.headers['Connection'] = 'Close'
		return response