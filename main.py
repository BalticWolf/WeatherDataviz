#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 7  22:30:07 2017

@author: timotheeaupetit
"""

from weather_charts import WeatherCharts

def main():
    m = WeatherCharts()
    m.load_cities()
    m.select_graph()
#    m.shout_cities()
    
if __name__ == '__main__':
    main()
    