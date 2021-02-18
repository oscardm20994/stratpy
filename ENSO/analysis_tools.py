from scipy import stats
import matplotlib
import pandas as pd
import numpy as np 
from .cube_analysis import *

import matplotlib.pyplot as plt
def remove_trend(dfx):
	tseries=np.squeeze(np.asarray(dfx))
	x=np.arange(len(tseries))
	mask=~np.isnan(x) & ~np.isnan(tseries)
	slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask],tseries[mask])
	if p_value<0.09:
		coeff=-x*slope
		#print('wohooo',p_value,slope*12,slope*120)
		tseries=tseries+coeff
	else:

		#print(p_value)
		coeff=np.zeros(len(tseries))
	return tseries#np.flip(tseries,axis=0)
def deseason(series,tvec):
	try:
		newt = [cell.point for cell in tvec.cells()]
	except:
		newt=tvec
	df=pd.DataFrame(series,index=pd.to_datetime(newt))
	try:
		result = seasonal_decompose(df)
	except:
		return series
	series=series-np.squeeze(result.seasonal.values)
	return series
def gtvec(cube,tcoord=None):
	if tcoord==None:
		tvec=cube.coord('time')
	else:
		tvec=cube.coord('t')
	newt= pd.to_datetime([datetime.datetime.strptime(str(cell.point),'%Y-%m-%d %H:%M:%S') for cell in tvec.cells()])
	return newt

def eof_deseason(eofcube,newt):
	latss=eofcube.coord('latitude').points
#	print(latss.shape)
	lonss=eofcube.coord('longitude').points
	for j in range(latss.shape[0]):
		for i in range(lonss.shape[0]):
			data=eofcube[:,j,i].data

			data=remove_trend(data)
			mean=np.mean(data)
			data=deseason(data,newt)

			eofcube[:,j,i].data=data-np.mean(data)
	return eofcube
def enso_cube_(filename,name):
	#classi=cube_analysis(filename)
	cube=loader(filename)
	newt=gtvec(cube)
	en34=iris_slice(cube,lats=[-5.5,5.5],lons=[190,240],areamean=True)
	print(en34)
	en34.data=remove_trend(en34.data)
	en34.data=deseason(en34.data,newt)
	en34.data=en34.data-np.mean(en34.data)
	eofarea=iris_slice(cube,lats=[-12,12],lons=[110,290],areamean=False)
	eof_cube=eof_deseason(eofarea,newt)
	cb,pcs,frac=eofcube(eof_cube)
	print(cb)	
	path='/home/users/jlgarcia/data/indices/'
	f=open(path+name+'ensoindices.txt','a')
	f.write('Date,EN3.4,PC1,PC2\n')	
	en34=en34.data
	for it,tt in enumerate(newt):
		print(tt,en34[it],pcs[it][0].data,pcs[it][1].data)	
		f.write(str(tt)+','+str(en34[it])+','+str(pcs[it][0].data)+','+str(pcs[it][1].data)+'\n')	

	f.close()	
	return cube
