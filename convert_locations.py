#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import csv
import json
#from geopy import geocoders
import time

def __read_csv(filename, key='key'):
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        users_by_id = {}
        for row in reader:
            users_by_id[row[key]] = row
        return users_by_id

def __convert_locations(locations_by_id, objects):
    #g = geocoders.Google(domain='maps.google.de')
    for locid,old_loc in locations_by_id.items():
        loc = {}
        loc['model'] = 'techism.location'
        loc['pk'] = locid
        fields = {}
        fields['name'] = old_loc['name']
        fields['city'] = old_loc['city']
        fields['street'] = old_loc['street']
        #try:
        #    r, (lat, lng) = g.geocode(old_loc['street'] + ", " + old_loc['city'])
        #    fields['latitude'] = lat
        #    fields['longitude'] = lng
        #except:
        #    pass
        loc['fields'] = fields
        objects.append(loc)
        #print json.dumps(loc, indent=4)
        #time.sleep(1)

###

objects = []

locations_by_id = __read_csv('techism2_location.csv')
__convert_locations(locations_by_id, objects)

data = json.dumps(objects, indent=4)
print data

