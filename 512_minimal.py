#! path~to/anaconda3/bin/python3.8
# -*- coding: utf-8 -*-

"""
The script provides  code   relevant data to generate fig. 1 and 2 and associated unshown DATA of the preprint

Hidden Symmetry in the Navier Stokes intermittency, by Mailybaev and Thalabard,

with current identifiers
    Philosophical Transactions A RSTA-2021-0098
    https://arxiv.org/submit/3752236

The data is contained in the repository 512, in the form of '***.dill' files 
labeled 
512_K62_vx.dill for figure 1

512_K62_multiplier__full.dill for figure 2

Requires python 3.8 and the packages listed in the start_up file 'init_python.py'

@author: Simon Thalabard
Created on Fri Mar 12 13:15:54 2021
"""

#%% Startup File
startup_file='init_python.py'
exec(open(startup_file).read())
join=os.path.join

#%% Parameters for the  512 DATA
param=dic2struc(**{
        'nu':5e-4,
        'eps':0.40988,
        'N':512,
#        'eta':0.0042,
        'L':1.52,
        'dx':2*pi/512,
        'keta':239.30,
        'eta':0.026, #2pi/keta
        'rms':0.854
        })

#%% Fig 1a and b: K62 statistics of the parallel increments
#Also produces the ESS fit from which 1b is obtained
exec(open('512_plotPDF_K62.py').read())

figs1a.savefig(join('Figs','1a.png'))
figs1b.savefig(join('Figs','1b.png'))

#%% Fig 2 : PDF of multipliers
LAMBDA=2
#Sets the ratio beween the multipliers l2=l1/LAMBDA in Eq (1.2)
#Can be  1/32,1/16,1/8,1/4,1/2,2,4,8,16,32,64, 128, 256,512 for the settings (i),(ii),(iii) of the rescaling parameter
#Lambda =4 and 16 correpsonds to Fig 2

CENTERING=False
#centers or not the PDF

INERTIALRANGE=(6,11500)
#Sets range of data to display based on the quantity min(ELL) (in units of eta)

exec(open('512_plotPDF_multipliers.py').read())
fig.savefig(join('Figs','512_mul_%0.2f.png' %(LAMBDA,)))
