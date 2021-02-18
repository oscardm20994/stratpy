import numpy as np
import datetime 
import pandas as pd
from eofs.standard import Eof
from statsmodels.tsa.seasonal import seasonal_decompose
from datetime import date
from dateutil.relativedelta import relativedelta
import scipy.signal
import statsmodels.api as sm
import glob,os, datetime,sys
from seasonal import fit_seasons,adjust_seasons
from mpl_toolkits.basemap import shiftgrid
from eofs.iris import Eof as eoFs
from scipy import interpolate,stats
import iris

def ensoindexfromcube(cube):
	print(cube.coords)
	coord_names = [coord.name() for coord in cube.coords()]
	if 'time' in coord_names:
		tt='time'
		kind='obs'
	else:
		tt='t'
		kind='model'
	print(kind)
	print(cube.coord(tt))
	tvec=cube.coord(tt)
	origcube=cube
	datevar = []
	tvec=cube.coord(tt)
	print(tvec.shape)
	print(cube.shape)
	latconstraint=iris.Constraint(latitude=lambda cell: -11 < cell < 11)
	lat34=iris.Constraint(latitude=lambda cell: -5.5 < cell < 5.5)
	lonconstraint=iris.Constraint(longitude=lambda cell: 110< cell < 290)
	lon34=iris.Constraint(longitude=lambda cell: 190< cell < 240)
	if cube.shape[1]==1:
		print('wrong shape of cube')
	cube=cube.extract(lat34)
	print(cube)
	cube=cube.extract(lon34)
	print(cube)
	print(origcube)
	meancube=origcube.collapsed(['latitude','longitude'],iris.analysis.MEAN)
	mean=meancube.collapsed(tt,iris.analysis.MEAN).data
	anomalcube=cube.collapsed(['latitude','longitude'],iris.analysis.MEAN)-mean
	cons=iris.Constraint(clim_season='djf')
	iris.coord_categorisation.add_season(cube, tt, name='clim_season')
	iris.coord_categorisation.add_season_year(cube, tt, name='season_year')
	seasonal=cube.aggregated_by(['clim_season','season_year'],iris.analysis.MEAN)

