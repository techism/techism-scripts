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

def __get_tag_names(old_org):
    #TODO: strip, filter empty, lowercase
    return  old_org['tags'].split('|')

def __convert_tags(orgs_by_id, objects):
    key = 0
    tags_by_name = {}
    for old_org in orgs_by_id.values():
        tag_names = __get_tag_names(old_org)
        for tag_name in tag_names:
            if not tag_name in tags_by_name:
                key += 1
                tag = {}
                tag['model'] = 'techism.organizationtag'
                tag['pk'] = key
                tag['fields'] = {'name':tag_name}
                objects.append(tag)
                tags_by_name[tag_name] = tag
    return tags_by_name

def __convert_orgs(orgs_by_id, tags_by_name, objects):
    for orgid,old_org in orgs_by_id.items():
        org = {}
        org['model'] = 'techism.organization'
        org['pk'] = int(orgid)
        fields = {}
        fields['title'] = old_org['title']
        fields['description'] = old_org['description']
        fields['url'] = old_org['url']
        tag_ids = []
        tag_names = __get_tag_names(old_org)
        for tag_name in tag_names:
            tag_ids.append(tags_by_name[tag_name]['pk'])
        fields['tags'] = tag_ids
        org['fields'] = fields
        objects.append(org)


###

objects = []

orgs_by_id = __read_csv('techism2_organization.csv')
tags_by_name = __convert_tags(orgs_by_id, objects)
__convert_orgs(orgs_by_id, tags_by_name, objects)

data = json.dumps(objects, indent=4)
print data


