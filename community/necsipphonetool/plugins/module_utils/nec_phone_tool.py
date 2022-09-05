import re
import requests
import sys

# Ignore bad ssl certs in requests
requests.packages.urllib3.disable_warnings()

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

# Logon to phone
def logOnPhone(hostName, logOnName, logOnPassword, bypassProxy, verifyCerts):
    #if (bypassProxy):
    #    pass
    logOnResponse = requests.get(hostName + '/index.cgi?username={}&password={}'.format(logOnName, logOnPassword), verify=verifyCerts)
    # Extract session id from logon response with regex and return it
    sessionId = re.search(r'session=(.{4})"', logOnResponse.text).group(1)
    return logOnResponse, sessionId
       
# Log off phone
def logOffPhone(hostName, sessionId, bypassProxy, verifyCerts):
    if (bypassProxy):
        pass
    logOffResponse = requests.get(hostName + '/index.cgi?session={}&set=all'.format(sessionId), verify=verifyCerts)
    return logOffResponse
	
# Log off phone
def setFactoryValues(hostName, sessionId, bypassProxy, verifyCerts):
    if (bypassProxy):
        pass
    factoryValuesResponse = requests.get(hostName + '/index.cgi?session={}&data_clear=4110430'.format(sessionId), verify=verifyCerts)
    return factoryValuesResponse

# Set single paramater on phone
def setParameter(hostName, sessionId, parameter, value, bypassProxy, verifyCerts):
	if (bypassProxy):
		pass
	setParameterResponse = requests.get(hostName + '/index.cgi?session={}&set={}&item={}'.format(sessionId, parameter, value), verify=verifyCerts)
	return setParameterResponse

def main():
    print('\n\tDo not run me.\n\tImport me.\n')

# run main if not imported
if __name__ == '__main__':
    main()
