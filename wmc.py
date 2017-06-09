from os.path import dirname, exists
from time import sleep

import sys
import simplejson as json
import requests
import os

directory = "data/"
tolerance = '0.005'

base = 'https://mapit.mysociety.org/area'
wmc = base + 's/WMC'

if not exists(directory):
    os.mkdir(directory)

r = requests.session()

data = r.get(wmc)

print(data.text)

# handle HTTP 429

if data.status_code == 429:
    print('50 free requests per day used up')
    print('See https://mapit.mysociety.org/pricing/ for details')
    sys.exit()

all = data.json()

for key, area in sorted(all.items()):

    name = area[u'name']

    geojsonurl = base + "/" + key + ".geojson?simplify_tolerance=" + tolerance

    file = directory + key + ".geojson"

    if not exists(file):
        print(key + u',' + name)
#        open F, ">$file";
        with open(file, 'w') as fp:
            poly = r.get(geojsonurl)
#        print F $poly;
            if poly.status_code == 200:
                fp.write(poly.text)
            elif poly.status_code == 429:
                print('50 free requests per day used up')
                print('See https://mapit.mysociety.org/pricing/ for details')
                fp.close()
                os.unlink(file)
                sys.exit()
#        close F;

        sleep(2)
