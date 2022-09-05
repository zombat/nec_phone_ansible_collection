#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from itertools import product
import nec_phone_tool
import pprint
import re
import socket
import sys
import time

parser = argparse.ArgumentParser(prog='nec_cli_tool.py', description='NEC CLI Tool for')
# DT750 has TCP 80(http), 81 (hosts2-ns), and 82 (xfer) open by default.
# DT820 also has TCP 443 (https)

parser.add_argument('--logOnName', type=str, help='Logon name', default='ADMIN')
parser.add_argument('--logOnPassword', type=str, help='Logon password', default='6633222')
parser.add_argument('--hostName', type=str, nargs='+', help='Host name', required=True)
parser.add_argument('--insecureAlways', action='store_true', help='Use http:// instead of https://')
parser.add_argument('--insecureSecondary', action='store_true', help='Use http:// if https:// fails')
parser.add_argument('--factoryValues', action='store_true', help='Set device to factory values')
parser.add_argument('--forceReboot', action='store_true', help='Force reboot')
parser.add_argument('--setLLDP', type=str, help='Enable or disable LLDP', choices=['enable', 'disable'])
parser.add_argument('--testCreds', action='store_true', help='Test credentials')
parser.add_argument('--v', action='store_true', help='Verbose output')
parser.add_argument('--vv', action='store_true', help='Very Verbose output')
args = parser.parse_args()

if args.insecureAlways:
    httpSchema = 'http://'
else:
    httpSchema = 'https://'


# May use this in the future if I decide to remove requirement for hostName
# def checkArgs(hostName, logOnName, logOnPassword):
#     # Ensure variables are defined
#     if hostName == 'None':
#         print('\n\tHost name is not defined.\n')
#         sys.exit(1)

def logOn(hostName, logOnName, logOnPassword, loopCheck):
    try:
        logOnResponse, sessionId = nec_phone_tool.logOnPhone(hostName, logOnName, logOnPassword, False, False)
        if logOnResponse.status_code == 200 and sessionId:
            if args.vv:
                  print('\tLogon successful for session {} on host {}'.format(sessionId, hostName))
            elif args.v:
                print('\tLogon successful')
            return True, sessionId
        else:
            if args.vv:
                print('\tLogoff failed for session {} on host {}'.format(sessionId, hostName))
            else:
                print('\tLogoff failed')
            return False, 'null'
    except:
        if args.insecureSecondary and loopCheck == 0:
            # Replace https:// with http:// and try again
            print('\tDegrading protocol to http://')
            hostName = hostName.replace('https://', 'http://')
            return logOn(hostName, logOnName, logOnPassword, 1)
        else:
            print('\tLogon failed')
            return False, 'null'

def logOff(hostName, sessionId, loopCheck):
    try:
        logOffResponse = nec_phone_tool.logOffPhone(hostName, sessionId, False, False)
        if logOffResponse.status_code == 200:
            if args.vv:
                print('\tLogoff successful for session {} on host {}'.format(sessionId, hostName))
            elif args.v:
                print('\tLogoff successful')
        else:
            if args.vv:
                print('\tLogoff failed for session {} on host {}'.format(sessionId, hostName))
                print(logOffResponse.status_code)
                print(logOffResponse.text)
            else:
                print('\tLogoff failed')
    except:
        if args.insecureSecondary and loopCheck == 0:
            # Replace https:// with http:// and try again
            print('\tDegrading protocol to http://')
            hostName = hostName.replace('https://', 'http://')
            logOff(hostName, sessionId, 1)
        else:
            print('\tLogoff failed')

def factoryValues(hostName, sessionId, loopCheck):
    try:
        factoryValuesResponse = nec_phone_tool.setFactoryValues(hostName, sessionId, False, False)
        if factoryValuesResponse.status_code == 200:
            if args.vv:
                print('\tSet Factory values successful for session {} on host {}'.format(sessionId, hostName))
            elif args.v:
                print('\tSet Factory values successful')
        else:
            if args.vv:
                print('\tSet Factory values failed for session {} on host {}'.format(sessionId, hostName))
                print(factoryValuesResponse.status_code)
                print(factoryValuesResponse.text)
            else:
                print('\tSet Factory values failed')
    except:
        if args.insecureSecondary and loopCheck == 0:
            # Replace https:// with http:// and try again
            print('\tDegrading protocol to http://')
            hostName = hostName.replace('https://', 'http://')
            logOff(hostName, sessionId, 1)
        else:
            print('\tSet Factory values failed')

def setSingleParamItem(hostName, sessionId, paramItem, paramValue, loopCheck):
    if paramValue == 'enable':
        paramValue = '1'
    elif paramValue == 'disable':
        paramValue = '0'
    try:
        setSingleParamItemResponse = nec_phone_tool.setParameter(hostName, sessionId, paramItem, paramValue, False, False)
        if setSingleParamItemResponse.status_code == 200:
            if args.vv:
                print('\tSet single param item successful for session {} on host {}'.format(sessionId, hostName))
                print('\tParam: {} Value: {}'.format(paramItem, paramValue))
            elif args.v:
                print('\tSet single param item successful')
        else:
            if args.vv:
                print('\tSet single param item failed for session {} on host {}'.format(sessionId, hostName))
                print('\tParam: {} Value: {}'.format(paramItem, paramValue))
                print(setSingleParamItemResponse.status_code)
                print(setSingleParamItemResponse.text)
            else:
                print('\tSet single param item failed')
    except:
        if args.insecureSecondary and loopCheck == 0:
            # Replace https:// with http:// and try again
            print('\tDegrading protocol to http://')
            hostName = hostName.replace('https://', 'http://')
            setSingleParamItem(hostName, sessionId, paramItem, paramValue, 1)
        else:
            print('\tSet single param item failed')

def main():
    if httpSchema == 'http://':
        print('\n\tWARNING: Using http://. This is not secure. Use https:// if possible.')
    for host in args.hostName:
        hostName = httpSchema + host
        if args.factoryValues:
            if args.v or args.vv:
                print('\tFactory Value Settings')
            logonGood, sessionId = logOn(hostName, args.logOnName, args.logOnPassword, 0)                
            if logonGood:
                factoryValues(hostName, sessionId, 0)
                logOff(hostName, sessionId, 0) 
        elif args.forceReboot:
            if args.v or args.vv:
                print('\tForce reboot')
            logOff(hostName, 'null', 0)
        elif args.testCreds:
            if args.v or args.vv:
                print('\tTest credentials') 
            logonGood, sessionId = logOn(hostName, args.logOnName, args.logOnPassword, 0)
            if logonGood:
                logOff(hostName, sessionId, 0)
        elif args.setLLDP:
            if args.v or args.vv:
                print('\tSet LLDP') 
            logonGood, sessionId = logOn(hostName, args.logOnName, args.logOnPassword, 0)
            if logonGood:
                setSingleParamItem(hostName, sessionId, '44604f3', args.setLLDP, 0)
                logOff(hostName, sessionId, 0)
        else:
            print('\n\tNo actions selected\n')
        time.sleep(0.5)


# Do the thing!
if __name__ == '__main__':
    main()    
