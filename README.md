# pynest
I created this python Nest Thermostat api after looking at others that were around, and not really liking them.  I learned a lot by reading several other nest APIs for both python and php.

#What is it?
This is a simple api to connect to a nest Thermostat.  In order to use it, you will need a nest thermostat, and an account at nest.com.

#How do I use it?
Once you have the pynest.py file, you can connect to the site like this:
```python
myNest = pynest.Nest("myusername","mypassword")
```
To list the structures or houses that you have attached to your account (most people probably have only one, but I needed to account for many):
```python
myHouses = myNest.list_structures()
print myHouses
```
Will gve you:
{u'Some GUID Here':u'Name assigned to this structure'}

Then you can get the thermostats that are in that structure:
```python
therms = myNest.list_thermostats('Some GUID Here')
```
Where the Guid is the ID that is returned as the key in the dictionary returned by list_structures.

Then you can get a temperature for a thermostat by passing an ID that comes in from the list that is now in therms:
```python
print myNest.get_temp('device id')
```
You can add an optional argument to get_temp called units to specify C or F, by default the temperature is in degrees C.

#What did I read?
* https://github.com/gboudreau/nest-api
* https://github.com/ablyler/nest-php-api
* https://github.com/smbaker/pynest

All I really wanted was an API, so feel free to use it, let me know if you do!
