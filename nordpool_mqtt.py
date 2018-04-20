#!/usr/bin/python
# coding: utf-8

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
import datetime
import paho.mqtt.publish as publish

mqtt_port = '1883'
mqtt_ip = 'FIX ME'
mqtt_topic_today = 'nordpool/price/today/{}'
mqtt_topic_tomorrow = 'nordpool/price/tomorrow/{}'
dir_path = '/path/to/nordpool-mqtt'
# Possible values: Oslo, Kr.sand, Bergen, Tr.heim, Molde, Tromsø
city = u'Tromsø'
dt_today = datetime.date.today().strftime("%d-%m-%Y")

def publish_price(topic, date):
	data = json.load(open('{}/cache/{}.json'.format(dir_path, date)))

	#print u'Units: {}\n Updated: {}\n Currency:{}'.format(resp_dict['data']['Units'][0], resp_dict['data']['DateUpdated'], resp_dict['currency'])
	for row in data['data']['Rows']:
		for col in row['Columns']:
			if col['Name'] != city:
				continue
			hours_display = row['Name'].replace('&nbsp;', '')
			publish.single(topic.format(hours_display), col['Value'].replace(',','.').replace(' ',''), hostname=mqtt_ip, port=mqtt_port)
			#Check if current time
			now = datetime.datetime.now()
			hours = hours_display.split('-')
			try:
				if date == dt_today and (datetime.time(int(hours[0]),00) <= now.time() <= datetime.time(int(hours[1]),00) or (datetime.time(23,00) <= now.time() and int(hours[1]) == 0)):
					publish.single(topic.format('current'), col['Value'].replace(',','.').replace(' ',''), hostname=mqtt_ip, port=mqtt_port)
			except ValueError:
				pass

#Get todays prices
publish_price(mqtt_topic_today, dt_today)

#We only have next day prices after 12:00
now = datetime.datetime.now()
if now.time() >= datetime.time(13,00):
	dt_tomorrow = (datetime.date.today()+ datetime.timedelta(days=1)).strftime("%d-%m-%Y")
	publish_price(mqtt_topic_tomorrow, dt_tomorrow)
