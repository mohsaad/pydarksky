#!/usr/bin/env python3

from datetime import datetime
import argparse
import requests
import json
import os
from sty import fg, rs
from math import floor

LOCATION_URL = "http://www.cleardarksky.com/t/chart_prop00.txt"
BASE_URL = "http://www.cleardarksky.com/txtc"
UNICODE_BLOCK = u'\u25a0'

class ClearDarkSkyData():

    def __init__(self):
        self.locations = {}
        self.location_download_path = '/tmp/sky_locations.txt'
        self._build_or_load_location_map()

    def _check_for_existing_locations(self):
        if os.path.exists(self.location_download_path):
            return True

        return False

    def _download_locations(self):
        if not self._check_for_existing_locations():
            r = requests.get(LOCATION_URL)
            open(self.location_download_path, 'wb').write(r.content)


    def _build_or_load_location_map(self):
        self._download_locations()
        f = open('/tmp/sky_locations.txt', encoding = "ISO-8859-1")
        for line in f:
            key, state, location = line.split('\n')[0].split('|')
            if not state.lower() in self.locations:
                self.locations[state.lower()] = [(key, location)]
            else:
                self.locations[state.lower()].append((key, location))

    def search_locations(self, state):
        if not state.lower() in self.locations:
            return None
        else:
            return self.locations[state.lower()]

    def download_sky_chart(self, key):
        url = '{}/{}csp.txt'.format(BASE_URL, key)
        r = requests.get(url)
        open('/tmp/{}.txt'.format(key), 'wb').write(r.content)

        return "/tmp/{}.txt".format(key)

    def interpret_sky_chart(self, key_file):
        f = open(key_file, 'r')
        title = f.readline().strip(' ').split('=')[1].strip('"')
        version = f.readline().strip(' ').split('=')[1].strip('"')
        UTC_offset = f.readline().strip(' ').split('=')[1]
          
        transparency_values = {}
  
        # Skip the next 4 lines.
        for i in range(0, 4):
          f.readline()
        
        line = 'n'
        while line != None: 
            line = f.readline()
            if line.split('\n')[0] == ')':
                break

            filter_table = dict.fromkeys(map(ord, '"\t\n()'), None)
            values = line.translate(filter_table).split(',')[0:-2]
            datetime_obj = datetime.strptime(values[0], '%Y-%m-%d %H:%M:%S')
            transparency_values[datetime_obj] = values[1:-1]

        # Get all data after next 5 lines.
        
        for i in range(0, 5):
            f.readline()

        while line != None:
            line = f.readline()
            if line.split('\n')[0] == ')':
                break

            values = line.translate(filter_table).split(',') 
            datetime_obj = datetime.strptime(values[0], '%Y-%m-%d %H:%M:%S')
      
            if datetime_obj in transparency_values:
                for item in values[1:-1]:
                    transparency_values[datetime_obj].append(item)

        return transparency_values

    def print_transparency_values(self, transparency_values):
        tens_digit_str = ""
        ones_digit_str = ""
        cloud_str = ""
        transparency_str = ""
        seeing_str = ""
        darkness_str = ""


        for key in sorted(transparency_values):
            cloud_add = int(transparency_values[key][0]) * 23
            trans_add = int(transparency_values[key][1]) * 46
            see_add = int(transparency_values[key][2]) * 46
            
            tens_digit_str += str(key.hour).zfill(2)[0] + " "
            ones_digit_str += str(key.hour).zfill(2)[1] + " "
            cloud_str += fg(255 - cloud_add, cloud_add, 0) + UNICODE_BLOCK + fg.rs + " "
            transparency_str += fg(255 - trans_add, trans_add, 0) + UNICODE_BLOCK + fg.rs + " "
            seeing_str += fg(255 - see_add, see_add, 0) + UNICODE_BLOCK + fg.rs + " "
            
            if len(transparency_values[key]) > 5:
                darkness_add = floor(float(transparency_values[key][5]) * 24 + 104)
            else:
                darkness_add = 255

            darkness_str += fg(255 - darkness_add, 255 - darkness_add, 255 - darkness_add) + UNICODE_BLOCK + fg.rs + " "

        
        print("              {}".format(tens_digit_str))
        print("              {}".format(ones_digit_str))
        print("Cloud Cover:  {}".format(cloud_str))
        print("Transparency: {}".format(transparency_str))
        print("Seeing:       {}".format(seeing_str))
        print("Darkness:     {}".format(darkness_str))

def main():
    parser = argparse.ArgumentParser(description="Get clear sky charts and display them in the terminal")
    parser.add_argument('--search', help='Search for a location')

    c = ClearDarkSkyData()
    link = c.download_sky_chart('SanFranCA')
    vals = c.interpret_sky_chart(link)
    c.print_transparency_values(vals)

if __name__ == '__main__':
    main()
