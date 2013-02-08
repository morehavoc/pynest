__author__ = 'cmoravec'

class NestException(Exception):
    pass
class NestHttpError(NestException):
    pass
class NestInvalidResponse(NestHttpError):
    pass
class NestUnauthorized(NestException):
    pass


class InvalidUsernamePassword(NestException):
    pass

import urllib2, urllib

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise NestException("Unable to load a json library, make sure either json or simplejson is installed.")


class Nest(object):

    def __init__(self, username, password, access_token="", user_id="", transport_url="https://home.nest.com/", data=""):
        """Creates a nest object using the specified username and password."""
        self._username = username
        self._password = password
        self._authenticated = False
        self._access_token = access_token
        self._user_id = user_id
        self._transport_url = transport_url
        self._data = data
        if self._access_token == "":
            self._login()
            self.refresh()

    def refresh(self):
        data = self._sendPOST("/v2/mobile/user."+self._user_id)
        self._data = data

    def list_structures(self):
        """Returns a dictionary where the key is the structureID and the value is the user defined name of the structure"""
        resultList = {}
        for structName, structData in self._data["structure"].iteritems():
            resultList[structName] = structData["name"]
        return resultList

    def list_thermostats(self,structureID):
        """For the specified structureID, lists the thermostats there.  Returns a list of thermostat ids."""
        if self._data["structure"].has_key(structureID):
            return [d.split(".")[1] for d in self._data["structure"][structureID]["devices"]]
        else:
            return []

    def get_thermostat_details(self,thermostatID):
        """For the specified thermostatID, returns a dictionary of settings for that thermostat."""
        if self._data["device"].has_key(thermostatID):
            return self._data["device"][thermostatID]
        else:
            return {}


    def get_temp(self,thermostatID,units="C"):
        """For the specified thermostatID, returns the temperature.  IF units is C, then in celsius, if F
            then fahrenheit, for anything else, Celsius. Returns -9999 if the thermostatID is not valid."""
        if self._data["shared"].has_key(thermostatID) == False:
            return -9999
        if units.lower() == "f":
            return self._convertCelsiusToFahrenheit(self._data["shared"][thermostatID]["current_temperature"])
        else:
            return self._data["shared"][thermostatID]["current_temperature"]


    def _convertFahrenheitToCelsius(self,temp):
        """Converts the temperature given from Fahrenheit to Celsius"""
        return float(temp-32) * float(5.0/9/0)
    def _convertCelsiusToFahrenheit(self,temp):
        """Converts the temperature given from Celsius to Fahrenheit"""
        return float(temp)*float(9.0/5.0) + 32

    def _login(self):
        try:
            data = self._sendPOST("user/login",{"username":self._username,"password":self._password},{})
            self._access_token = data.get("access_token","")
            self._user_id = data.get("userid","")
            self._transport_url = data.get("urls",{}).get("transport_url",self._transport_url)
            self._authenticated = True
        except urllib2.HTTPError:
            raise NestUnauthorized("Unauthorized, try a different password.")

    def _loadJson(self,response):
        try:
            if hasattr(json,"loads"):
                return json.loads(response)
            else:
                return json.read(response)
        except Exception as e:
            raise e

            raise NestInvalidResponse("An error occurred while converting the json response.")

    def _sendPOST(self, url_end_point, parameters=None, headers={}):
        _headers = headers
        _headers["user-agent"]="Nest/1.1.0.10 CFNetwork/548.0.4"
        if self._authenticated:
            _headers["Authorization"]="Basic "+self._access_token
            _headers["X-nl-user-id"] = self._user_id
            _headers["X-nl-protocol-version"] = "1"
        if parameters is not None:
            _data = urllib.urlencode(parameters)
        else:
            _data = None
        try:
            _request = urllib2.Request(self._transport_url+url_end_point,data=_data,headers=_headers)
            _response = urllib2.urlopen(_request).read()
        except Exception as e:
            raise NestHttpError("An error occurred %s"%(str(e)))
        return self._loadJson(_response)





def main():
    n = Nest("username","password")
    print n.list_structures()
    for s in n.list_structures().keys():
        print n.list_thermostats(s)
        for t in n.list_thermostats(s):
            print n.get_thermostat_details(t)
            print n.get_temp(t)
            print n.get_temp(t,"F")
    print n

if __name__ == '__main__':
    main()