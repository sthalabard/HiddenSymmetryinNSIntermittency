"""
Auxilliary script for the script 512_minimal.py 
Plots the PDF of fig 1

@author: sthalabard
Created on Fri Mar 12 13:15:54 2021
"""

out=load_dill('512/512_K62_vx.dill')
out.__dict__
out.eta=param.eta

#%% Parameter for the cosmetics
cosmetics=dic2struc()
cosmetics.coolR=lambda u: cm.cubehelix(np.log2(2*u)/np.log2(2048))
cosmetics.lw=lambda r1:2+0.5*np.log2(r1/4)

#%%  FIGURE 1 a : PDF DV 512
fig,ax=newfig(1,1,num='1a : PDF of increments')
axi = inset_axes(ax, width="30%", height="30%", loc='upper right',borderpad=0.1)
axs=[ax,axi]

#Inset log scale
ax=axs[1]
ax.set_yscale('log')
ax.set_ylim(1e-4,1e4)
ax.set_xlim(-16,16)
for i,r in enumerate(out.R0s):
    c=cosmetics.coolR(r)
    lw=cosmetics.lw(r)

    if i%2==1: continue
    dec=2**((len(out.R0s)-1-i))
    ps,bs=smooth_pdf(out.pdfs[i,:],out.bins,logmin=-7,nbins=32)

    ix=np.flatnonzero(ps>1e-8)
    ax.plot(out.bins,dec*out.pdfs[i,:],c=c,lw=lw,alpha=0.1)
    ax.plot(bs[ix],ps[ix]*dec,\
            c=c,lw=lw,label='$%0.1f$' %(r*out.param.dx/out.param.eta,))
gauss=np.sqrt(1/(2*pi))*np.exp(-out.bins**2*0.5)
ax.plot(out.bins,gauss*dec,'k--',lw=3,label=None,alpha=1)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(labelsize=20)

#% Main Panel
ax=axs[0]
ax.set_yscale('linear')
ax.set_ylim(0,0.7)
ax.set_xlim(-3,3)
ax.set_yticks([0,0.2,0.4])
ax.set_ylim(0,0.6)
ax.set_xlim(-2,2)
ax.set_xlabel('$\\Delta u_\\parallel/S_2^{1/2} $')
ax.set_ylabel('PDF')
ax.grid()

for i,r in enumerate(out.R0s):
    c=cosmetics.coolR(r)
    lw=cosmetics.lw(r)
    if i%2==1: continue
    ax.plot(out.bins,out.pdfs[i,:], \
            c=c,lw=lw,alpha=1,label='$%0.1f$' %(r*out.param.dx/out.param.eta,))

ax.plot(out.bins,gauss,'k--',lw=3,label=None,alpha=1)
ax.annotate(s='Unit Gaussian $\longrightarrow$',xy=(-0.4,0.2))
ax.legend(ncol=1,frameon=True,loc='upper left', title='$\\ell/\\eta$')

figs1a,axs1a=fig,axs

#%% Fig 1b,  Structure Functions and extended self-similarity
#Left panel shows fit of structure functions (not shown in paper)
#Right panel shows corresponding zeta_p behavior

fig,axs=newfig(1,2,num='1b :ESS')
axi = inset_axes(axs[1], width="45%", height="40%", loc='upper left',borderpad=.9)
axs=[axs[0],axs[1],axi]

#Left panel
ax=axs[0]
coolp=lambda u:cm.Blues(u/10)
ax.set_xlim(1e-1,3e2)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('$S_3/\\epsilon \\eta$')
ax.set_ylabel('$S_p^{3/p}/S_3$')
f=fig.canvas
ax.grid()

#imin, imax determine fitting range, and subsequent error estimate
tmpmin=[]
tmpmax=[]
imin=[0,0,0,4,3,2,1,1,1,1]
imax=[-8,-7,-6,-2,-3,-4,-5,-2,-1,-5]

