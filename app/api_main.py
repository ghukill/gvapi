# globals
import os
import requests
import json

# locals
import localConfig
from localConfig import logging

def api_main(image):
	# request
	data = {
	  "requests":[
	    {
	      "image":{
	        "content":False
	      },
	      "features":[
	        {
	          "type":"FACE_DETECTION",
	          "maxResults":20
	        },
	        {
	          "type":"LABEL_DETECTION",
	          "maxResults":20
	        },
	        {
	          "type":"TEXT_DETECTION",
	          "maxResults":20
	        },
	        {
	          "type":"LANDMARK_DETECTION",
	          "maxResults":20
	        },
	        {
	          "type":"LOGO_DETECTION",
	          "maxResults":20
	        }
	      ]
	    }
	  ]
	}

	# sample image
	fhand = open(image,'r')

	# set to json
	data['requests'][0]['image']['content'] = fhand.read().encode('base64')

	# send request
	r = requests.post('https://vision.googleapis.com/v1alpha1/images:annotate?key=%s' % localConfig.API_KEY, data=json.dumps(data), headers={'Content-Type': 'application/json'})

	# print results
	# logging.debug(r.text)

	# print cute
	response = json.loads(r.text)
	return response
