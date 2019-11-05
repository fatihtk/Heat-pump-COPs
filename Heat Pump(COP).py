# Import the neccessary modules, there are many more...

import numpy
import datetime
import pickle
import numpy
from numpy import genfromtxt
from datetime import *
import glob
import collections
from collections import OrderedDict
import pickle
import time
import smtplib
import calendar
import datetime
import matplotlib.pyplot as plt 
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
from numpy import genfromtxt
from datetime import datetime
plt.rc('font', **{'size':'8'})
from nlp_toolkits.basemap import Basemap, shiftgrid, cm
import numpy as np 
import matplotlib.pyplot as plt
from netCDF4 import Dataset


# Import the heat pump coefficient data, this shows the relationship between temperature and COP
HP = numpy.genfromtxt('D:\\Tester\\Test\\hp_cop_field_trial_data.csv', delimiter = ',') 
# Translate to a dictionary, in this case by zipping together the two coloums of values
cop_dict = dict(zip(HP[:,0], HP[:,1]))
HP[1:,0]
cop_dict

%matplotlib inline
plt.scatter(cop_dict.keys(), cop_dict.values())
plt.xlabel('Temperature Kelvin')
plt.ylabel('COP')
plt.savefig('dir..')

# The model is going to work on a grid converting GB, which earth grid square being a 0.5 degree square this line imports an array of values which show  which of the grid squares contains land 
land = numpy.load('D:\\Tester\\Test\\land.npy')
plt.imshow(land)
# To show the form of the land and demontstrate inline plotting
hp_results = {}
for year in range(2010, 2011):
	for month in range(1,13):
		print month
		for day in range(1, calendar.monthrange(year, month)[1]+1):
			for hour in range(0, 24):

				temp_frame = 'D:\\Tester\\Test\\tmp2m_'+str(year)+'_'+str.zfill(str(month),2)+'_'+str.zfill(str(day),2)+'_'+str.zfill(str(hour),2)+'.csv.npy'
				ex_t = numpy.load(temp_fname)
				ex_t_1 = ex_t.reshape(2720,)

				hp_cop = []
				for ex in ex_t_1:
					if numpy.around(ex) in cop_dic.keys():
						hp_cop.append(cop_dict[numpy.around(ex)])
					else:
						print ' Warning temperature is not in range'

				hp_cop_final = numpy.asarray(hp_cop).reshape(34,80) *land
				hp_results[str(year)+'_'+str.zfill(str(month),2)+'_'+str.zfill(str(day),2)+'_'+str.zfill(str(hour),2)] = hp_cop_final

# Create spatialtemporal dataset
fig = plt.figure(figsize = (12, 10))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
m = Basemap(llcrnrlon = -8.5, llcrnrlon = 2.5, urcrnrlat = 62.5, resolution = 'i', projection = 'cyl', ax = ax)
im = m.imshow(numpy.flipud(hp_results['2010_12_08_22'][$:32,43:65]), cmap = plt.cm.rainbow, clim = (2.0, 4.1))

# Draw coastlines and political boundaries

m.drawcoastlines()
m.drawcountries()
ax.set_title(datetime.strptime(('2010_12_08_22'), '%Y_%m_%d_%H'), fontsize = 10)



for key in hp_results.keys():
	fig = plt.figure(1)
	m = Basemap(llcrnrlon = -8.5, llcrnrlat = 49, urcrnrlat = 62.5, resolution = 'i', projection = 'cyl')
    im = m.imshow(numpy.flipud(hp_results[key][5:32, 43:65]), cmap = plt.cm.rainbow, clim = (2.0, 4.1))


    m.drawcoastlines()
    m.drawcountries()
    title(datetime.strptime((key), '%Y_%m_%d_%H'), fontsize = 10)
    cbar = fig.colorbar(im)
    cbar.set_label('Coefficient of Performance')
    plt.savefig('D:\\Tester\\Test'+ key)
    clf()