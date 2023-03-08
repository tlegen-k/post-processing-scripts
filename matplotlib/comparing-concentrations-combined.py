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
gs = fig.add_gridspec(1,3)
ax1,ax2,ax3 = gs.subplots()
# Set width and height of figure to the powerpoint presentation size
width = 10
height = 6
fig.set_size_inches(width,height)

# Set marker style
marker_style = dict( marker='o', markersize=5)

# Reading numerical data for no reactions case 7.75 m/s
with open('../7.75/no-reactions/post-processing/plot-over-time-in-water.csv', "r") as f:
    lines      = f.readlines()[2:]
    t_no_7_75      = [float(line.split(",")[1])  for line in lines]
    H2O2_no_7_75   = [float(line.split(",")[2])  for line in lines]
    HNO2_no_7_75   = [float(line.split(",")[3]) for line in lines]
    N2O4_no_7_75   = [float(line.split(",")[4]) for line in lines]
    NO_no_7_75     = [float(line.split(",")[5]) for line in lines]
    NO2_no_7_75    = [float(line.split(",")[6]) for line in lines]
    OH_no_7_75     = [float(line.split(",")[7]) for line in lines]

# Reading numerical data for with reactions case 7.75 m/s
with open('../7.75/with-reactions/post-processing/plot-over-time-in-water.csv', "r") as f:
    lines      = f.readlines()[2:]
    t_with_7_75    = [float(line.split(",")[1])  for line in lines]
    H2O2_with_7_75 = [float(line.split(",")[2])  for line in lines]
    HNO2_with_7_75 = [float(line.split(",")[3]) for line in lines]
    N2O4_with_7_75 = [float(line.split(",")[4]) for line in lines]
    NO_with_7_75   = [float(line.split(",")[5]) for line in lines]
    NO2_with_7_75  = [float(line.split(",")[6]) for line in lines]
    OH_with_7_75   = [float(line.split(",")[7]) for line in lines]
    times_to_consider_7_75 = len(t_with_7_75)

# Reading numerical data for no reactions case 15 m/s
with open('../15/no-reactions/post-processing/plot-over-time-in-water.csv', "r") as f:
    lines      = f.readlines()[2:]
    t_no_15       = [float(line.split(",")[1])  for line in lines]
    H2O2_no_15    = [float(line.split(",")[2])  for line in lines]
    HNO2_no_15    = [float(line.split(",")[3]) for line in lines]
    N2O4_no_15    = [float(line.split(",")[4]) for line in lines]
    NO_no_15      = [float(line.split(",")[5]) for line in lines]
    NO2_no_15     = [float(line.split(",")[6]) for line in lines]
    OH_no_15      = [float(line.split(",")[7]) for line in lines]
    
# Reading numerical data for with reactions case 15 m/s
with open('../15/with-reactions/post-processing/plot-over-time-in-water.csv', "r") as f:
    lines      = f.readlines()[2:]
    t_with_15     = [float(line.split(",")[1])  for line in lines]
    H2O2_with_15  = [float(line.split(",")[2])  for line in lines]
    HNO2_with_15  = [float(line.split(",")[3]) for line in lines]
    N2O4_with_15  = [float(line.split(",")[4]) for line in lines]
    NO_with_15    = [float(line.split(",")[5]) for line in lines]
    NO2_with_15   = [float(line.split(",")[6]) for line in lines]
    OH_with_15    = [float(line.split(",")[7]) for line in lines]
    times_to_consider_15 = len(t_with_15)

# Reading numerical data for no reactions case 20 m/s
with open('../20/no-reactions/post-processing/plot-over-time-in-water.csv', "r") as f:
    lines      = f.readlines()[2:]
    t_no_20       = [float(line.split(",")[1])  for line in lines]
    H2O2_no_20    = [float(line.split(",")[2])  for line in lines]
    HNO2_no_20    = [float(line.split(",")[3]) for line in lines]
    N2O4_no_20    = [float(line.split(",")[4]) for line in lines]
    NO_no_20      = [float(line.split(",")[5]) for line in lines]
    NO2_no_20     = [float(line.split(",")[6]) for line in lines]
    OH_no_20      = [float(line.split(",")[7]) for line in lines]

# Reading numerical data for with reactions case 20 m/s
with open('../20/with-reactions/post-processing/plot-over-time-in-water.csv', "r") as f:
    lines      = f.readlines()[2:]
    t_with_20     = [float(line.split(",")[1])  for line in lines]
    H2O2_with_20  = [float(line.split(",")[2])  for line in lines]
    HNO2_with_20  = [float(line.split(",")[3]) for line in lines]
    N2O4_with_20  = [float(line.split(",")[4]) for line in lines]
    NO_with_20    = [float(line.split(",")[5]) for line in lines]
    NO2_with_20   = [float(line.split(",")[6]) for line in lines]
    OH_with_20    = [float(line.split(",")[7]) for line in lines]
    times_to_consider_20 = len(t_with_20)

