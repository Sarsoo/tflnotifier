import requests, smtplib, os

url = 'https://api.tfl.gov.uk/'
app_id = os.environ['TFLID']
app_key = os.environ['TFLKEY']

def _TFLURL(path):
	return 'https://api.tfl.gov.uk/' + path + '?app_id={}&app_key={}'.format(app_id, app_key)

def getLineStatusRequest(line):

	payload = {'app_id': app_id, 'app_key': app_key}
	
	return requests.get(url + 'Line/{}/Status'.format(line), params = payload)

def lineStatus(line):
	resp = getLineStatusRequest(line)

	print(resp.json()[0]['name'])
	#print(resp.json()['name'])
	#print(resp.json()[0]['lineStatuses'][0]['statusSeverityDescription'])

	for status in resp.json()[0]['lineStatuses']:
		print(status['statusSeverityDescription'])
    
def isDelayed(line):
	resp = getLineStatusRequest(line)
  
	for status in resp.json()[0]['lineStatuses']:
		if status['statusSeverity'] < 10:
			return True
	return False
	
def getLineStatusDescription(line):
	resp = getLineStatusRequest(line)
	
	if len(resp.json()[0]['lineStatuses']) > 1:
		list = []
		for status in resp.json()[0]['lineStatuses']:
			list.append(status['statusSeverityDescription'])
		return list
	else:
		return resp.json()[0]['lineStatuses'][0]['statusSeverityDescription']

def getLineStatusReason(line):
	resp = getLineStatusRequest(line)
	if isDelayed(line):
		list = []
		for status in resp.json()[0]['lineStatuses']:
			list.append(status['reason'])
		return list
	else:
		return None

def sendNotification(message, subject = ''):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(os.environ['TFLMAILFROM'], os.environ['TFLPW'])
	
	msg = 'Subject: {}\n\n{}'.format(subject, message)
	server.sendmail(os.environ['TFLMAILFROM'], os.environ['TFLMAILTO'], msg)
	server.quit()

message = 'met line: '
for description in getLineStatusDescription('metropolitan'):
	message += description + ' '
metReasons = getLineStatusReason('metropolitan')
if metReasons:
	for reason in metReasons:
		message += '\n\t\t' + reason
message += '\n'
message += 'pic line: '
for description in getLineStatusDescription('piccadilly'):
	message += description + ' '
picReasons = getLineStatusReason('piccadilly')
if picReasons:
	for reason in picReasons:
		message += '\n\t\t' + reason
message += '\n'
message += 'dis line: '
for description in getLineStatusDescription('district'):
	message += description + ' '
disReasons = getLineStatusReason('district')
if disReasons:
	for reason in disReasons:
		message += '\n\t\t' + reason

#print(message)
sendNotification(message, 'tfl update')
