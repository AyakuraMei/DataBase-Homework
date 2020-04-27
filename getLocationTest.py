#test file

import requests
import pprint
import json


location_dict = dict()
return_list = list()
longtitude = 120.04925573429551
latitude = 27.315590522490712
file_name = 'locationTest.json'
file = open(file_name, 'w')

while longtitude < 124:
    location_dict[str(longtitude)] = str(latitude)
    longtitude = longtitude + 0.1
    latitude = latitude + 0.1

for key in location_dict:
    url = 'http://ditu.amap.com/service/regeo?longitude=' + str(key) + \
          '&latitude=' + str(location_dict[key])
    r = requests.get(url)
    return_list.append(r)

for i in return_list:
    #pprint.pprint(i.json())
    json_data = json.dumps(i.json())
    file.write(json_data + '\n')

file.close()