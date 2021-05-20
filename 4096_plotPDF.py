"""
Auxilliary script for the script 4096_minimal.py 
Plots the hidden PDF of  Fig 4

@author: sthalabard
Created on Fri Mar 12 13:15:54 2021
"""

#%% LOAD PDF
file=join('4096','4096_%s_D%0.3f.dill' %(RESCALING,LAMBDA))
print('loading ' + file)
out=load_dill(file)
out.__dict__
print('done')

if USE_JACOBIAN:
    PDFS,BINS=out.par.pdfs_w,out.bins
else:
    PDFS, BINS=out.par.pdfs, out.bins

#%% CREATE PLOT
fig,ax=newfig(1,1,num='%s $\\Lambda=2^{%d}$' %(RESCALING, np.log2(LAMBDA),))
properties={ 'width':"45%", 'height':"40%", 'loc':'lower center','borderpad':1.3}
axi = inset_axes(ax,**properties)
axs=[ax,axi]

tweaks=dic2struc() #structure to save the x-shifts and scaling of the data
tweaks.r0,tweaks.xshift,tweaks.scale=[],[],[]

for i in range(len(out.R0s)-1,-1,-1):

    #Find and smooth data
    r0,r0_eta=out.R0s[i], out.R0s[i]*out.param.dx*0.5/out.param.eta # Zooming scale in units dx/2 and  in units of eta
    r1, r1_eta=r0*LAMBDA,r0_eta *LAMBDA # Observing scale in units dx/2 and in units of eta

    if r1 not in out.R0s: print(r1,'not available.... skipping!')
    if min(r1_eta,r0_eta)<INERTIALRANGE[0]:continue
    if max(r1_eta,r0_eta)>INERTIALRANGE[1]:continue

    ps,bs=smooth_pdf(PDFS[i,:],BINS[i,:],logmin=np.log10(cosmetics.pdfcutoff),nbins=33)

    if cosmetics.binslin is not None:
        pslin,bslin=smooth_pdf(PDFS[i,:],BINS[i,:],nbins=cosmetics.binslin,scale='linear')
    else:
        pslin,bslin=PDFS[i,:].copy(),BINS[i,:].copy()

    #Scale data
    ix=np.flatnonzero(PDFS[i,:]>1e-1)
    xshift=(BINS[i,ix]*PDFS[i,ix]).sum()/PDFS[i,ix].sum()
    tmp=scp.interpolate.interp1d(bs,ps)
    scale=1/(tmp(0)*pi)

    if CENTERING is False: xshift=0
    tweaks.xshift.append(xshift); tweaks.scale.append(scale); tweaks.r0.append(r0)

    xdata, ydata =(BINS[i,:]-xshift)/scale,scale*PDFS[i,:]
    xdata_smooth, ydata_smooth =(bs-xshift)/scale,scale*ps
    xdatalin_smooth, ydatalin_smooth =(bslin-xshift)/scale,scale*pslin

    #
    for iax,ax in enumerate(axs):
        c=cosmetics.coolR(r1)
        lw=cosmetics.lw(r1)
        if iax==0:
            dec=1
            ax.plot(xdatalin_smooth,ydatalin_smooth,\
                    c=c,lw=lw,alpha=1,label='$%0.0f$' %(r0_eta,))
            
        if iax==1:
            ax.plot(xdata,ydata,c=c,lw=0.5,alpha=0.03) #unsmoothed data
            ax.plot(xdata_smooth,ydata_smooth,\
                    c=c,lw=lw,alpha=1,label='$%0.0f$' %(r0_eta,))


#% LABELS and legends
for iax,ax in enumerate(axs):
    ax.grid()

    if iax==1:
        ax.set_yscale('log')
        ax.set_ylim(1e-9,1)
        ax.set_xlim(-10,10)
        ax.set_xlabel(None)
        ax.set_ylabel(None)
        ax.tick_params(labelsize=30)
        
#        ax.annotate(s='$ |U_\\parallel|^{-%0.1f} \\rightarrow$' %(expofit,),xy=(-60,8e-5),fontsize=25)

    elif iax==0:
        ax.set_xlim(-3,3)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], ncol=1,frameon=True,title='$\\ell/\eta$', loc='upper right')

        ax.set_yticks([0,0.2,0.4,0.6])
        ax.set_yticklabels([0,0.2,0.4,0.6])
        ax.set_ylim(0,0.4)
        ax.set_xlabel('$ U_\\parallel \;/\\gamma$')

        if USE_JACOBIAN:
            ax.set_ylabel('hidden PDF')
        else:
            ax.set_ylabel('PDF')

        if LAMBDA>=1:
            lambdalabel='$\\lambda = %d$' %(LAMBDA,)
        else :
            lambdalabel='$\\lambda = 1/%d$' %(1/LAMBDA,)
        ax.annotate(s=lambdalabel,xy=(-1.8,0.35),fontsize=40)

#% Good rendering for various rescaling and fits
ax=axs[1]
if RESCALING is 'kolmogorov':
    ax.set_ylim(1e-7,1)
    ax.set_xlim(-16,16)

if RESCALING is 'DV2':
    ax.set_ylim(1e-7,1)
    ax.set_xlim(-13,13)

if RESCALING is 'DV_rand':
    ax.set_ylim(1e-7,1)
    ax.set_xlim(-128,128)
    tmp=scp.interpolate.interp1d(xdata_smooth,ydata_smooth)
    if USE_JACOBIAN:expotails=3
    else:expotails=2
    xfit=5
    tmpx=np.linspace(xfit,256,1024)
    fun=lambda x:  tmp(xfit)*np.abs(x/xfit)**(-expotails)
    ax.plot(tmpx,fun(tmpx),'k--',lw=2)

    tmpx=np.linspace(-xfit,-256,1024)
    ax.plot(tmpx,fun(tmpx),'k--',lw=2)
    ax.annotate(s='$ |U_\\parallel|^{-%0.1f} \\rightarrow$' %(expotails,),xy=(-120,2e-4),fontsize=25)



if RESCALING is 'DV3_ABS':
    ax.set_ylim(1e-9,1)
    ax.set_xlim(-64,64)
#    ax.set_xlim(1,64)
#    ax.set_xscale('log')
    tmp=scp.interpolate.interp1d(xdata_smooth,ydata_smooth)

    if USE_JACOBIAN:expotails=5
    else:expotails=4
    xfit=5
    tmpx=np.linspace(xfit,64)
    fun=lambda x:  tmp(xfit)*np.abs(x/xfit)**(-expotails)
    ax.plot(tmpx,fun(tmpx),'k--',lw=2)

    tmpx=np.linspace(-xfit,-64)
    ax.plot(tmpx,fun(tmpx),'k--',lw=2)
    ax.annotate(s='$ |U_\\parallel|^{-%0.1f} \\rightarrow$' %(expotails,),xy=(-60,8e-5),fontsize=25)