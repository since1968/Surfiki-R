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
body_content = "{\"query\": {\"bool\": {\"must\": [{\"range\": {\"dtInsertDT\": {\"from\": $start,\"to\": $end}}},{\"query_string\": {\"default_field\": \"strItemKeywords\",\"query\": \"republicans\"}}],\"must_not\": [],\"should\": []},\"from\": 0,\"size\": 100000,\"sort\": [],\"facets\": {}}}"
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

f = open('republicans.csv', "wb+")
csv_file = csv.writer(f, quoting=csv.QUOTE_ALL)
csv_file.writerow(['strItemLinkURL','strItemTitle','strKeywords','strItemKeywords','dTItemDateTime','dtInsertDT','strItemDesc','intFKstrLinkURL','strSemItemKeywords','strItemTitleKeywords','bitHasLocation','strOpinon','strObjSubj','strSGML','strLocation','strNames','geoLat','geoLong','strURLType','strImageURL','strIOFileName','strEmails','bitHasEmails','strPhones','bitHasPhones','bitHasNames','bitHasMoney','strMoney','bitHasNumerics','strNumerics','bitHasQuestions','strURLS','bitHasURLS','bitHasMetrics','strSC','strWC','strWPS','strSYC','strSPW','strLD','strKGL','strFRE','strGFI','bitHasMisc','strMiscOne','strMiscTwo','strMiscThree','strMiscFour','strMiscFive'])

for hit in hits:
    try:
        csv_file.writerow([hit['_source']['strItemLinkURL'],hit['_source']['strItemTitle'],hit['_source']['strKeywords'],hit['_source']['strItemKeywords'],hit['_source']['dTItemDateTime'],hit['_source']['dtInsertDT'],hit['_source']['strItemDesc'],hit['_source']['intFKstrLinkURL'],hit['_source']['strSemItemKeywords'],hit['_source']['strItemTitleKeywords'],hit['_source']['bitHasLocation'],hit['_source']['strOpinon'],hit['_source']['strObjSubj'],hit['_source']['strSGML'],hit['_source']['strLocation'],hit['_source']['strNames'],hit['_source']['geoLat'],hit['_source']['geoLong'],hit['_source']['strURLType'],hit['_source']['strImageURL'],hit['_source']['strIOFileName'],hit['_source']['strEmails'],hit['_source']['bitHasEmails'],hit['_source']['strPhones'],hit['_source']['bitHasPhones'],hit['_source']['bitHasNames'],hit['_source']['bitHasMoney'],hit['_source']['strMoney'],hit['_source']['bitHasNumerics'],hit['_source']['strNumerics'],hit['_source']['bitHasQuestions'],hit['_source']['strURLS'],hit['_source']['bitHasURLS'],hit['_source']['bitHasMetrics'],hit['_source']['strSC'],hit['_source']['strWC'],hit['_source']['strWPS'],hit['_source']['strSYC'],hit['_source']['strSPW'],hit['_source']['strLD'],hit['_source']['strKGL'],hit['_source']['strFRE'],hit['_source']['strGFI'],hit['_source']['bitHasMisc'],hit['_source']['strMiscOne'],hit['_source']['strMiscTwo'],hit['_source']['strMiscThree'],hit['_source']['strMiscFour'],hit['_source']['strMiscFive']])
    except (UnicodeEncodeError) as ex:
        continue
f.close()