# # convert to normalized number concentrations simulations results
# H2O2_no_20[:] = [x/(0.2657*10**(-6)) for x in H2O2_no_20]
# HNO2_no_20[:] = [x/(1.3289*10**(-6)) for x in HNO2_no_20]
# # N2O4_no_20[:] = [x/(1.3289*10**(-5)) for x in N2O4_no_20]
# NO_no_20[:] = [x/(1.3289*10**(-5)) for x in NO_no_20]
# NO2_no_20[:] = [x/(0.8305*10**(-7)) for x in NO2_no_20]
# OH_no_20[:] = [x/(0.2159*10**(-5)) for x in OH_no_20]

# H2O2_with_20[:] = [x/(0.2657*10**(-6)) for x in H2O2_with_20]
# HNO2_with_20[:] = [x/(1.3289*10**(-6)) for x in HNO2_with_20]
# # N2O4_with_20[:] = [x/(1.3289*10**(-5)) for x in N2O4_with_20]
# NO_with_20[:] = [x/(1.3289*10**(-5)) for x in NO_with_20]
# NO2_with_20[:] = [x/(0.8305*10**(-7)) for x in NO2_with_20]
# OH_with_20[:] = [x/(0.2159*10**(-5)) for x in OH_with_20]

# Plot data for 7.75 m/s cases with/without chemical reactions
ax1.plot(t_no_7_75, H2O2_no_7_75, label="H2O2 no reactions", **marker_style, fillstyle='none', linestyle='None', color='r')
ax1.plot(t_with_7_75, H2O2_with_7_75, label="H2O2 with reactions", fillstyle='none', color='r')

ax1.plot(t_no_7_75, HNO2_no_7_75, label="HNO2 no reactions", **marker_style, fillstyle='none', linestyle='None', color='g')
ax1.plot(t_with_7_75, HNO2_with_7_75, label="HNO2 with reactions", fillstyle='none', color='g')

ax1.plot(t_no_7_75, N2O4_no_7_75, label="N2O4 no reactions", **marker_style, fillstyle='none', linestyle='None', color='y')
ax1.plot(t_with_7_75, N2O4_with_7_75, label="N2O4 with reactions", fillstyle='none', color='y')

ax1.plot(t_no_7_75, NO_no_7_75, label="NO no reactions", **marker_style, fillstyle='none', linestyle='None', color='b')
ax1.plot(t_with_7_75, NO_with_7_75, label="NO with reactions", fillstyle='none', color='b')

ax1.plot(t_no_7_75, NO2_no_7_75, label="NO2 no reactions", **marker_style, fillstyle='none', linestyle='None', color='c')
ax1.plot(t_with_7_75, NO2_with_7_75, label="NO2 with reactions", fillstyle='none', color='c')

ax1.plot(t_no_7_75, OH_no_7_75, label="OH no reactions", **marker_style, fillstyle='none', linestyle='None', color='m')
ax1.plot(t_with_7_75, OH_with_7_75, label="OH with reactions", fillstyle='none', color='m')

# Plot data for 15 m/s cases with/without chemical reactions
ax2.plot(t_no_15, H2O2_no_15, label="H2O2 no reactions", **marker_style, fillstyle='none', linestyle='None', color='r')
ax2.plot(t_with_15, H2O2_with_15, label="H2O2 with reactions", fillstyle='none', color='r')

ax2.plot(t_no_15, HNO2_no_15, label="HNO2 no reactions", **marker_style, fillstyle='none', linestyle='None', color='g')
ax2.plot(t_with_15, HNO2_with_15, label="HNO2 with reactions", fillstyle='none', color='g')

ax2.plot(t_no_15, N2O4_no_15, label="N2O4 no reactions", **marker_style, fillstyle='none', linestyle='None', color='y')
ax2.plot(t_with_15, N2O4_with_15, label="N2O4 with reactions", fillstyle='none', color='y')

ax2.plot(t_no_15, NO_no_15, label="NO no reactions", **marker_style, fillstyle='none', linestyle='None', color='b')
ax2.plot(t_with_15, NO_with_15, label="NO with reactions", fillstyle='none', color='b')

