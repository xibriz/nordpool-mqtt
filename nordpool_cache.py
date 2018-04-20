#!/usr/bin/python
# coding: utf-8

import urllib2
import json
import datetime


dir_path = '/path/to/nordpool-mqtt'
# Possible values: Oslo, Kr.sand, Bergen, Tr.heim, Molde, Tromsø
city = u'Tromsø'

def save_price(date):
	response = urllib2.urlopen('https://www.nordpoolgroup.com/api/marketdata/page/23?currency=NOK&endDate={}'.format(date))
	data = json.loads(response.read())

	with open('{}/cache/{}.json'.format(dir_path, date), 'w') as outfile:
		json.dump(data, outfile)

#Get todays prices
dt_today = datetime.date.today().strftime("%d-%m-%Y")
save_price(dt_today)

#We only have next day prices after 12:00
now = datetime.datetime.now()
if now.time() >= datetime.time(12,00):
	dt_tomorrow = (datetime.date.today()+ datetime.timedelta(days=1)).strftime("%d-%m-%Y")
	save_price(dt_tomorrow)