prange=np.arange(9)
for i,p in enumerate(prange[-1::-1]):
    if p==0:
        tmpmin.append(0)
        tmpmax.append(0)
        continue
    y=out.S[:,p]**(1/p)
    tmp=[]
    for ista,iend in itertools.zip_longest(imin,imax):
        x=out.S[:,3]/(out.param.eps*out.param.eta)
        y=out.S[:,p]**(3/p)/out.S[:,3]
        po=np.polyfit(np.log(x[ista:iend]),np.log(y[ista:iend]),1)
        tmp.append(po[0])
    tmpmin.append(np.asarray(tmp).min())
    tmpmax.append(np.asarray(tmp).max())

    ax.plot(x,y,'o--',c=coolp(p),lw=0.6,ms=14,markeredgecolor='k',label='%d' %(p,))
    fit=x**po[0]*np.exp(po[1])
    ax.plot(x[ista:iend],fit[ista:iend],'--',c='k')

ax.legend(title='p',ncol=1,frameon=True)

#Right panel
ax=axs[1]
ax.set_xlabel('$p$')
ax.set_ylabel('$\\zeta_p$')
ax.grid()
ximin=(np.asarray(tmpmin)[-1::-1]+1)*prange/3 
ximax=(np.asarray(tmpmax)[-1::-1]+1)*prange/3
ps=np.arange(len(tmpmin))

for p in ps:
    ax.plot([p,p],[ximin[p],ximax[p]],'o-',lw=2,c='k',ms=7)
    
ax.plot(ps,ps/3,lw=2,ls='--',label='p/3',c='firebrick')
c2=0.026

c1=(1/3+3*c2/2)
xi=lambda u:u*(1/3+1.5*c2)-0.5*c2*u**2
D=lambda h:3-(h-c1)**2/(2*c2) #singularity spectrum

ax.plot(ps,xi(ps),lw=2,label='$c_1\; p - c_2 \\; p^2/2$\n $c_2=%0.3f$' %(c2,),c='midnightblue')
arrowprops={'arrowstyle':'->','color':'midnightblue'}
ax.annotate(s=' Refined self-similarity\n \t \\quad $ c_1\; p - c_2 \\; p^2/2$',xy=(5.3,1.6),xytext=(5.5,1.2),fontsize=25,color='midnightblue',arrowprops=arrowprops)
arrowprops={'arrowstyle':'->','color':'firebrick'}

ax.annotate(s=' Pure self-similarity\n $ p/3 $',xy=(5.5,1.85),xytext=(4,2),fontsize=25,color='firebrick',arrowprops=arrowprops)

#Inset of right panel :Legendre Transform of RSS
ax=axs[2]
h=np.linspace(-2,2,100)
ax.plot(h,D(h),lw=2,c='k',label='$3-\\frac{(c_1-h)^2}{2\\;c_2}$')

ax.set_ylim(0,3)
ax.set_xlim(0,0.8)
ax.set_xticks([0,1/3])
ax.set_xticklabels(['0','1/3'])
ax.annotate(s='$c_1 = %0.2f$' %(c1,),xy=(0.4,1.5),fontsize=20,color='midnightblue')
ax.annotate(s='$D(h)$',xy=(0.005,2.5),fontsize=24,color='black',rotation=0)
ax.annotate(s='$h$',xy=(0.7,0.1),fontsize=24,color='black',rotation=0)
arrowprops={'arrowstyle':'->','color':'k'}

ax.annotate(s='$ 3- \\frac{(c_1-h)^2}{2c_2}$',xy=(0.03,0.9),xytext=(0.1,0.5),fontsize=25,color='k',arrowprops=arrowprops)

ax.set_xticks([0,1/3])
ax.set_xticklabels(['0','$1/3$'])
ax.grid()
ax.tick_params(labelsize=24)
ax.axvline(c1,lw=2,ls='dashed',c='midnightblue')

figs1b,axs1b=fig,axs
