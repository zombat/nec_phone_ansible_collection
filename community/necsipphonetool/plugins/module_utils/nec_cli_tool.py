#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import nec_phone_tool
import pprint
import re
import socket
import sys

parser = argparse.ArgumentParser(prog='nec_cli_tool.py', description='NEC CLI Tool for')
# Add enumeration args. Use regex values from logOnName/Password to build wordlist. Use hostName to build scan list.
# DT750 has TCP 80(http), 81 (hosts2-ns), and 82 (xfer) open by default.
# DT820 also has TCP 442 (https)

parser.add_argument('--logOnName', type=str, help='Logon name', required=True)
parser.add_argument('--logOnPassword', type=str, help='Logon password', required=True)
parser.add_argument('--hostName', type=str, nargs='+', help='Host name', required=True)
parser.add_argument('--insecureAlways', action='store_true', help='Use http:// instead of https://')
parser.add_argument('--insecureSecondary', action='store_true', help='Use http:// if https:// fails')
parser.add_argument('--factoryValues', action='store_true', help='Set device to factory values')
parser.add_argument('--forceReboot', action='store_true', help='Force reboot')
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

def logOn(hostName, logOnName, logOnPassword):
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
        if args.insecureSecondary:
            # Replace https:// with http:// and try again
            print('\tDegrading protocol to http://')
            hostName = hostName.replace('https://', 'http://')
            return logOn(hostName, logOnName, logOnPassword)
        else:
            print('\tLogon failed')
            return False, 'null'

def logOff(hostName, sessionId):
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
        if args.insecureSecondary:
            # Replace https:// with http:// and try again
            print('\tDegrading protocol to http://')
            hostName = hostName.replace('https://', 'http://')
            logOff(hostName, sessionId)
        else:
            print('\tLogoff failed for host: {}'.format(hostName))
        

def main():
    if httpSchema == 'http://':
        print('\n\tWARNING: Using http://. This is not secure. Use https:// if possible.')
    for host in args.hostName:
        hostName = httpSchema + host
        if(args.factoryValues):
            if args.v or args.vv:
                print('\tFactory Value Settings')
            logonGood, sessionId = logOn(hostName, args.logOnName, args.logOnPassword)                
            if logonGood:
                logOff(hostName, sessionId) 
        if(args.forceReboot):
            if args.v or args.vv:
                print('\tForce reboot')
            logOff(hostName, 'null')
        elif(args.testCreds):
            if args.v or args.vv:
                print('\tTest credentials') 
            logonGood, sessionId = logOn(hostName, args.logOnName, args.logOnPassword)
            if logonGood:
                logOff(hostName, sessionId)
        else:
            print('\n\tNo actions selected\n')
    

    


# Do the thing!
if __name__ == '__main__':
    main()    
