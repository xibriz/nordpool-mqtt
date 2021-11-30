#!/usr/bin/python
# coding: utf-8

import configparser
from urllib.request import urlopen
import json
import datetime
import os
import codecs

main_base = os.path.dirname(__file__)
config_file = os.path.join(main_base, "config", "prod.cfg")

config = configparser.ConfigParser()
config.read_file(codecs.open(config_file, 'r', 'utf8'))

dir_path = config.get('Nordpool', 'cache_dir')
city = config.get('Nordpool', 'city')

def save_price(date):
	response = urlopen('https://www.nordpoolgroup.com/api/marketdata/page/23?currency=NOK&endDate={}'.format(date))
	data = json.loads(response.read())

	with open('{}/{}.json'.format(dir_path, date), 'w') as outfile:
		json.dump(data, outfile)

#Get todays prices
dt_today = datetime.date.today().strftime("%d-%m-%Y")
save_price(dt_today)

#We only have next day prices after 12:00
now = datetime.datetime.now()
if now.time() >= datetime.time(12,00):
	dt_tomorrow = (datetime.date.today()+ datetime.timedelta(days=1)).strftime("%d-%m-%Y")
	save_price(dt_tomorrow)
