##### script to define the SSW class developed by Oscar Dimdore-Miles
##### this class can contains data used to calcuate the state of the polar vortex and SSWs
##### in a given dataset.

#import necessary packages
import iris
import numpy as np
import iris.coord_categorisation as coord_cat
from collections import Counter
from stratpy.sudden_strat_warming.SSW_detector import SSW_counter

## build SSW class which has attributes for different SSW metrics
class SSW:
	
	## init function asks user to assign dataset name (e.g. SSW_UKESM_pi_ctrl for the UKESM model pre industrial control run) 
	## and the years over which the data are evaluated
	def __init__(self, dataset_name, years):
		self.dataset_name = dataset_name
		self.years = years


	#function to calculate when SSWs occur in the simulation/observations. Input is an iris cube contaning the daily
	# ZMZW. Sends it off to the stratpy.processing.clean_cube function to constrain to the 10hPa level at 60N
	def get_SSW_dates(self, ZMZW_cube, thresh = 0):

		#call function to detect SSWs                
		SSW_month, SSW_year, SSW_day = SSW_counter(ZMZW, self.years[0], self.years[-1], thresh)
		
		#assign attributes of SSW instance to calulated SSW times 
		self.SSW_month = SSW_month
		self.SSW_year = SSW_year
		self.SSW_day_number = SSW_day


	# function to add month, season and year metadata
	def add_times(cube, time):
		coord_cat.add_month(cube, time, name='month')
		coord_cat.add_season(cube, time, name='clim_season')
		coord_cat.add_year(cube, time, name='year')
		coord_cat.add_day_of_year(cube, time, name='day_number')
		coord_cat.add_season_year(cube, time, name='season_year')
		return cube
	
	#callback function necessary for concatenating cubes	
	def callback(cube, field, filename): 
		del cube.attributes['history']
		del cube.attributes['valid_max']
		del cube.attributes['valid_min']
	
	
	## function to give the SSW rate in a given dataset over the whole time period
	def get_SSW_rate(self):
		self.SSWrate = len(self.SSW_month)/np.float(len(self.years))
		return
	
	### function to give the error bounds on a given SSW rate. takes as input the SSW tim
	### using bootstrap resampling. gives the mean +- an estiamted error. 
	def SSW_rate_Er(self, resample_interval):
		#call SSW timeseries function         
		get_SSWs_timeseries()
		## resample SSW time series and calculate set of rates
		rates = np.empty(0)
		for i in range(10000):
			rates = np.append(rates, np.mean(np.random.choice(SSW_timeseries, resample_interval, replace = False)))
		
		#get percentile of each of these rates		
		percentiles = np.percentile(rates, np.arange(0,101,1))
		
		#extract desired error % and return
		upper = percentiles[100 - self.bound]
		lower = percentiles[self.bound]
		
		SSWrate_Er = np.array([upper, lower])
		
		return SSWrate_Er, rates
	
	
	##call above function and assign the errors in SSW rates to the instance. 
	def get_SSW_rate_Er(self):
	
		self.SSWrate_Er = self.SSW_rate_Er(self, resample_interval)[0]
		self.SSWrate_Er[0] = self.SSWrate_Er[0] - self.SSWrate
		self.SSWrate_Er[1] = np.abs(self.SSWrate - self.SSWrate_Er[1])
		return
	
	
	## function to produce a time series of the number of SSW events
	## in each winter season.
	def get_SSWs_timeseries(self):
		year_count = []
		SSW_year_counter = Counter(self.SSW_year)
		for i in range(len(self.years)):
			year_count = np.append(year_count, SSW_year_counter[self.years[i]])
		
		self.SSW_timeseries = np.array(year_count)
		
		return 
	
	



	
	
	
	
	
		
		
