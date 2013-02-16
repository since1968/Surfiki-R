#!/usr/bin/python
# -*- coding: utf-8 -*-

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
body_content = "{\"query\": {\"bool\": {\"must\": [{\"range\": {\"dtInsertDT\": {\"from\": $start,\"to\": $end}}},{\"query_string\": {\"default_field\": \"strItemKeywords\",\"query\": \"obama\"}}],\"must_not\": [],\"should\": []},\"from\": 0,\"size\": 1000000,\"sort\": [],\"facets\": {}}}"
body_content = body_content.replace("$start", str(hourago))
body_content = body_content.replace("$end", str(current))
print body_content
connection.request("POST",'/search/surfiki/_search',body_content,headers)
result = connection.getresponse()
data = result.read()
connection.close()
decoded = data.decode('utf-8','ignore')
res = json.loads(decoded)
hits = res['hits']['hits']

f = open('obama.csv', "wb+")
csv_file = csv.writer(f, quoting=csv.QUOTE_ALL)
csv_file.writerow(['strURLType','dTItemDateTime','strOpinon','strOnjSubj'])

for hit in hits:
    try:
        csv_file.writerow([hit['_source']['strURLType'],hit['_source']['dTItemDateTime'],hit['_source']['strOpinon'],hit['_source']['strObjSubj']])
    except (UnicodeEncodeError) as ex:
        continue
f.close()