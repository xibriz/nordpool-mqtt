#!/usr/bin/python
# coding: utf-8

import configparser
from urllib.request import urlopen
import json
import datetime
import paho.mqtt.publish as publish
import os
import codecs

main_base = os.path.dirname(__file__)
config_file = os.path.join(main_base, "config", "prod.cfg")

config = configparser.ConfigParser()
config.read_file(codecs.open(config_file, 'r', 'utf8'))

mqtt_port = config.getint('MQTT', 'port')
mqtt_ip = config.get('MQTT', 'ip')
mqtt_topic_today = config.get('MQTT', 'today_pub')
mqtt_topic_tomorrow = config.get('MQTT', 'tomorrow_pub')
dir_path = config.get('Nordpool', 'cache_dir')
city = config.get('Nordpool', 'city')

dt_today = datetime.date.today().strftime("%d-%m-%Y")

def publish_price(topic, date):
	data = json.load(open('{}/{}.json'.format(dir_path, date)))

	#print u'Units: {}\n Updated: {}\n Currency:{}'.format(resp_dict['data']['Units'][0], resp_dict['data']['DateUpdated'], resp_dict['currency'])
	for row in data['data']['Rows']:
		for col in row['Columns']:
			if col['Name'] != city:
				continue
			hours_display = row['Name'].replace('&nbsp;', '')
			publish.single(topic.format(value=hours_display), col['Value'].replace(',','.').replace(' ',''), hostname=mqtt_ip, port=mqtt_port)
			#Check if current time
			now = datetime.datetime.now()
			hours = hours_display.split('-')
			try:
				if date == dt_today and (datetime.time(int(hours[0]),00) <= now.time() <= datetime.time(int(hours[1]),00) or (datetime.time(23,00) <= now.time() and int(hours[1]) == 0)):
					publish.single(topic.format(value='current'), col['Value'].replace(',','.').replace(' ',''), hostname=mqtt_ip, port=mqtt_port)
			except ValueError:
				pass

#Get todays prices
publish_price(mqtt_topic_today, dt_today)

#We only have next day prices after 12:00
now = datetime.datetime.now()
if now.time() >= datetime.time(13,00):
	dt_tomorrow = (datetime.date.today()+ datetime.timedelta(days=1)).strftime("%d-%m-%Y")
	publish_price(mqtt_topic_tomorrow, dt_tomorrow)
