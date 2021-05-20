# HiddenSymmetryinNSIntermittency
Source code for the eponymous arXiv submission by Mailybaev and Thalabard

**Hidden symmetry in the Navier-Stokes intermittency**
by Mailybaev and Thalabard,

with current identifiers

- Philosophical Transactions A RSTA-2021-0098
    
- ArXiV https://arxiv.org/submit/3752236
***


The repository contains data and minimal python code to 
 generate figure 1,2 and 4 of the paper, as well as the other figures mentionned but not shown in the paper.

The data is contained in the subfolders 
512, 4096 in the form of .dill files, Python pickling format, containing all relevant PDF.
The script Dill2mat.py  converts from dill to Matlab .mat format.

Data is analysed with the python scripts:

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
- Currently choices of Lambda for the 4096  reduce to 1/2 2, corresponding to reported Figure 4 in the submission, unlike what is written in the 4096_minimal.py file.
Full data is available on request.

@author: Simon Thalabard simon.thalabard@ens-lyon.org
***

