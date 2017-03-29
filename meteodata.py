#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:43:46 2016

@author: timotheeaupetit
"""
# this must come first
from __future__ import print_function

"""
{u'city': {u'coord': {u'lat': 49.558578, u'lon': 1.62803},
           u'country': u'FR',
           u'id': 3028097,
           u'name': u'Cayenne'},
 u'data': [{u'clouds': 80,
            u'deg': 330,
            u'dt': 1394884800,
            u'humidity': 85,
            u'pressure': 1028.47,
            u'speed': 5.41,
            u'temp': {u'day': 282.3,
                      u'eve': 282.86,
                      u'max': 283.22,
                      u'min': 279.7,
                      u'morn': 279.7,
                      u'night': 281.96},
            u'weather': [{u'description': u'broken clouds',
                          u'icon': u'04d',
                          u'id': 803,
                          u'main': u'Clouds'}]},
           '... other similar dicts ...'],
 u'time': 1394865585}
"""


"""
MA COMMANDE
python ./meteodata.py -c 49,2.5,48,2.4 -n 'Paris' -n 'Versailles' --1d data/cities_idf.json
python ./meteodata.py -n 'Paris' -n 'Londres' --2d data/cities_europe.json
python ./meteodata.py -3 data/cities_europe.json
"""

# standard library imports
import json
from argparse import ArgumentParser

import time
import numpy as np
#from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from citylist import CityList

def format_date(dt):
    # *Y*ear *m*onth *d*ay *H*our *M*inute
    date_format="%Y-%m-%d:%H-%M" # UTC
    
    # gmtime pour afficher en heure UTC (formerly GMT)
    return time.strftime(date_format, time.gmtime(dt))

def kelvin_to_celcius(k_temp):
    return round(float(k_temp - 273.15), 2)
    
class Missmeteo(object):
    def __init__(self):
        """
        constructor creates an ArgumentParser object to implement main interface
        puts resulting args in self.args
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
            for city in f:
                self.d_city = json.loads(city)
                if self.args.crop:
                    if self.in_area(self.d_city):
                        self.city_select.add_city(self.d_city)
                else:
                    if self.is_selected(self.d_city):
                        
                        self.city_select.add_city(self.d_city)
                    else:
                        self.city_list.add_city(self.d_city)
                    
    def is_selected(self, city):
        return city['city']['name'] in self.args.names
    
    def in_area(self, city):
        max_lat, max_lon, min_lat, min_lon = map(float, self.args.crop.split(','))
        lat = city['city']['coord']['lat']
        lon = city['city']['coord']['lon']
        return ((min_lat <= lat <= max_lat) and (min_lon <= lon <= max_lon))

    def select_graph(self):
        if self.args.hist_1d:
            self.graphe_1(self.city_select[0])
        elif self.args.plot_2d:
            self.graphe_2()
        elif self.args.surf_3d:
            self.graphe_3()
        else:
            print('Choisir 1, 2 ou 3 pour chart_type\n')
    
    def graphe_1(self, city): # Histogramme
        """
        Avec l'option -1, le programme affiche sous forme de diagramme à barres, les températures de la première ville sélectionnée, et ce sur l'ensemble de la période.
        Pour chaque date on affiche, dans l'ordre, les champs suivants de temp dans data
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
        plt.ylabel('Celcius') #attention au '°' qui est mal interprété
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
        
    def main(self):
        self.load_cities()
        self.select_graph()
    
m = Missmeteo()
m.main()

