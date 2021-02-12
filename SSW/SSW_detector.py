#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 15:49:49 2021
SSW detector
@author: oscardimdore-miles
"""
import iris
import numpy as np

def SSW_counter(U_strat, start_year, end_year, thresh):
#identify SSWs from U_strat cube. defition of an SSW: U becomes negative at 60N 10hPa in months NDJFM (20 days after an SSW, another can occur)

	#restrict months to Nov-April
	SSW_day, U_SSW_seasons, SSW, final, indexi, indexj, SSW_year = [], [], [], [], [], [], []
	U_strat_ND = U_strat.extract(iris.Constraint(month = ['Nov', 'Dec']))
	U_strat_JFMA = U_strat.extract(iris.Constraint(month = ['Jan', 'Feb', 'Mar', 'Apr']))

    #place each extended winter in a cublist by itself
	U_SSW_seasons.append(U_strat_JFMA.extract(iris.Constraint(year = start_year)))
	for i in range(start_year, end_year-1):
		dummy2 = iris.cube.CubeList([U_strat_ND.extract(iris.Constraint(year = i)),U_strat_JFMA.extract(iris.Constraint(year = i+1))])
		U_SSW_seasons.append(dummy2.concatenate_cube())
    
    #loops over winters scanning through to check whether the ZMZW reverses at
    #any point
	for j in range(1,len(U_SSW_seasons)):
		print(j)
		i=0
		while i < len(U_SSW_seasons[j].data):
			if U_SSW_seasons[j].data[i] < thresh and U_SSW_seasons[j].data[i-1] >= thresh:
				SSW.append(str(U_SSW_seasons[j].coord('month').points[i]))
				SSW_year.append(U_SSW_seasons[j].coord('season_year').points[i])
				SSW_day.append(U_SSW_seasons[j].coord('day_number').points[i])
				indexi.append(i)
				indexj.append(j)
				final.append(i)
				for x in range(i, len(U_SSW_seasons[j].data)):
					if np.all(U_SSW_seasons[j].data[x:x+19] > thresh):
						i = x+19
						break

					elif x == len(U_SSW_seasons[j].data)-1:
						i = 1000000
						
					else:
						j=j	
			else:
				i = i+1
		
		
		#Check for a fianl warming and remove from SSW list if found
		#f = np.where(U_SSW_seasons[j].data == final[-1])[0]
		#print f #U_SSW_seasons[j].data[f-1:f+1]
		if final != []:	
			for k in range(final[-1],len(U_SSW_seasons[j].data)-9):
				if np.all(U_SSW_seasons[j].data[k:k+9] > thresh):
					break
				elif k== len(U_SSW_seasons[j].data)-10: 
					#print 'final warming found'
					del SSW[-1]
					del SSW_year[-1]
					del SSW_day[-1]

                    			#del SSW_Kurt[-1]
					del indexi[-1]
					del indexj[-1]
					break
				else:
					k=k	
		else:	
			j = j
			
	#filter out all April warmings, these are not strictly SSWs		
	for i in range(len(SSW)):
		if SSW[i] == 'Apr':
			SSW_year[i] = 0
			SSW_day[i] = 0
	SSW_year = list(filter(lambda a: a != 0, SSW_year))
	SSW_day = list(filter(lambda a: a != 0, SSW_day))
	SSW = list(filter(lambda a: a != 'Apr', SSW))
    
    #return month, year and day of SSW events 
	return SSW, SSW_year, SSW_day

