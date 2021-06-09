#! path~to/anaconda3/bin/python3.8
# -*- coding: utf-8 -*-

"""
The script provides minimal code  to generate figure 4, as well as unshown figures of the preprint

Hidden Symmetry in the Navier Stokes intermittency, by Mailybaev and Thalabard,

with current identifiers
    Philosophical Transactions A RSTA-2021-0098
    https://arxiv.org/submit/3752236

The data is contained in the repository 4096, in the form of '***.dill' files
labeled 4096_xxxx_Dy.yyyy
with xxxx = RESCALING, presribing the choice of functionnal A in Eq.(6.6) (see details below)
     y.yyy= LAMDBA (observing scale)

Requires python 3.8 and the packages listed in the start_up file 'init_python.py'

@author: Simon Thalabard
Created on Fri Mar 12 13:15:54 2021
"""

#%% Startup file
startup_file='init_python.py'
exec(open(startup_file).read())
join=os.path.join
#%% Parameter for 4096
param=dic2struc()
param.nu=1e-5
param.rms=0.1936
param.epsilon=0.003613
param.L=2.01
param.N=4096
param.dt=5.9e-4
param.dx=2*pi/param.N 
param.eta=2*pi*(param.nu**3/param.epsilon)**(0.25)
param.lam=param.rms**3/param.epsilon
param.Tlam=param.lam/param.rms

#%% Parameter for the hidden PDF of Figure 4
RESCALING='DV3_ABS'
#Sets the functionnal A of Eq. (2.3)
#The choices described in Eq.(6.6) are obtained by setting the rescaling to 
#(i) 'DV2' (ii)'DV_rand' (iii) 'DV3_ABS' 
# The setting  'kolmogorov' is also allowed, formally corresponding to the mean-field choice A_\ell = \ell^{1/3}

LAMBDA=4
#Sets the observing rescaled scale of Eq.(6.5)
#Can be  1/4,1/2,2,4 for the settings (i),(ii),(iii) of the rescaling parameter
#should be 1 for the RESCALING setting 'kolmogorov'

USE_JACOBIAN=True
#Sets whether the jacobian of Eq.(6.5) is included or not 

CENTERING=False
#centers or not the PDF

INERTIALRANGE=(6,500)
#Sets range of data to display based on the quantity min(\ell, \lambda \ell) (in units of eta)

#%% Parameter for the Cosmetics
cosmetics=dic2struc()
cosmetics.coolR=lambda u: cm.cubehelix(np.log2(u)/np.log2(8192))
cosmetics.lw=lambda r1:6-np.log2(512/r1)

cosmetics.pdfcutoff=5e-9
#sets minimal pdf value to smooth from in order to filter noisy data the in semilogy inset
#nice values are 
#5e-7 for DV2 RESCALING
#5e-7 for DV_rand RESCALING
#5e-9 for DV3_ABS RESCALING
#1e-6 for kolmogorov RESCALING

cosmetics.binslin=None#128 #None
# If integer value, smooths the PDF in the lin representation based on percentiles; useful especially for LAMBDA>1.
# eg cosmetics.binslin=10 the represented PDF in the main panel has 10 bins determined by the 10 deciles of the PDF.
#If None, does not smooth the pdf in the main panel

#%%
exec(open('4096_plotPDF.py').read())

#%
if USE_JACOBIAN:
    name='%s_%0.2f_hidden.png' %(RESCALING,LAMBDA,)
else:
    name='%s_%0.2f_uniform.png' %(RESCALING,LAMBDA,)
fig.savefig(join('Figs',name))
#%% IF NEEDED
#Adjust display in the main panel
ax=axs[0]
ax.set_xlim(-3,3)

#Adjust display fit in the inset
ax=axs[1]
#ax.set_xlim(-16,16)
