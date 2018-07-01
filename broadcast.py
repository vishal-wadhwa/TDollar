import requests 
import json
import datetime
import time
import Queue
from app import *
openSlots = {
	'table_tennis':[],
	'foosball':[],
	'massage_chair':[],
	'leg_massager':[]
}

text = ''' The bidding for %s for the following slot begins now \n 
Start: %s \n
End: %s \n
'''

finishText = '''
The winner for %s for the following slot \n
Start: %s End: %s
is %s
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
		if not len(openSlots) == 0:
			finishSlot=openSlots[type][0]
			openSlots[type].pop(0)
			fStart=finishSlot.start_time
			fEnd = fStart +duration
			if current_time + duration > fStart:
				finishSlot.status='closed'
			highestBidder=finishSlot.highestBidder
			userObj = users.query.filter_by(name=highestBidder).first()
			data ={
			'text': finishText%(type, modify(fStart), modify(fEnd), userObj.fullname)
			}
			re = requests.post(url, data = json.dumps(data), headers = headers)
			
			finishSlot_bids = bidInfo.query.filter_by(slot_id = finishSlot.slot_id).all()
			for bid in finishSlot_bids:
				if bid.name == userObj.name:
					continue
				uu = users.query.filter_by(name=bid.name).first()
				uu.holding=uu.holding+bid.amt
		
		slot_start = current_time + twoHrs
		slot_finish = slot_start + duration
		data ={
			'text': text%(type, modify(slot_start), modify(slot_finish))
		}
		newSlot = slot(start_time = slot_start, slot_type='table_tennis')
		openSlots['type'].append(newSlot)
		db.session.add(newSlot)
		db.session.commit()

		re = requests.post(url, data = json.dumps(data), headers = headers)
		print re
		time.sleep(20*60)
