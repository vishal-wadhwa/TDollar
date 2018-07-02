import requests 
import json
import datetime
import time
import buildDropDown

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
	return datetimeObj.strftime('%I:%M %p')
	# return '%s:%s'%(datetimeObj.hour, datetimeObj.minute)

headers = {
	'content-type': 'application/json'
}

url = 'https://hooks.slack.com/services/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'
types = ['table_tennis']
# twoHrs= datetime.timedelta(hours = 2)
twoHrs= datetime.timedelta(minutes = 2)
# duration = datetime.timedelta(minutes = 20)
duration = datetime.timedelta(minutes = 1)
while(True):
	for type in types:
		current_time = datetime.datetime.now()
		if not len(openSlots[type]) == 0:
			finishSlot=openSlots[type][0]
			finishSlot.status='closed'
			db.session.commit()
			openSlots[type].pop(0)
			fStart=finishSlot.start_time
			fEnd = fStart +duration
			print fStart
			print current_time + duration
			print current_time + duration > fStart
			if current_time + duration > fStart:
				finishSlot.status='closed'
				finishSlot_bids = bidInfo.query.filter_by(slot_id = finishSlot.slot_id).all()
				print finishSlot_bids
				highestBidder = ''
				highestBid = -1
				for bid in finishSlot_bids:
					if bid.amt>highestBid:
						highestBid = bid.amt
						highestBidder = users.query.filter_by(name  = bid.name).first()

				if highestBid == -1:
					user_name = 'No Bidder'
				else:
					user_name = highestBidder.fullname
	

				data ={
				'text': '',
				'attachments': buildDropDown.slotDispStart('Winner for the following {} slot is: *{}*. :confetti_ball: '.format(type, user_name), modify(fStart), modify(fEnd))
				}
				re = requests.post(url, data = json.dumps(data), headers = headers)
				
				
				if not user_name == 'No Bidder':
					for bid in finishSlot_bids:
						if bid.name == highestBidder.name:
							continue
						uu = users.query.filter_by(name=bid.name).first()
						uu.holding=uu.holding+bid.amt

			
		slot_start = current_time + twoHrs
		slot_finish = slot_start + duration
		data ={
			'text': '',
			'attachments': buildDropDown.slotDispStart('Bidding for the following {} slot begins: '.format(type), modify(slot_start), modify(slot_finish))
		}
		newSlot = slots(start_time = slot_start, slot_type='table_tennis')
		openSlots[type].append(newSlot)
		db.session.add(newSlot)
		db.session.commit()

		re = requests.post(url, data = json.dumps(data), headers = headers)
		print re
		time.sleep(60)
		# time.sleep(20*60)
