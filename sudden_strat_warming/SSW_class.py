##### script to define the SSW class developed by Oscar Dimdore-Miles
##### this class can contains data used to calcuate the state of the polar vortex and SSWs
##### in a given dataset. This includes climatologies of various variables, wave driving, SSW time
##### series, wavelet power spectra etc


#import necessary packages
import iris
import numpy as np
import iris.coord_categorisation as coord_cat
from collections import Counter
from SSW_detector import SSW_counter


## build SSW class which has attributes for different SSW metrics
class SSW:
	
	## init function
	def __init__(self, dataset_name, years):
		self.dataset_name = dataset_name
		self.years = years



		def get_SSWs(self, ZMZW, thresh = 0):
				SSW, SSW_year, SSW_day = SSW_counter(ZMZW, self.years[0], self.years[-1], thresh) 
				self.SSW_month = SSW
				self.SSW_year = SSW_year
				self.SSW_day_number = SSW_year

	

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
	
    ## define a loader function. this loads cubes of data. adds extra time coordinates
	## using the user defined "add_times" function
	def loader(fname):
		##load all files defined in fname
		cubes = iris.load(fname)
		
		#check how many cubes
		if len(cubes) == 1:
			cube = cubes[0]
		
		else:
			cube = cubes
		
		return cube

	
	## function to give the SSW rate in a given dataset over the whole time period
	def get_SSW_rate(self):
		
		self.SSWrate = len(self.SSW_month)/np.float(len(self.years))
		
		return
	
	### function to give the error bounds on a given SSW rate
	### using bootstrap resampling. gives the mean +-
	def SSW_rate_Er(self, SSW_timeseries):
		
		## resample SSW time series and calculate set of rates
		rates = np.empty(0)
		for i in range(10000):
			rates = np.append(rates, np.mean(np.random.choice(SSW_timeseries, self.resample_interval, replace = False)))
		
		#get percentile of each of these rates		
		percentiles = np.percentile(rates, np.arange(0,101,1))
		
		#extract desired error % and return
		upper = percentiles[100 - self.bound]
		lower = percentiles[self.bound]
		
		SSWrate_Er = np.array([upper, lower])
		
		return SSWrate_Er, rates
	
	
	##call above function
	def get_SSW_rate_Er(self):
	
		self.SSWrate_Er = self.SSW_rate_Er(self.SSW_timeseries)[0]
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
	
	



	
	
	
	
	
		
		
