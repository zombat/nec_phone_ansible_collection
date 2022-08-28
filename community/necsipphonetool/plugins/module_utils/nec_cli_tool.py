import argparse
import nec_phone_tool
import pprint
import re
import sys

# Set variables
logOnName = ''
logOnPassword = ''
httpSchema = 'http://'
parser = argparse.ArgumentParser(prog='nec_cli_tool.py', description='NEC CLI Tool for')
parser.add_argument('--logOnName', type=str, help='Logon name', required=True)
parser.add_argument('--logOnPassword', type=str, help='Logon password', required=True)
parser.add_argument('--hostName', type=str, help='Host name', required=True)
parser.add_argument('--forceReboot', action='store_true', help='Force reboot')
parser.add_argument('--testCreds', action='store_true', help='Test credentials')
args = parser.parse_args()

hostName = httpSchema + args.hostName

def checkArgs(hostName, logOnName, logOnPassword):
    # Ensure variables are defined
    if hostName == 'None':
        print('\n\tHost name is not defined.\n')
        sys.exit(1)

def main():    
    if(args.forceReboot):
        print('\n\tForce reboot')
        logOff(hostName, 'null')
        sys.exit(1)
        
    if(args.testCreds):
        print('\n\tTest credentials')
        logonGood, sessionId = logOn(hostName, args.logOnName, args.logOnPassword)
        if logonGood:
            print('\tLogon successful\n')
            print('\tSession Id: {}'.format(sessionId))
            logOff(hostName, sessionId)
            sys.exit(1)
        else:
            print('\tLogon failed')
            sys.exit(1)
    
def logOn(hostName, logOnName, logOnPassword):
    try:
        logOnResponse, sessionId = nec_phone_tool.logOnPhone(hostName, logOnName, logOnPassword, False, False)
        if logOnResponse.status_code == 200 and sessionId:
            return True, sessionId
        else:
            return False, 'null'
    except:
        return False, 'null'
    
def logOff(hostName, sessionId):
    try:
        logOffResponse = nec_phone_tool.logOffPhone(hostName, sessionId, False, False)
        if logOffResponse.status_code == 200:
            print('Logoff successful')
        else:
            print('Logoff failed')
            print(logOffResponse.status_code)
            print(logOffResponse.text)
            sys.exit(1)
    except:
        print('Logoff failed')
        print(logOffResponse.status_code)
        print(logOffResponse.text)
        sys.exit(1)

# Do the thing!
if __name__ == '__main__':
    main()    
