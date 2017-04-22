#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 09:05 2016
Updated on Fri Apr 07 23:07 2017

@author: timotheeaupetit
"""

import time
    
class City(object):
    def __init__(self, json_data):
        # self.id = json_data['city']['id'] # Not used
        self.name = json_data['city']['name']
        self.country = json_data['city']['country']
        
        self.longitude = json_data['city']['coord']['lon']
        self.latitude = json_data['city']['coord']['lat']
        
        self.data = self.list_measures(json_data['data'])
    
    def list_measures(self, json_data):
        """
        Builds a list of "Measure" objects.
        """
        measures = []
        for measure in json_data:
            measures.append(Measure(measure))
        
        return measures
    
#    def temperature_sequence(self):
#        """
#        Builds a sequence of temperatures
#        """
#        temperatures = []
#        
#        for measure in self.data:
#            temperatures.append(measure.t_morn)
#            temperatures.append(measure.t_day)
#            temperatures.append(measure.t_eve)
#            temperatures.append(measure.t_night)
#        
#        return temperatures
    
    def in_area(self, lat_1, lon_1, lat_2, lon_2):
        """
        Returns true if the city is located in the area, false otherwise.
        An area is a rectangle which 2 opposite corners coordinates 
        are located as follows: lat_1, lon_1, lat_2, lon_2.
        """
        lat = self.latitude
        lon = self.longitude
        
        if lat_1 < lat_2: # check whichever values are the smallest/biggest
            min_lat = lat_1
            max_lat = lat_2
        else:
            min_lat = lat_2
            max_lat = lat_1
        
        if lon_1 < lon_2:
            min_lon = lon_1
            max_lon = lon_2
        else:
            min_lon = lon_2
            max_lon = lon_1       
        
        return ((min_lat <= lat <= max_lat) and (min_lon <= lon <= max_lon))
    
    def is_selected(self, city_list):
        """
        Returns true if a city is in found in city_list, false otherwise
        """
        return self.name in city_list  
    
    def __repr__(self):
        return self.name + ' (' + self.country + ')'
    
###############################################################################
class Measure(object):
    """
    A Measure contain weather data taken at a certain time ('dt')
    """
    def __init__(self, json_data):
        # self.clouds = json_data['clouds']  # Not used
        # self.deg = json_data['deg']  # Not used
        # self.humidity = json_data['humidity']  # Not used
        # self.speed = json_data['speed'] # Not used
        # self.time = json_data['time'] # Not used
        self.date = json_data['dt']
        self.pressure = json_data['pressure']
        
        self.t_morn =   Measure.kelvin_to_celcius(json_data['temp']['morn'])
        self.t_day =    Measure.kelvin_to_celcius(json_data['temp']['day'])
        self.t_eve =    Measure.kelvin_to_celcius(json_data['temp']['eve'])
        self.t_night =  Measure.kelvin_to_celcius(json_data['temp']['night'])
        self.t_min =    Measure.kelvin_to_celcius(json_data['temp']['min'])
        self.t_max =    Measure.kelvin_to_celcius(json_data['temp']['max'])
        
        # self.weather = json_data['weather'] # Not used

    def format_date(self):
        """
        Converts a date (given in seconds since the Epoch) 
        in the format *Y*ear *m*onth *d*ay *H*our *M*inute
        """
        pattern="%Y-%m-%d:%H-%M" # UTC
        
        return time.strftime(pattern, time.gmtime(self.date))
    
    def kelvin_to_celcius(k_temp):
        """
        Converts kelvin degrees to celcius degrees.
        The scale offset is equal to 273.15°.
        """
        return round(float(k_temp - 273.15), 2)
    
    def __repr__(self):
        return 'Measured on: ' + Measure.format_date(self.date)