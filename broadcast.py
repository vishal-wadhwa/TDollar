import requests 
import json
import datetime
import time

text = ''' The bidding for %s for the following slot begins now \n 
Start: %s \n
End: %s \n
'''

def modify(datetimeObj):
	return '%s:%s'%(datetimeObj.hour, datetimeObj.minute)

headers = {
	'content-type': 'application/json'
}
url = 'https://hooks.slack.com/services/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'
types = ['TT']
twoHrs= datetime.timedelta(hours = 2)
duration = datetime.timedelta(minutes = 20)
while(True):
	for type in types:
		current_time = datetime.datetime.now()
		slot_start = current_time + twoHrs
		slot_finish = slot_start + duration
		data ={
			'text': text%(type, modify(slot_start), modify(slot_finish))
		}
		re = requests.post(url, data = json.dumps(data), headers = headers)
		print re
		time.sleep(20*60)
