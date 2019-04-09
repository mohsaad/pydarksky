#!/usr/bin/env python3

import argparse
from .csk import ClearDarkSkyData

def main():
    parser = argparse.ArgumentParser(description="Get clear sky charts and display them in the terminal")
    parser.add_argument('--search-by-state', action='store_true', help='Search for a location by state')
    parser.add_argument('--search-by-city', action='store_true', help='Search for a location by state')
  
    args = parser.parse_args()

    location_set = False
    c = ClearDarkSkyData()
    
    if args.search_by_state and args.search_by_city:
        c.set_location_by_city()
        location_set = True

    if args.search_by_state and not location_set:
        c.set_location_by_state()

    if args.search_by_city and not location_set:
        c.set_location_by_city()

    c.sky_chart_pipeline()

if __name__ == '__main__':
    main()
