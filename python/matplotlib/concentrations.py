# Creates plots of phase fractions for phase change simulations using specified output size to match paper draft width in powerpoint slides
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import StrMethodFormatter
import math

import numpy as np
import csv

# Need to set fonts before initializing with subplots()
# set font size for plot according to paper recommendations
plt.rcParams.update({'font.size': 10})
plt.rcParams.update({'font.family': 'serif'})
plt.rcParams.update({'font.serif': 'Arial'})

fig = plt.figure()
gs = fig.add_gridspec(1,1)
ax = gs.subplots()
# Set width and height of figure to the powerpoint presentation size
width = 10
height = 6
fig.set_size_inches(width,height)

# Set marker style
marker_style = dict( marker='o', markersize=5)

times = [40,60,80]
ppms = [1,2,3,4,5]

volumes_40s=[]
conc_40s=[]
for i in range(5):
    with open('../{}ppm/post-processing/averages-{}.csv'.format(i+1, times[0]), "r") as f:
        lines  = f.readlines()[1:]
        H2O2   = [float(line.split(",")[2])  for line in lines]
        volume = [float(line.split(",")[8])  for line in lines]
    volumes_40s.append(volume[0])
    conc_40s.append(H2O2[0])

conc_60s=[]
for i in range(5):
    with open('../{}ppm/post-processing/averages-{}.csv'.format(i+1, times[1]), "r") as f:
        lines  = f.readlines()[1:]
        H2O2   = [float(line.split(",")[2])  for line in lines]
        volume = [float(line.split(",")[8])  for line in lines]
    conc_60s.append(H2O2[0])

conc_80s=[]
for i in range(5):
    with open('../{}ppm/post-processing/averages-{}.csv'.format(i+1, times[2]), "r") as f:
        lines  = f.readlines()[1:]
        H2O2   = [float(line.split(",")[2])  for line in lines]
    conc_80s.append(H2O2[0])

volume=volumes_40s[0]

# # convert to normalized number concentrations simulations results
conc_40s[:] = [x*34.01*10**(-3)/volume for x in conc_40s]
conc_60s[:] = [x*34.01*10**(-3)/volume for x in conc_60s]
conc_80s[:] = [x*34.01*10**(-3)/volume for x in conc_80s]


ax.plot(ppms, conc_40s, label="t = 40s", **marker_style, fillstyle='none', linestyle='None', color='r')
ax.plot(ppms, conc_60s, label="t = 60s", **marker_style, fillstyle='none', linestyle='None', color='g')
ax.plot(ppms, conc_80s, label="t = 80s", **marker_style, fillstyle='none', linestyle='None', color='b')

# set labels
ax.set_xlabel('Inlet H2O2 concentrations (ppm)')
ax.set_ylabel('H2O2 concentrations in liquid (mg/l)')

#calculate equation for trendline
z_40 = np.polyfit(ppms, conc_40s, 1)
p_40 = np.poly1d(z_40)

z_60 = np.polyfit(ppms, conc_60s, 1)
p_60 = np.poly1d(z_60)

z_80 = np.polyfit(ppms, conc_80s, 1)
p_80 = np.poly1d(z_80)

#add trendline to plot
ax.plot(ppms, p_40(ppms), color='r')
ax.plot(ppms, p_60(ppms), color='g')
ax.plot(ppms, p_80(ppms), color='b')

ax.legend(frameon=False, loc='best')

# # remove outer paddings around the all subplots
plt.tight_layout()
# plt.show()
# if want to save in file
plt.savefig('figures/concentrations.pdf', bbox_inches="tight")
