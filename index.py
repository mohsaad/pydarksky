#!/usr/bin/env python

import argparse
import requests
import json
import os

LOCATION_URL = "http://www.cleardarksky.com/t/chart_prop00.txt"
BASE_URL = "http://www.cleardarksky.com/txtc"

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
            open(self.location_download_path, 'w').write(r.content)


    def _build_or_load_location_map(self):
        self._download_locations()
        f = open('/tmp/sky_locations.txt')
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
        open('/tmp/{}.txt'.format(key), 'w').write(r.content)

        return "/tmp/{}.txt".format(key)

    def interpret_sky_chart(self, key_file):
        f = open(key_file, 'r')
        title = f.readline().strip(' ').split('=')[1].strip('"')
        version = f.readline().strip(' ').split('=')[1].strip('"')
        UTC_offset = f.readline().strip(' ').split('=')[1]
          
        transparency_values = []
  
        # Skip the next 4 lines.
        for i in range(0, 4):
          f.readline()

        for line in f:
          if line.split('\n')[0] == ')':
            break
          
          print(line.split('\n')[0])

def main():
    parser = argparse.ArgumentParser(description="Get clear sky charts and display them in the terminal")
    parser.add_argument('--search', help='Search for a location')

    c = ClearDarkSkyData()
    link = c.download_sky_chart('SanFranCA')
    c.interpret_sky_chart(link)

if __name__ == '__main__':
    main()
