# nordpool-mqtt
Parse todays and the next days power prices from Nordpool and publish them om MQTT

# Setup

Just set up two cronjobs like this:
```
0 13 * * * /usr/bin/python /path/to/nordpool-mqtt/nordpool_cache.py
0 * * * * /usr/bin/python /path/to/nordpool-mqtt/nordpool_mqtt.py
```
