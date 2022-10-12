# nordpool-mqtt
Parse todays and the next days electricity prices from Nordpool and publish them om MQTT

# Changes to original code include

Breaking change in configuration: no more city, select area from one of
- AT Austria
- BE Belgium
- DE Germany
- DK1, DK2 - Denmark
- EE - Estonia
- FI - Finland
- FR - France
- LT - Lithuania
- LV - Latvia
- NL - Netherlands
- NO1 - Oslo
- NO2 - Krstiansand
- NO3 - Molde, Trondheim
- NO4 - Tromsø
- NO5 - Bergen
- SE, SE1, SE2, SE3, SE4 - Sweden

Currency selection from *EUR*, DKK, NOK, SEK. Where EUR is now the default in configuration file. You should set to NOK to get the original behaviour.

Configuration now adds username and password for MQTT and is required for publishing topics to the MQTT server. Setup authentication also on the MQTT server.

## Installation
```
$ git clone https://github.com/oh2th/nordpool-mqtt.git
$ cd nordpool-mqtt
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install pip --upgrade
$ pip3 install -r requirements.txt
```

## Configuration

Copy `config/default.cfg` to `config/prod.cfg` and fill in all the FIXME values

# Setup

Just set up two cronjobs like this:
```
0 13 * * * /usr/bin/python /path/to/nordpool-mqtt/nordpool_cache.py
0 * * * * /usr/bin/python /path/to/nordpool-mqtt/nordpool_mqtt.py
```

# Output

```
nordpool/price/today/00-01 292.47
nordpool/price/today/01-02 291.70
nordpool/price/today/02-03 291.79
nordpool/price/today/03-04 289.07
nordpool/price/today/04-05 292.18
nordpool/price/today/05-06 299.47
nordpool/price/today/06-07 305.02
nordpool/price/today/07-08 318.63
nordpool/price/today/08-09 331.17
nordpool/price/today/09-10 325.82
nordpool/price/today/10-11 319.41
nordpool/price/today/11-12 318.73
nordpool/price/today/current 318.73
nordpool/price/today/12-13 318.34
nordpool/price/today/13-14 320.67
nordpool/price/today/14-15 322.52
nordpool/price/today/15-16 324.85
nordpool/price/today/16-17 328.55
nordpool/price/today/17-18 342.06
nordpool/price/today/18-19 351.01
nordpool/price/today/19-20 341.67
nordpool/price/today/20-21 329.81
nordpool/price/today/21-22 329.52
nordpool/price/today/22-23 320.96
nordpool/price/today/23-00 312.60
nordpool/price/today/Min 289.07
nordpool/price/today/Max 351.01
nordpool/price/today/Average 317.42
nordpool/price/today/Peak 328.73
nordpool/price/today/Off-peak 1 297.54
nordpool/price/today/Off-peak 2 323.22
```
