# Hidden Symmetry in NS Intermittency
Source code and Data for the  arXiv submission 

**Hidden symmetry in the Navier-Stokes intermittency**,
*by Mailybaev and Thalabard*,

with current identifiers

- Philosophical Transactions A RSTA-2021-0098
    
- ArXiV https://arxiv.org/submit/3752236

[![DOI](https://zenodo.org/badge/369326157.svg)](https://zenodo.org/badge/latestdoi/369326157)
***


The repository contains data and minimal python code to 
generate figure 1,2 and 4 of the paper, as well as the other figures mentionned but not shown in the paper.

The data is contained in the subfolders 
512 & 4096 in the form of .dill files, ie, Python pickling format, and contains all relevant PDF.
The script Dill2mat.py  converts from dill to Matlab .mat format.

Data is analysed with the Python scripts:

- 512_minimal.py for figures 1 and 2
calling the subscripts

> init_python.py

> 512_plotPDF_K62.py

> 512_plotPDF_multipliers.py

- 4096_minimal.py for figures 4
calling the subscripts

>  init_python.py

> 512_plotPDF_K62.py

> 512_plotPDF_multipliers.py

The scripts  run on python 3.8 with anaconda 3 distribution under Spyder 4.1.5 environment


***
*Observations* 

- To reproduce Fig 4, please set LAMBDA= 1/2 and  2, USE_JACOBIAN=True, and  CENTERING = False in the file 4096_minimal.py.

- We also include the data for Lambda =1/4 and 4.

- The case without the weights mentionned but not shown at the end of Section 6 is obtained by setting USE_JACOBIAN=False.

- Use Lambda=1, RESCALING='kolmogorov' to compare collapse with usual PDF of parallel increments.

@author: Simon Thalabard simon.thalabard@ens-lyon.org
***

