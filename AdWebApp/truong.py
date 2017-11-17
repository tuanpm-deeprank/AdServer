# importing the requests library
import requests
 
# api-endpoint
URL = "http://10.12.11.161:5000/getAds"
#URL = "http://google.com"
 
# location given here
paper = "abc"
 
# defining a params dict for the parameters to be sent to the API
PARAMS = {"paper":paper}
 
# sending get request and saving the response as response object
headers = {'Content-type': 'application/json'}
r = requests.post(url = URL, json = PARAMS, headers=headers)
print r
print 'aaaaaaaaaaaaaaaaaaaaaa'
 
# extracting data in json format
data = r.json()
 
print data
 
# extracting latitude, longitude and formatted address 
# of the first matching location
#latitude = data['results'][0]['geometry']['location']['lat']
#longitude = data['results'][0]['geometry']['location']['lng']
#formatted_address = data['results'][0]['formatted_address']
 
# printing the output
#print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
#      %(latitude, longitude,formatted_address))
