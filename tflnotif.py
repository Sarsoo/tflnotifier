import requests
import os

url = 'https://api.tfl.gov.uk/'
app_id = os.environ['TFLID']
app_key = os.environ['TFLKEY']


def getLineStatusRequest(lines):

	payload = {'app_id': app_id, 'app_key': app_key}
	
	return requests.get(url + 'Line/{}/Status'.format(','.join(lines)), params=payload)


def sendNotification(linename, message):

	json = {"text": "{}: {}".format(linename, message)}

	requests.post(os.environ['SLACKHOOK'], json=json)


if __name__ == '__main__':

	statuses = getLineStatusRequest(['metropolitan', 'piccadilly']).json()

	for line in statuses:

		statustext = ''

		for status in line['lineStatuses']:
			if status['statusSeverity'] < 10:
				statustext += '\n' + status['reason']

		sendNotification(line['id'][:3], ', '.join([i['statusSeverityDescription'] for i in line['lineStatuses']]) + statustext)
