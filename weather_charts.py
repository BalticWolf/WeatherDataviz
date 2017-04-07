#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:43:46 2016

@author: timotheeaupetit
"""
# this must come first
from __future__ import print_function

# standard library imports
import json
from argparse import ArgumentParser

import time
import numpy as np

#from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt

from citylist import CityList, City

    
class WeatherCharts(object):
    def __init__(self):
        """
        constructor creates an ArgumentParser object to implement main interface
        Puts resulting args in self.args
        """
        parser = ArgumentParser()
        
        parser.add_argument ("-c", "--crop", dest='crop', default=None,
                             action='store',
                             help="Specify a rectangular area as a comma-separated list of 4 numbers for north, east, south, west")
        parser.add_argument ("-n", dest = "names", nargs='*', default=None,
                             action='append',
                             help="cumulative - select cities by their names")
        parser.add_argument ("-1", "--1d", dest='hist_1d', default=None,
                             action='store_true',
                             help="Display a bar chart for the pressure in the first selected city")
        parser.add_argument ("-2", "--2d", dest='plot_2d', default=None,
                             action='store_true',
                             help="Display a 2D diagram of the positions of selected cities")
        parser.add_argument ("-3", "--3d", dest='surf_3d', default=None,
                             action='store_true',
                             help="Display a 3D diagram of the pressure in all cities")
        parser.add_argument ("filename")
        
        self.args = parser.parse_args()
        
        cities = []
        if self.args.names:
            
            for name in self.args.names:
                cities.append(name[0])
        
        self.args.names = cities

    def load_cities(self):
        self.city_list = CityList()
        self.city_select = CityList()
        
        with open(self.args.filename) as f:
            for city_data in f:
                self.city = City(json.loads(city_data))
                
                if self.args.crop is not None:
                    if self.in_area(self.city):
                        self.city_select.add_city(self.city)
                        
                else:
                    if self.is_selected(self.city):
                        self.city_select.add_city(self.city)
                        
                    else:
                        self.city_list.add_city(self.city)
                    
    def is_selected(self, city):
        return city in self.args.names
    
    def in_area(self, city):
        max_lat, max_lon, min_lat, min_lon = map(float, self.args.crop.split(','))
        lat = city.latitude
        lon = city.longitude
        return ((min_lat <= lat <= max_lat) and (min_lon <= lon <= max_lon))

    def select_graph(self):
        if self.args.hist_1d:
            self.graphe_1(self.city_select[0])
            
        elif self.args.plot_2d:
            self.graphe_2()
            
        elif self.args.surf_3d:
            self.graphe_3()
        
        else:
            print('Choose between 1, 2 or 3 for chart_type\n')
    
    def graphe_1(self, city): # Histogramme
        """
        Triggered by choosing option "-1".
        Displays temperatures variations on a bar chart for the first selected city.
        Each day, there are 4 temperature measures appearing in that order:
        'morn', 'day', 'eve', 'night'
        """
        x = []
        abscisse = []
        y = []
        for data in city['data']:
            for i in range(4):
                abscisse.append(format_date(data['dt']))
                x.append(data['dt'] + i*3600*6)
            
            y.append(kelvin_to_celcius(data['temp']['morn']))
            y.append(kelvin_to_celcius(data['temp']['day']))
            y.append(kelvin_to_celcius(data['temp']['eve']))
            y.append(kelvin_to_celcius(data['temp']['night']))
        
        plt.bar(x, y)
        plt.xticks(np.arange(len(abscisse)) + 3600*6, tuple(abscisse))
        plt.ylabel('Celcius') # the '°' character is misinterpreted
        plt.title('Temperatures in '+ city['city']['name'])
        plt.show()
        
    def graphe_2(self): # Carte 2D
        """
        Avec l'option -2, le programme affiche l'ensemble des villes par leur position, en mettant en évidence les villes sélectionnées avec une taille plus importante et une couleur différente.
        matplotlib.pyplot.scatter
        """
        x = []
        y = []
        x_sel = []
        y_sel = []
        for city in self.city_list:
            y.append(city['city']['coord']['lat'])
            x.append(city['city']['coord']['lon'])
        plt.scatter(x, y, c='black')
        
        for city in self.city_select:
            y_sel.append(city['city']['coord']['lat'])
            x_sel.append(city['city']['coord']['lon'])
        plt.scatter(x_sel, y_sel, s = 200, c='red', alpha = 0.5)
        plt.show()
        
    def graphe_3(self): # Surface 3D
        """
        plot_trisurf
        """
        x = []
        y = []
        p = []
        self.date_ref = None
        for city in self.city_list:
            if not self.date_ref:
                self.date_ref = format_date(city['data'][0]['dt'])
            
            p.append(city['data'][0]['pressure'])
            y.append(city['city']['coord']['lat'])
            x.append(city['city']['coord']['lon'])
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(x, y, p, cmap=cm.jet, linewidth=0.2)
        plt.title(self.date_ref)
        plt.show()
        
def format_date(dt):
    # *Y*ear *m*onth *d*ay *H*our *M*inute
    date_format="%Y-%m-%d:%H-%M" # UTC
    
    # gmtime pour afficher en heure UTC (formerly GMT)
    return time.strftime(date_format, time.gmtime(dt))

def kelvin_to_celcius(k_temp):
    return round(float(k_temp - 273.15), 2)

