#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 09:05 2016
Updated on Fri Apr 07 23:07 2017

@author: timotheeaupetit
"""

    
class CityList(list):
    def __init__(self):
        list.__init__(self)
    
    def add_city(self, city):
        self.append(city)
    
class City(object):
    def __init__(self, json_data):
        self.name = json_data['city']['name']
        self.longitude = json_data['city']['coord']['lon']
        self.latitude = json_data['city']['coord']['lat']
        self.data = Measure(json_data['data']) # should be a list of measures

class Measure(object):
    def __init__(self, json_data):
        self.clouds = json_data['clouds']
        # self.deg = json_data['deg'] # can't recall what this is
        self.date = json_data['dt']
        self.humidity = json_data['humidity']
        self.pressure = json_data['pressure']
        self.wind_speed = json_data['speed']
        self.temperatures = json_data['temp'] # should be a list
        self.weather = json_data['weather'] # should be a list