#!/usr/bin/env python3

from datetime import datetime
import argparse
import requests
import pickle
import json
import os
from sty import fg, rs, bg
from math import floor
from appdirs import AppDirs

LOCATION_URL = "http://www.cleardarksky.com/t/chart_prop00.txt"
BASE_URL = "http://www.cleardarksky.com/txtc"
UNICODE_BLOCK = u'\u25a0'
TIME_COLORS = [10,11,9,14]

APP_NAME = "ClearSkyCharts"
APP_AUTHOR = "mohsaad"
STATE_FILENAME = 'current_location.state'

BACKGROUND_COLOR = 233
HEADER_COLOR = 202


class ClearDarkSkyData():

    def __init__(self):
        self.locations_by_state = {}
        self.locations_by_city = {}
        self.dirs = AppDirs(APP_NAME, APP_AUTHOR)
        
        if not os.path.exists(self.dirs.user_cache_dir):
            os.makedirs(self.dirs.user_cache_dir)

        # Try to load a state file. If failure, make sure to run setting program.
        try:
            self.location, self.location_name = pickle.load(open('{}/{}'.format(self.dirs.user_cache_dir, STATE_FILENAME), 'rb'))
        except Exception as e:
            self.location = None
            self.location_name = ''

        self.location_download_path = self.dirs.user_cache_dir + '/sky_locations.txt'
        self._build_or_load_location_map()
        self.counter = 0

    def set_location_by_state(self):
        while True:
            state = input("Enter your state: ")
            if self._search_locations_by_state(state):
                break
            print("State not found!")


        key = state.lower()
        for i in range(0, len(self.locations_by_state[key])):
            print("({}): {}".format(i, self.locations_by_state[key][i][1]))

        while True:
            try:
                choice = input("Enter your choice here: ")
                self.location = self.locations_by_state[key][int(choice)][0]
                self.location_name = self.locations_by_state[key][int(choice)][1]
                break
            except (ValueError, IndexError) as e:
                print("Invalid choice!")

        pickle.dump((self.location, self.location_name), open('{}/{}'.format(self.dirs.user_cache_dir, STATE_FILENAME), 'wb'))

    def set_location_by_city(self):
        cities = []
        while True:
            city = input("Enter your city: ")
            for key in self.locations_by_city:
                if city.lower() in key:
                    cities.append(key)
            
            if len(cities) > 0:
                break
            print("No cities found!")

        for i in range(0, len(cities)):
            print("({}): {}".format(i, self.locations_by_city[cities[i]][1]))

        while True:
            try:
                choice = input("Enter your choice here: ")
                self.location = self.locations_by_city[cities[int(choice)]][0]
                self.location_name = self.locations_by_city[cities[int(choice)]][1]
                break
            except (ValueError, IndexError) as e:
                print("Invalid choice!")

        pickle.dump((self.location, self.location_name), open('{}/{}'.format(self.dirs.user_cache_dir, STATE_FILENAME), 'wb'))

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
        f = open(self.location_download_path, encoding = "ISO-8859-1")
        for line in f:
            key, state, location = line.split('\n')[0].split('|')
            if not state.lower() in self.locations_by_state:
                self.locations_by_state[state.lower()] = [(key, location)]
            else:
                self.locations_by_state[state.lower()].append((key, location))

            self.locations_by_city[location.lower()] = (key, location)

    def _search_locations_by_state(self, state):
        if not state.lower() in self.locations_by_state:
            return False
        else:
            return True

    def download_sky_chart(self, key):
        url = '{}/{}csp.txt'.format(BASE_URL, key)
        r = requests.get(url)
        filename = "{}/{}.txt".format(self.dirs.user_cache_dir, key)

        open(filename, 'wb').write(r.content)

        return filename

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

    def print_transparency_values(self, transparency_values, name, state):
        # Initialize strings
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M")

        tens_digit_str = fg(10) + "{0: <15}".format(current_date) + fg.rs
        ones_digit_str = fg(11) + "{0: <15}".format(current_time) + fg.rs
        transparency_str = fg(15) + "{0: <15}".format("Transparency:") + fg.rs
        cloud_str = fg(15) + "{0: <15}".format("Cloud Cover:") + fg.rs
        seeing_str = fg(15) + "{0: <15}".format("Seeing:") + fg.rs
        darkness_str = fg(15) + "{0: <15}".format("Darkness:") + fg.rs

        # Go through each data point
        for key in sorted(transparency_values):
            cloud_add = int(transparency_values[key][0]) * 23
            trans_add = int(transparency_values[key][1]) * 46
            see_add = int(transparency_values[key][2]) * 46
            
            if int(key.hour) == 0:
                self.counter += 1

            tens_digit_str += fg(TIME_COLORS[self.counter]) + str(key.hour).zfill(2)[0] + fg.rs + " "
            ones_digit_str += fg(TIME_COLORS[self.counter]) + str(key.hour).zfill(2)[1] + fg.rs + " "
            cloud_str += fg(255 - cloud_add, cloud_add, 0) + UNICODE_BLOCK + fg.rs + " "
            transparency_str += fg(255 - trans_add, trans_add, 0) + UNICODE_BLOCK + fg.rs + " "
            seeing_str += fg(255 - see_add, see_add, 0) + UNICODE_BLOCK + fg.rs + " "
            
            if len(transparency_values[key]) > 5:
                darkness_add = floor(float(transparency_values[key][5]) * 24 + 104)
            else:
                darkness_add = 255

            darkness_str += fg(255 - darkness_add, 255 - darkness_add, 255 - darkness_add) + UNICODE_BLOCK + fg.rs + " "

        string_length = (15 + len(transparency_values.keys()) * 2)       
        header = bg(BACKGROUND_COLOR) + fg(HEADER_COLOR) + '-' * string_length  + fg.rs + bg.rs
        title_string = bg(BACKGROUND_COLOR) + fg(HEADER_COLOR) + " Clear Sky Chart for {}, {} ".format(name, state).center(string_length, '-') + fg.rs + bg.rs
        print(header)
        print(title_string)
        print(header)
        print(bg(BACKGROUND_COLOR) + tens_digit_str + bg.rs)
        print(bg(BACKGROUND_COLOR) + ones_digit_str + bg.rs)
        print(bg(BACKGROUND_COLOR) + cloud_str + bg.rs)
        print(bg(BACKGROUND_COLOR) + transparency_str + bg.rs)
        print(bg(BACKGROUND_COLOR) + seeing_str + bg.rs)
        print(bg(BACKGROUND_COLOR) + darkness_str + bg.rs)

    def sky_chart_pipeline(self):
        if self.location is None:
            self.set_location_by_city()

        state = self.location[-2:]
      
        link = self.download_sky_chart(self.location)
        vals = self.interpret_sky_chart(link)
        self.print_transparency_values(vals, self.location_name, state)
