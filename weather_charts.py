#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:43:46 2016

@author: timotheeaupetit
"""

# standard library imports
import json
from argparse import ArgumentParser

import numpy as np


import matplotlib.pyplot as plt

from city import City

    
class WeatherCharts(object):
    def __init__(self):
        """
        constructor creates an ArgumentParser object to implement main interface.
        Puts resulting args in self.args
        """
        parser = ArgumentParser()
        
        parser.add_argument ("-c", "--crop", dest='crop', default=None,
                             action='store',
                             help =  "Specify a rectangular area " +
                                     "as a comma-separated list of 4 numbers "+
                                     "for north, east, south, west")
        
        parser.add_argument ("-n", dest = "names", nargs='*', default=None,
                             action='append',
                             help="cumulative - select cities by their names")
        
        parser.add_argument ("-1", "--1d", dest='hist_1d', default=None,
                             action='store_true',
                             help=   "Display a bar chart for the pressure " +
                                     "in the first selected city")
        
        parser.add_argument ("-2", "--2d", dest='plot_2d', default=None,
                             action='store_true',
                             help=   "Display a 2D diagram of the positions " +
                                     "of selected cities")
        
        parser.add_argument ("-3", "--3d", dest='surf_3d', default=None,
                             action='store_true',
                             help=   "Display a 3D diagram of the pressure " +
                                     "in all cities")
        
        parser.add_argument ("filename")
        
        self.args = parser.parse_args()
        
        cities = []
        if self.args.names is not None:
            for name in self.args.names:
                cities.append(name[0])
        
        self.args.names = cities

    def load_cities(self):
        self.city_list = []
        self.city_selection = []
        
        with open(self.args.filename) as f:
            for city_data in f:
                city = City(json.loads(city_data))
                
                if self.args.crop is not None:
                    if city.in_area(map(float, self.args.crop.split(','))):
                        self.city_selection.append(city)
                        
                else:
                    if city.is_selected(self.args.names):
                        self.city_selection.append(city)
                        
                    else:
                        self.city_list.append(city)
    
    def shout_cities(self):
#        print(self.args.names) 
#        print(self.city_selection)
        print(self.city_list)

    def select_graph(self):
        if self.args.hist_1d is not None:
            self.graphe_1(self.city_selection[0])
            
        elif self.args.plot_2d is not None:
            self.graphe_2()
            
        elif self.args.surf_3d is not None:
            self.graphe_3()
        
        else:
            print('Choose between 1, 2 or 3 for chart_type\n')
    
    def graphe_1(self, city):
        """
        Triggered by choosing option "-1".
        Displays temperatures variations on a bar chart for the first selected city.
        Each day, there are 4 temperature measures appearing in that order:
        'morn', 'day', 'eve', 'night'
        """
        x = []
        abscisse = []
        y = []
        for data in city.data:
            abscisse.append(data.format_date())
            
            for i in range(4):
                x.append(data.date + i*3600*6) # 4 measures, 6 hours appart
            
            y.append(data.t_morn)
            y.append(data.t_day)
            y.append(data.t_eve)
            y.append(data.t_night)
        
        plt.bar(x, y, 3600*4) # each bar is given a width of 4 hours
        
        # max(x) = max(data.date) + 3*3600*6, but we only want max(data.date)
        plt.xticks(np.linspace(min(x), max(x)-3*3600*6, len(x)/4), tuple(abscisse), rotation = 90)
        plt.ylabel('Degrees Celcius') # the '°' character is misinterpreted
        plt.title('Temperatures in '+ city.name)
        plt.show()
        
    def graphe_2(self):
        """
        Triggered by choosing option "-2".
        Displays cities as a scatter plot based on their locations.
        Selected cities are highlighted with bigger spots in a different color.
        """
        x = []
        y = []
        x_sel = []
        y_sel = []
        for city in self.city_list:
            y.append(city.latitude)
            x.append(city.longitude)
            
        plt.scatter(x, y, s=20, c='blue')
        
        for city in self.city_selection:
            y_sel.append(city.latitude)
            x_sel.append(city.longitude)
            
        plt.scatter(x_sel, y_sel, s = 200, c='red', alpha = 0.5)
        plt.show()
        
    def graphe_3(self): # Surface 3D
        """
        Triggered by choosing option "-3".
        Displays a surface of air pressures, based on the city locations.
        Considering only the first measure for each city (may not be the same date).
        """
        from mpl_toolkits.mplot3d import Axes3D , axes3d
        from matplotlib import cm
        x = []
        y = []
        p = []
        
        self.date_ref = None
        for city in self.city_list:
            if self.date_ref is None:
                self.date_ref = city.data[0].date
            
            p.append(city.data[0].pressure)
            y.append(city.latitude)
            x.append(city.longitude)
        
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax = Axes3D(fig)
        ax.plot_trisurf(x, y, p, cmap=cm.jet, linewidth=0.2)
        # cset = ax.contour(x, y, p, 16, extend3d=True)
        # cset = ax.contour(X, Y, Z, 16, extend3d=True)
        # ax.clabel(cset, fontsize=9, inline=1)
        plt.title('Pressure on ' + str(self.date_ref))
        plt.show()
        