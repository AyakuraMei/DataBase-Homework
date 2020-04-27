#test file

import json
import pprint

file = open('locate_x_y.json', 'w')
locate = dict()
pos = list()    #latitude, longtitude

with open('locationTest.json', 'r') as f:
    for line in f:
        test_string = line
        #print(test_string)
        string = json.loads(test_string)
        #pprint.pprint(string)
        try:
            for key in string['data']['poi_list']:
                pos.append(float(key['latitude']))
                pos.append(float(key['longitude']))
                locate['desc'] = key['name']
                locate['xy'] = pos
                json_str = json.dumps(locate)
                pprint.pprint(json_str)
                locate.clear()
                pos.clear()
                file.write(json_str + '\n')
        except KeyError:
            continue
