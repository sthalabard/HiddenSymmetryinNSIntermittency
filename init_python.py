#!/home/sthalabard/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:47:39 2019
Start-Up File for Spyder
@author: sthalabard
"""


import numpy as np
from math import *
import scipy as scp
from scipy import fftpack as ffts
from scipy import io, integrate,interpolate
from matplotlib import pyplot as plt
from matplotlib.pyplot import *
from matplotlib.ticker import MultipleLocator
from matplotlib import animation,cm,rc,colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource, LogNorm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from time import time as ctime
import os,glob,subprocess
import warnings; warnings.simplefilter('ignore')
import timeit,itertools

##########
from IPython.display import display,HTML,Image
display(HTML("<style>.container { width:95% !important; }</style>"))

import sys   
#print(sys.executable)
#%%
def newfig(a=1,b=1,figheight=12,aspectratio=0.75,fontsize=34,**kwargs):
    rc('legend', frameon=False,fancybox=False,shadow=False,fontsize=28,loc='best')
    rc('lines', linewidth=1)
    font = {'family':'serif','size':fontsize}
    rc('font',**font)
    rc('text', usetex=True)
    rc('xtick',labelsize=fontsize)
    rc('ytick',labelsize=fontsize)
    rc('savefig',format='pdf')
    return plt.subplots(a,b,figsize=(b*figheight,a*figheight*aspectratio),clear=True,tight_layout=True,**kwargs)

def newfig_3d(figheight=12,aspectratio=0.75,**kwargs):
    rc('legend', frameon=False,fancybox=False,shadow=False,fontsize=26,loc='best')
    rc('lines', linewidth=1)
    font = {'family':'serif','size':32}
    rc('font',**font)
    rc('text', usetex=True)
    rc('xtick',labelsize=32)
    rc('ytick',labelsize=32)
    rc('savefig',format='pdf')
    fig = plt.figure(figsize=(figheight,figheight*aspectratio),clear=True,tight_layout=True,**kwargs)
    ax = fig.add_subplot(111, projection='3d')
    ax.grid(False)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
    
#    ax.xaxis.set_major_locator(MultipleLocator(5))
#    ax.yaxis.set_major_locator(MultipleLocator(5))
#    ax.zaxis.set_major_locator(MultipleLocator(0.01))
    return fig,ax

class dic2struc:
    def __init__(self, **entries):
        self.__dict__.update(entries)

#%% SAVE/Load picklles PICKLES
import pickle
def save_pickle(name, data):
    pikd = open(name, 'wb')
    pickle.dump(data, pikd)
    pikd.close()
    return None

def load_pickle(file):
    pikd = open(file, 'rb')
    data = pickle.load(pikd)
    pikd.close()
    return data
#%% Am ore recent version of pickling using dill
import dill
def save_dill(name, data):
    pikd = open(name, 'wb')
    dill.dump(data, pikd)
    pikd.close()
    return None

def load_dill(file):
    pikd = open(file, 'rb')
    data = dill.load(pikd)
    pikd.close()
    return data

#%% TIMING
class tictoc:
    def __init__(self):
        self.tic0=time.perf_counter()

    def toc(self):
        print( '%0.2f s'  %(time.perf_counter()-self.tic0,))
        return None
    
    def tic(self):
        self.tic0=time.perf_counter()
        return None

#%% PDF Smoother
def smooth_pdf(pdf,bins,nbins=10,logmin=-5,scale='log'):
    xdata,ydata=bins,pdf
    cum=np.cumsum(ydata)*(xdata[2]-xdata[1])
    newbins=np.interp(np.linspace(0,1,nbins),cum,xdata)
    if scale is 'log':
        newbins_left=np.interp(10**np.linspace(logmin,0,nbins),cum,xdata)
        newbins_bulk=np.interp(np.linspace(0,1,nbins),cum,xdata)
        newbins_right=np.interp(1-10**np.linspace(logmin,0,nbins),cum,xdata)
        newbins=np.sort(np.concatenate((newbins_left,newbins_bulk,newbins_right)))

    cum=np.interp(newbins,xdata,cum)
    newpdf=np.diff(cum)/np.diff(newbins)
    newbins=(newbins[1:]+newbins[:-1])*0.5
    return newpdf,newbins