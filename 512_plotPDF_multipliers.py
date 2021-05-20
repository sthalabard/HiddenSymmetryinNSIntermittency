"""
Auxilliary script for the script 512_minimal.py 
Plots the PDF of the multipliers displayed in Fig 2

@author: sthalabard
Created on Fri Mar 12 13:15:54 2021
"""

#%% MULTIPLIERS FOR PAPER 512**3
#%%
cauchy=lambda x : (1/pi)/(x**2+1)

#%% Load file
file=join('512','512_HS_vx_multiplier__full.dill')
out=load_dill(file)
#%% 
fig,ax=newfig(1,1,num='2: Lambda = %d: pdf' %(np.log2(LAMBDA),))
PDFS,BINS=out.pdfs,out.bins
axi = inset_axes(ax, width="45%", height="40%", loc='upper right',borderpad=0.4)
axs=[ax,axi]

tweaks=dic2struc() #structure to save the x-shifts and scaling of the data
tweaks.r1,tweaks.xshift,tweaks.scale=[],[],[]

shiftLAMBDA=int(np.log2(LAMBDA))
for i in np.arange(len(out.R0s)-1,-1,-1):
    j=i+shiftLAMBDA
    if j<0 or j>len(out.R1s)-1:continue
    r1, r1_eta=out.R1s[j], out.R1s[j]*out.param.dx/out.param.eta
    if r1_eta<INERTIALRANGE[0]:continue
    if r1_eta>INERTIALRANGE[1]:continue

    #Smooth and rescale data
    #maximum is determined from smoothing the data
    pslin,bslin=smooth_pdf(PDFS[i,j,:],BINS,nbins=128,scale='linear')
    itmp=np.argmax(pslin[ix])
    xshift=bslin[ix][itmp]

    ps,bs=smooth_pdf(PDFS[i,j,:],BINS,logmin=-8,nbins=64+1)
    tweaks.xshift.append(xshift)
    tweaks.r1.append(r1_eta)

    #Scaling is determing from position of maximum
    tmp=scp.interpolate.interp1d(bs-xshift,ps)
    scale=1/(tmp(0)*pi)
    tweaks.scale.append(scale)

    if CENTERING is False: xshift=0
    xdata, ydata =(BINS-xshift)/scale,scale*PDFS[i,j,:]
    xdata_smooth, ydata_smooth =(bs-xshift)/scale,scale*ps

    for ax in axs:
        c=cosmetics.coolR(r1)
        lw=cosmetics.lw(r1)
        ax.plot(xdata,ydata,c=c,lw=1,alpha=0.02)
        ax.plot(xdata_smooth,ydata_smooth,c=c,lw=lw,alpha=1,label='$%0.1f $' %(r1_eta,))
#%
for ik,key in enumerate(tweaks.__dict__.keys()):
    tweaks.__dict__[key]=np.array(tweaks.__dict__[key])

#%INDICATIVE FITs
xshiftmean=(tweaks.xshift/tweaks.scale).mean()
print(xshiftmean)
#if CENTERING: xshiftmean=0
#if LAMBDA==4:
#    xshiftmean=0.5
#if LAMBDA==16:
#    xshiftmean=0.23

for ax in axs:
    x=np.linspace(-512,512,32*512)
    ax.plot(x,cauchy(x-xshiftmean),'k--',lw=2,label=None,alpha=1)

ax=axs[0]
ax.set_xlim(-2,2)
ax.set_ylim(0,0.6)
ax.set_yscale('linear')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], ncol=1,frameon=True,title='$\\ell/\\eta$', loc='upper left')
ax.set_xlabel('$w_\\parallel (\\ell,2^{%d}\\ell)/\\gamma$'  %(-np.log2(LAMBDA),))
ax.set_ylabel('PDF')
ax.grid()
x=np.linspace(-512,512,32*512)
arrowprops={'arrowstyle':'->','color':'black'}
ax.annotate(s=' Cauchy($w_\\lambda$,1) \n \hspace{0.2cm}$w_\\lambda=%0.2f$' %(xshiftmean,),xy=(-0.5,cauchy(-0.5-xshiftmean)),xytext=(-0.3,0.1),arrowprops=arrowprops)

ax.set_yticks([0,0.2,0.4])
ax.set_yticklabels([0,0.2,0.4])

ax=axs[1]
ax.set_xlim(-256,256)
ax.set_ylim(1e-6,2)
ax.set_yscale('log')
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.grid()