ax2.plot(t_no_15, NO2_no_15, label="NO2 no reactions", **marker_style, fillstyle='none', linestyle='None', color='c')
ax2.plot(t_with_15, NO2_with_15, label="NO2 with reactions", fillstyle='none', color='c')

ax2.plot(t_no_15, OH_no_15, label="OH no reactions", **marker_style, fillstyle='none', linestyle='None', color='m')
ax2.plot(t_with_15, OH_with_15, label="OH with reactions", fillstyle='none', color='m')

# Plot data for 20 m/s cases with/without chemical reactions
ax3.plot(t_no_20, H2O2_no_20, label="H2O2 no reactions", **marker_style, fillstyle='none', linestyle='None', color='r')
ax3.plot(t_with_20, H2O2_with_20, label="H2O2 with reactions", fillstyle='none', color='r')

ax3.plot(t_no_20, HNO2_no_20, label="HNO2 no reactions", **marker_style, fillstyle='none', linestyle='None', color='g')
ax3.plot(t_with_20, HNO2_with_20, label="HNO2 with reactions", fillstyle='none', color='g')

ax3.plot(t_no_20, N2O4_no_20, label="N2O4 no reactions", **marker_style, fillstyle='none', linestyle='None', color='y')
ax3.plot(t_with_20, N2O4_with_20, label="N2O4 with reactions", fillstyle='none', color='y')

ax3.plot(t_no_20, NO_no_20, label="NO no reactions", **marker_style, fillstyle='none', linestyle='None', color='b')
ax3.plot(t_with_20, NO_with_20, label="NO with reactions", fillstyle='none', color='b')

ax3.plot(t_no_20, NO2_no_20, label="NO2 no reactions", **marker_style, fillstyle='none', linestyle='None', color='c')
ax3.plot(t_with_20, NO2_with_20, label="NO2 with reactions", fillstyle='none', color='c')

ax3.plot(t_no_20, OH_no_20, label="OH no reactions", **marker_style, fillstyle='none', linestyle='None', color='m')
ax3.plot(t_with_20, OH_with_20, label="OH with reactions", fillstyle='none', color='m')

# Set log scale for x and y coordinates
ax1.set_yscale('log')
ax2.set_yscale('log')
ax3.set_yscale('log')

ax1.yaxis.set_ticks_position('both')
ax2.yaxis.set_ticks_position('both')
ax3.yaxis.set_ticks_position('both')

# work around to show major and minor ticks for the log scale graphs
locmaj = matplotlib.ticker.LogLocator(base=10,numticks=12) 
ax1.yaxis.set_major_locator(locmaj)
ax2.yaxis.set_major_locator(locmaj)
ax3.yaxis.set_major_locator(locmaj)

locmin = matplotlib.ticker.LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=12)
ax1.yaxis.set_minor_locator(locmin)
ax1.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax2.yaxis.set_minor_locator(locmin)
ax2.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax3.yaxis.set_minor_locator(locmin)
ax3.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

# limiting x axis with min(max(t_with_reactions))
ax1.set_xlim(0, 25)
ax2.set_xlim(0, 25)
ax3.set_xlim(0, 25)

ax1.set_ylim(10**(-15),10**(-5))
ax2.set_ylim(10**(-15),10**(-5))
ax3.set_ylim(10**(-15),10**(-5))

#Average values from Norberg et al. 2018 for touching case (figure 7)
HNO2_Norberg = 6.64e-8 # green
NO2_Norberg = 7.75e-7 # light blue (turquoise)
OH_Norberg = 4.98e-8 # purple

# add custom points to scatter plot
ax1.plot(1, HNO2_Norberg, "x",  markersize=10, color='g')
ax2.plot(1, HNO2_Norberg, "x",  markersize=10, color='g')
ax3.plot(1, HNO2_Norberg, "x",  markersize=10, color='g')
# ax1.yellowgreen("HNO2 Norberg et al. 2018", [1, HNO2_Norberg])

ax1.plot(1, NO2_Norberg, "x",  markersize=10, color='c')
ax2.plot(1, NO2_Norberg, "x",  markersize=10, color='c')
ax3.plot(1, NO2_Norberg, "x",  markersize=10, color='c')

ax1.plot(1, OH_Norberg, "x",  markersize=10, color='m')
ax2.plot(1, OH_Norberg, "x",  markersize=10, color='m')
ax3.plot(1, OH_Norberg, "x",  markersize=10, color='m')

# remove outer paddings around the all subplots
plt.tight_layout()
# plt.show()
# if want to save in file
plt.savefig('figures/concentrations-comparison-nordberg-et-al-2018.pdf', bbox_inches="tight")
