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
        #self.country = json_data['city']['country'] # Not used
        
        self.longitude = json_data['city']['coord']['lon']
        self.latitude = json_data['city']['coord']['lat']
        
        self.data = self.list_measures(json_data['data'])
    
    def list_measures(self, json_data):
        measures = []
        for measure in json_data:
            self.measures.append(Measure(measure))
        
        return measures
        
class Measure(object):
    """
    A Measure contain weather data taken at a certain time ('dt')
    """
    def __init__(self, json_data):
        # self.clouds = json_data['clouds']  # Not used
        # self.deg = json_data['deg']  # Not used
        self.date = Measure.format_date(json_data['dt'])
        # self.humidity = json_data['humidity']  # Not used
        self.pressure = json_data['pressure']
        # self.speed = json_data['speed'] # Not used

        self.t_morn =   Measure.kelvin_to_celcius(json_data['temp']['morn'])
        self.t_day =    Measure.kelvin_to_celcius(json_data['temp']['day'])
        self.t_eve =    Measure.kelvin_to_celcius(json_data['temp']['eve'])
        self.t_night =  Measure.kelvin_to_celcius(json_data['temp']['night'])
        
        # self.weather = json_data['weather'] # Not used

    def format_date(dt):
        """
        This method converts a date (given in seconds since the Epoch) 
        in the format *Y*ear *m*onth *d*ay *H*our *M*inute
        """
        pattern="%Y-%m-%d:%H-%M" # UTC
        
        return time.strftime(pattern, time.gmtime(dt))
    
    def kelvin_to_celcius(k_temp):
        """
        This method converts kelvin degrees to celcius degrees.
        The scale offset is equal to 273.15°.
        """
        return round(float(k_temp - 273.15), 2)