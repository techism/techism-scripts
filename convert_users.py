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

def __convert_users(users_by_id, objects):
    for userid,old_user in users_by_id.items():
        user = {}
        user['model'] = 'auth.user'
        user['pk'] = userid
        fields = {}
        fields['username'] = old_user['username']
        fields['password'] = '!'
        fields['email'] = old_user['email']
        fields['first_name'] = old_user['first_name']
        fields['last_name'] = old_user['last_name']
        fields['is_active'] = old_user['is_active'] == 'True'
        fields['is_staff'] = old_user['is_staff'] == 'True'
        fields['is_superuser'] = old_user['is_superuser'] == 'True'
        fields['date_joined'] = old_user['date_joined'] + '.000Z'
        fields['last_login'] = old_user['last_login'] + '.000Z'
        user['fields'] = fields
        objects.append(user)

def __create_socialauth_user(key, userid, provider, uid, objects):
    usersocialauth = {}
    usersocialauth['model'] = 'social_auth.usersocialauth'
    usersocialauth['pk'] = key
    fields = {}
    fields['user'] = int(userid)
    fields['extra_data'] = '{}'
    fields['provider'] = provider
    fields['uid'] = uid
    usersocialauth['fields'] = fields
    #print provider + ' - ' + uid + ' - ' + userid
    objects.append(usersocialauth)

def __convert_socialauth(users_by_id, openid_by_userid, objects):
    key = 0
    mails = set()
    # 1st convert OpenID accounts
    for userid,old_user in users_by_id.items():
        if openid_by_userid.has_key(userid):
            key += 1
            mails.add(old_user['email'])
            if openid_by_userid[userid]['claimed_id'].startswith('https://www.google.com/accounts/o8'):
                __create_socialauth_user(key, userid, 'google', old_user['email'], objects)
            else:
                __create_socialauth_user(key, userid, 'openid', openid_by_userid[userid]['claimed_id'], objects)
    # 2nd convert Google accounts, avoid duplicates
    for userid,old_user in users_by_id.items():
        if not openid_by_userid.has_key(userid):
            if not old_user['email'] in mails:
                key += 1
                __create_socialauth_user(key, userid, 'google', old_user['email'], objects)
        

###

objects = []

users_by_id = __read_csv('auth_user.csv')
__convert_users(users_by_id, objects)

openid_by_userid = __read_csv('django_openid_auth_useropenid.csv', key='user_id')
__convert_socialauth(users_by_id, openid_by_userid, objects)

data = json.dumps(objects, indent=4)
print data

