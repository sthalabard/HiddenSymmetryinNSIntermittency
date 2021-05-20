#! path~to/anaconda3/bin/python3.8
# -*- coding: utf-8 -*-

"""
Converts dill files to mat files

Requires python 3.8 and the packages listed in the start_up file 'init_python.py'

@author: Simon Thalabard
"""

#%% Startup File
startup_file='init_python.py'
exec(open(startup_file).read())
join=os.path.join

folder='512'
outfolder='512_mat'
if not os.path.exists(outfolder):
    os.mkdir(outfolder)

for file in glob.glob(join(folder,'*.dill')):
    outfile=file.split(sep='.dill')[0]+'.mat'
    outfile=join(outfolder,outfile.split(sep='/')[1])
    out=load_dill(file)
    print(outfile)
    scp.io.savemat(outfile,out.__dict__) 
