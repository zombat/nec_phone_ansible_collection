import re
import requests
import sys

# Ignore bad ssl certs in requests
requests.packages.urllib3.disable_warnings()
proxies = {
	'http': 'http://10.4.0.53:5555',
	'https': 'http://10.4.0.53:5555'
}

phoneVariables =  {
	'firstServerSettings': {},
	'eapSupplicant': {},
	'actions': [],
	'auth': {
        'adminPassword': ''
        },
	'configFiles': {
		'DT700': '',
		'DT800': '',
		'DT900': '',
        },
	'clientIPAddress': {},
	'configurationItemCodes': {},
	'configuredDevices': [],
	'debug': False,
	'dump': False,
	'deviceQueue': [],
	'encryption': {},
	'phoneFirmware': {},
	'proxySettings': {},
	'hosts': [],
	'ignoreDevices': [],
	# 'license': {},
	'licenseRequest': {},
	'licenseSettings': {},
	'licenseServerSettings': {},
	'lanPortSettings': {},
	'lldpSettings': {},
	'networkSettings': {},
	'overWriteFirmwareVersion': False,
	'overWriteFirmwareVersionWith': '10.0.0.0',
	'pcPortSettings': {},
	'popUp': {},
	'server': False,
	'serverAddressURI': {},
	'setDataTypes': {
	},
	'sipServerPort': {},
	'spareIPSettings': {},
	'system': {
		'certificateState': {
			'rootCert' : [],
			'clientCert' : []
		},
		'downloadProtocol': '',
		'downloadHttps': False,
		'forceInsecure': False,
		'listArray': [],
		'loop': True,
		'loopTimer': 30000,
		'maxRetries': 3,
		'processCounter': 0,
		'protocolType': 'https',
		'retry': True,
		'retryCounter': 0
	},
	'upgradedDevices': [],
	'voiceRecSettings': {},
	'verbose': False,
}

# Pad digits with leading zeros if needed for two digit numbers
def padDigits(digits):
    if len(digits) == 1:
        digits = '0' + digits
    return digits

# Return date or date/time
def getDateTime(dateTime):
    if dateTime == 'date':
        return '%Y-%m-%d'
    elif dateTime == 'time':
        return '%H:%M:%S'
    elif dateTime == 'dateTime':
        return '%Y-%m-%d %H:%M:%S'
    else:
        return '%Y-%m-%d %H:%M:%S'

# Miliseconds to minutes and seconds
def msToMinSec(ms):
    minutes = int(ms / 60000)
    seconds = int((ms % 60000) / 1000)
    return '{}:{}'.format(padDigits(str(minutes)), padDigits(str(seconds)))

def passSingleParameter(hostName, sessionId, paramKey, paramValue, loopCheck):
    if paramValue == 'enable':
        paramValue = '1'
    elif paramValue == 'disable':
        paramValue = '0'
    try:
        passSingleParamItemResponse = nec_phone_tool.passSingleParameter(hostName, sessionId, paramKey, paramValue, False, False)
        if passSingleParamItemResponse.status_code == 200:
            if args.vv:
                print('\tSet single param item successful for session {} on host {}'.format(sessionId, hostName))
                print('\tParam: {} Value: {}'.format(paramKey, paramValue))
            elif args.v:
                print('\tSet single param item successful')
        else:
            if args.vv:
                print('\tSet single param item failed for session {} on host {}'.format(sessionId, hostName))
                print('\tParam: {} Value: {}'.format(paramKey, paramValue))
                print(passSingleParamItemResponse.status_code)
                print(passSingleParamItemResponse.text)
            else:
                print('\tSet single param item failed')
    except:
        if args.insecureSecondary and loopCheck == 0:
            # Replace https:// with http:// and try again
            print('\tDegrading protocol to http://')
            hostName = hostName.replace('https://', 'http://')
            passSingleParameter(hostName, sessionId, paramKey, paramValue, 1)
        else:
            print('\tSet single param item failed')

# Logon to phone
def logOnPhone(hostName, logOnName, logOnPassword, bypassProxy, verifyCerts, proxies=proxies):
    #if (bypassProxy):
    #    pass
    logOnResponse = requests.get(hostName + '/index.cgi?username={}&password={}'.format(logOnName, logOnPassword), verify=verifyCerts)
    # Extract session id from logon response with regex and return it
    try:
        sessionId = re.search(r'session=(.{4})"', logOnResponse.text).group(1)
    except:
        sessionId = ''
    finally:
        return logOnResponse, sessionId
       
# Log off phone
def logOffPhone(hostName, sessionId, bypassProxy, verifyCerts, proxies=proxies):
    if (bypassProxy):
        pass
    logOffResponse = requests.get(hostName + '/index.cgi?session={}&set=all'.format(sessionId), verify=verifyCerts, proxies=proxies)
    return logOffResponse
	
# Pass single parameter to phone
def passSingleParameter(hostName, sessionId, paramKey, paramValue, bypassProxy, verifyCerts, proxies=proxies):
	if (bypassProxy):
		pass
	passParameterResponse = requests.get(hostName + '/index.cgi?session={}&{}={}'.format(sessionId, paramKey, paramValue), verify=verifyCerts, proxies=proxies)
	return passParameterResponse

# Set single paramater on phone
def setSingleItem(hostName, sessionId, parameter, value, bypassProxy, verifyCerts, proxies=proxies):
	if (bypassProxy):
		pass
	setParameterResponse = requests.get(hostName + '/index.cgi?session={}&set={}&item={}'.format(sessionId, parameter, value), verify=verifyCerts, proxies=proxies)
	return setParameterResponse

# Set single paramater on phone
def setTwoParameters(hostName, sessionId, parameter, value, paramTwoKey, paramTwoValue, bypassProxy, verifyCerts, proxies=proxies):
	if (bypassProxy):
		pass
	setTwoParameters = requests.get(hostName + '/index.cgi?session={}&set={}&item={}&{}={}'.format(sessionId, parameter, value, paramTwoKey, paramTwoValue), verify=verifyCerts, proxies=proxies)
	return setTwoParameters

def main():
    print('\n\tDo not run me.\n\tImport me.\n')

# run main if not imported
if __name__ == '__main__':
    main()
