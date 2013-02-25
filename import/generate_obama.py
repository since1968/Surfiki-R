#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from os.path import abspath, dirname, join
import httplib
import time
import json
import csv

connection =  httplib.HTTPConnection('api.surfiki.io:80')
connection.connect()
headers = {}
headers['Content-Type'] = 'application/json'
current = int(round(time.time() * 1000))
hourago = current - 1000 * 60 * 60 * 24 * 120
body_content = "{\"query\": {\"bool\": {\"must\": [{\"range\": {\"dTItemDateTime\": {\"from\": $start,\"to\": $end}}},{\"query_string\": {\"default_field\": \"strItemKeywords\",\"query\": \"obama\"}}],\"must_not\": [],\"should\": []},\"from\": 0,\"size\": 0,\"sort\": [],\"facets\": {}}}"
body_content = body_content.replace("$start", str(hourago))
body_content = body_content.replace("$end", str(current))
connection.request("POST",'/search/surfiki/_search?search_type=count',body_content,headers)
res = json.loads(connection.getresponse().read().decode('utf-8','ignore'))
total = int(res['hits']['total'])
if os.path.exists('obama.csv'):
    os.remove('obama.csv')
f = open('obama.csv', 'w')
f.close()

size = 2000 
for index in range(0, (total + 1)/size - 1):
    body_content = "{\"query\": {\"bool\": {\"must\": [{\"range\": {\"dTItemDateTime\": {\"from\": $start,\"to\": $end}}},{\"query_string\": {\"default_field\": \"strItemKeywords\",\"query\": \"obama\"}}],\"must_not\": [],\"should\": []},\"from\": $begin,\"size\": $size,\"sort\": [],\"facets\": {}}}"
    body_content = body_content.replace("$start", str(hourago))
    body_content = body_content.replace("$end", str(current))
    body_content = body_content.replace("$begin", str(index*size))
    body_content = body_content.replace("$size", str(size))
    print body_content
    connection.request("POST",'/search/surfiki/_search',body_content,headers)
    res = json.loads(connection.getresponse().read().decode('utf-8','ignore'))
    hits = res['hits']['hits']

    f = open('obama.csv', "a")
    csv_file = csv.writer(f, quoting=csv.QUOTE_ALL)
    csv_file.writerow(['strURLType','dTItemDateTime','strOpinion','strObjSubj'])

    for hit in hits:
        try:
            csv_file.writerow([hit['_source']['strURLType'],hit['_source']['dTItemDateTime'],hit['_source']['strOpinon'],hit['_source']['strObjSubj']])
        except (UnicodeEncodeError) as ex:
            continue
    f.close()
connection.close()
