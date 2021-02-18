import numpy as np
import datetime 
import pandas as pd
from eofs.standard import Eof
from statsmodels.tsa.seasonal import seasonal_decompose
from datetime import date
from dateutil.relativedelta import relativedelta
import statsmodels.api as sm
import glob,os, datetime,sys
from seasonal import fit_seasons,adjust_seasons
from eofs.iris import Eof as eoFs
from scipy import interpolate,stats
import iris

#class cube_analysis:
#
#	def __init__(self,fname):
#		self.fname = fname

def loader(fname):
	##load all files defined in fname
	cubes = iris.load(fname)
	
	#check how many cubes
	if len(cubes) == 1:
		cube = cubes[0]
	
	else:
		cube = cubes
	
	return cube
def eofcube(cube):
	solver=eoFs(cube)
	eofs=solver.eofs(neofs=3)
	pcs=solver.pcs(npcs=2,pcscaling=1)
	frac=solver.varianceFraction(neigs=3)
	return eofs,pcs,frac

def iris_slice(cube,lats,lons,areamean=False):
	latcons=iris.Constraint(latitude=lambda cell: lats[0] < cell < lats[1])
	loncons=iris.Constraint(longitude=lambda cell: lons[0] < cell < lons[1])

	cube=cube.extract(latcons)
	cube=cube.extract(loncons)
	cube.coord('latitude').guess_bounds()
	cube.coord('longitude').guess_bounds()
	if areamean:
		grid_areas = iris.analysis.cartography.area_weights(cube)
		cube=cube.collapsed(['latitude','longitude'],iris.analysis.MEAN,weights=grid_areas)
	return cube
