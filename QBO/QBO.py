#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 16:55:41 2021

@author: oscardimdore-miles
"""

##### script to define the QBO class in the package stratpy developed by Oscar Dimdore-Miles
##### this class can contains data used to calcuate the state of the QBO
##### in a given dataset. This includes timeseries,

#import necessary packages
import iris
import numpy as np
import cf_units
from scipy.fftpack import fft, fftfreq

class QBO_class:

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        return
    
    #function to assign the instance of the QBO class the attribute of 
    #ZMZW timeseries over the equator. Takes a cube of ZMZW as input
    #outputs cube of QBO index
    def QBO_series(self, U):
        def correct_lat(cell):
            return -5.1 < cell < 5.1
        
        #make latitude constraint
        lat_constraint = iris.Constraint(latitude = correct_lat)
        
        #constrain 
        U_QBO = U.extract(lat_constraint)
        U_QBO = U_QBO.collapsed('latitude', iris.analysis.MEAN)
        
        #assign cube to QBO object
        self.QBO_series = U_QBO

  

	
	
	
