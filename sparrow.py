import requests


def sparrow(mobile_number,code):
	token = 'PbeQPaeIWAkDPNKzbFsm'
	sender = 'Demo'
	to = int(mobile_number)
	text = 'The key for your registration to Chalak is: ' + code
	r = requests.post(
	    "http://api.sparrowsms.com/v2/sms/",
	    data={'token' : token,
	          'from'  : sender,
	          'to'    :  to,
	          'text'  : text })

	status_code = r.status_code
	response = r.text
	response_json = r.json()


def sparrow2(mobile_number,password):
	token = 'PbeQPaeIWAkDPNKzbFsm'
	sender = 'Demo'
	to = int(mobile_number)
	text = 'The password registered to this number is ' + password
	r = requests.post(
	    "http://api.sparrowsms.com/v2/sms/",
	    data={'token' : token,
	          'from'  : sender,
	          'to'    :  to,
	          'text'  : text })

	status_code = r.status_code
	response = r.text
	response_json = r.json()

