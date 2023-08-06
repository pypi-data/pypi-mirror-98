import clarus.services

def defaultresources(output=None, **params):
    return clarus.services.api_request('CCP', 'DefaultResources', output=output, **params)

def rfrvolume(output=None, **params):
    return clarus.services.api_request('CCP', 'RFRVolume', output=output, **params)

def volume(output=None, **params):
    return clarus.services.api_request('CCP', 'Volume', output=output, **params)

