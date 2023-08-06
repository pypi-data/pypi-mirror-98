from __future__ import print_function

import logging
import requests
import json
import csv
import clarus
from clarus.api_config import ApiConfig
from six import StringIO

UTIL_SERVICE        = 'Util'

# Response Headers

STATS       = 'X-Clarus-Stats'
WARNINGS    = "X-Clarus-Messages"
MESSAGES    = "messages"

# Request Stats

GRID_TOTAL   = 'GridTotal'
REQUEST_ID   = 'RequestId'
GRID_ID      = 'GridId'
CALC_TIME    = 'CalcTime'
TASK_TIME    = 'TaskTime'
NUM_MTM      = 'NumMTM'
NUM_TRADES   = 'NumTrades'
NUM_WARNINGS = 'NumWarnings'

logger = logging.getLogger(__name__)

def urlRequest(url, params):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Calling url " + url)
        logger.debug("With params " + json.dumps(params))
        
    headers = {'Content-Type': 'application/json', 'User-Agent' : ApiConfig.user_agent}

    results = requests.post(url, data=json.dumps(params), headers=headers, auth=(ApiConfig.api_key, ApiConfig.api_secret) )
       
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug ('Request Time %0.2f s' % (results.elapsed.seconds+(results.elapsed.microseconds/1000000.0)))
        logger.debug ('CalcTime %s ms' % (getStat(results, CALC_TIME)))
        logger.debug ('HTTP status %s' % (results.status_code))
        logger.debug ('HTTP headers %s' % (results.headers))
    return results
        
def request(serviceCategory, service, output=None, **params):
    if output is None:
        output = ApiConfig.default_output_type
    return urlRequest(getURL(serviceCategory, service, output), params)

def gridRequest(params, output=None):
    if output is None:
        output = ApiConfig.default_output_type
    return urlRequest(getURL(UTIL_SERVICE, "Grid", output), params)
   
def getURL(serviceCategory, service, output):
    url = ApiConfig.base_url + serviceCategory + '/' + service + '.' + output
    ticket = ApiConfig.client_ticket
    if ticket is not None:
        if '?' in url:
            url += '&ticket=' + ticket
        else:
            url += '?ticket=' + ticket
    return url


def pivot(grid, rowAxis='Currency', colAxis='SubType', ccy='USD', view='Latest', output=None):
    return gridRequest({'GridId':getGridId(grid), 'Row':rowAxis, 'Col':colAxis, 'reportCcy': ccy, 'View':view}, output)

def filter(grid, filter, output=None):
    return gridRequest({'GridId':getGridId(grid), 'filter':filter}, output)

def drilldown(grid, row='Total', col='Total', view='Default', reportCcy=None, output=None):
    return gridRequest({'GridId':getGridId(grid), 'DrilldownRow':row, 'DrilldownCol':col, 'DrilldownView':view, 'reportCcy':reportCcy}, output)
         
def printRequestTime(r):
    print ('Request Time %0.2fs' %(getRequestTime(r)))
    
def getRequestTime(r):
    return (r.elapsed.seconds+(r.elapsed.microseconds/1000000.0))
        
def getStats(results):
    if STATS in results.headers:
        return dict((k.strip(), v.strip()) for k,v in (item.split('=') for item in results.headers.get(STATS).split(';')))
    else:
        return {}

def getWarnings(results):
    return results.headers.get(WARNINGS);

def getStat(results, stat):
    return getStats(results).get(stat)
    
def getTotal(results):
    return getStat(results, GRID_TOTAL)
            
def getRequestId(results):
    return getStat(results, REQUEST_ID)
    
def getGridId(results):
    return getStat(results, GRID_ID)
   
def printJSON(results):
    print(json.dumps(json.loads(results), sort_keys=True, indent=2))
    
def printResults(response):
    if (response.status_code!=200):
        try:
            error = json.loads(response.text)[MESSAGES][0]
        except ValueError:
            error = response.text
        print("Request HTTP Error " + str(response.status_code) + " : "  + error)
    elif JSON in response.headers.get('content-type'):
        printJSON(response.text)
    else :
        print (response.text)

def printStats(response):
    print(response.headers.get(STATS))

def printStat(response, statId):
    stat = getStat(response, statId)
    if stat==None:
        print("No " + statId)
    else:
        print(statId + ' ' + stat)
    
def printWarnings(results):
    s = results.headers.get(WARNINGS)
    if s==None:
        print ("No Warnings")
    else:
        print(s.replace(";", "\n"))

def toString(response):
    if (response.status_code!=200):
        warnings = response.headers.get(WARNINGS)
        if (warnings is not None):
            return warnings.replace(";", "\n")
        else:
            return response.text
    else:
        content_type = response.headers.get('Content-Type')
        if (content_type is not None):
            if (content_type.lower() == 'text/csv'):
                return toCsvString(response)
            if (content_type.lower() == 'text/tsv'):
                return toTsvString(response)
            if (content_type.lower() == 'application/json'):
                return toJsonString(response)
            return response.text
        else:
            return response.text
        
def toJsonString(response):
    return json.dumps(json.loads(response.text), sort_keys=True, indent=2)

def toCsvString(response):
    return response.text

def toTsvString(response, delimiter='\t'):
    return response.text