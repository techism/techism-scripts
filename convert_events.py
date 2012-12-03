#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import csv
import json

def __read_csv(filename, key='key'):
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        users_by_id = {}
        for row in reader:
            users_by_id[row[key]] = row
        return users_by_id

def __get_tag_names(old_event):
    #TODO: strip, filter empty, lowercase
    return  old_event['tags'].split('|')

def __convert_tags(events_by_id, objects):
    key = 0
    tags_by_name = {}
    for old_event in events_by_id.values():
        tag_names = __get_tag_names(old_event)
        for tag_name in tag_names:
            if not tag_name in tags_by_name:
                key += 1
                tag = {}
                tag['model'] = 'techism.eventtag'
                tag['pk'] = key
                tag['fields'] = {'name':tag_name}
                objects.append(tag)
                tags_by_name[tag_name] = tag
    return tags_by_name

def __convert_events(events_by_id, tags_by_name, objects):
    for eventid,old_event in events_by_id.items():
        event = {}
        event['model'] = 'techism.event'
        event['pk'] = int(eventid)
        fields = {}
        fields['title'] = old_event['title']
        fields['description'] = old_event['description']
        fields['url'] = old_event['url']
        tag_ids = []
        tag_names = __get_tag_names(old_event)
        for tag_name in tag_names:
            tag_ids.append(tags_by_name[tag_name]['pk'])
        fields['tags'] = tag_ids
        fields['date_time_begin'] = old_event['date_time_begin'] + '.000Z'
        if old_event['date_time_end']:
            fields['date_time_end'] = old_event['date_time_end'] + '.000Z'
        if old_event['location_id']:
            fields['location'] = old_event['location_id']
        if old_event['organization_id']:
            fields['organization'] = old_event['organization_id']
        if old_event['user_id']:
            fields['user'] = old_event['user_id']
        fields['published'] = old_event['published'] == 'True'
        fields['canceled'] = old_event['canceled'] == 'True'
        fields['date_time_created'] = old_event['date_time_created'] + '.000Z'
        if old_event['date_time_modified']:
            fields['date_time_modified'] = old_event['date_time_modified'] + '.000Z'
        event['fields'] = fields
        objects.append(event)


###

objects = []

events_by_id = __read_csv('techism2_event.csv')
tags_by_name = __convert_tags(events_by_id, objects)
__convert_events(events_by_id, tags_by_name, objects)

data = json.dumps(objects, indent=4)
print data

