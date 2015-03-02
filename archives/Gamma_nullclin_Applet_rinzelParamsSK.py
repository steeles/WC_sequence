
# Stephen Keeley, 2014

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib as mpl
import scipy as scipy
import scipy.fftpack



plt.close("all")


def pars():
    '''
    Return default parameters for Wong & Wang (2006) reduced model
    '''
    z = {}
    ### Stimulus Parameters ###

    z['mu0'] = 1. # Stimulus firing rate [Hz]


    ### Network Parameters ###

    z['tauAM'] = 2 # AMPA Synaptic time constant [sec] !!! Ampa assumed fast (ds/dt = 0)
    z['tauGABA'] = 10 # GABA Synaptic time constant [sec] !!! Gaba assumed fast (ds/dt = 0)
    z['gamma'] = 0.641 # Saturation factor for gating variable for NMDA
    z['alpha_1'] = 3 # Scake for AMPA synapse
    z['alpha_2'] = 4 # Scake for GABA synapse
    z['tau0'] = 1 # Noise time constant [sec]
    z['g_AM_E'] =15# Noise magnitude [nA]
    z['g_AM_I'] = 45# Noise magnitude [nA]
    z['g_GABA_E'] = 25 # Noise magnitude [nA]
    z['g_GABA_1'] = 0 # Noise magnitude [nA]
    
    
    ### Time Paramters
    z['tmax'] = 150# Total duration of simulation [sec]    
    z['dt'] = 0.01 # Integration dt}
    return z


# FI curve Definition


def F_E(I, the=.3, ke=0.2):
    """F(I) for vector I for the inhibitory curve"""
    #return I*200
    return 1/(1+np.exp(((the-I)/ke)))
    
    
def F_I(I, thi=0.4, ki =0.1):
    
    """F(I) for vector I for the excitatory curve. Adapted from Wong Wang 2006"""
    #return I*200
    return 1/(1+np.exp(((thi-I)/ki)))
    
def SeInf_I(I, thse=.4, kse=0.1):

    return 1/(1+np.exp((thse-I)/kse))
    
def SiInf_I(I, thsi=.4, ksi=0.1):

    return 1/(1+np.exp((thsi-I)/ksi))

    
#define dynamics of the model     
def dyn_fn(Sinit, pars): # Integrates trajectory for FitzHugh-Nagumo
    x = np.zeros(( len(Sinit), int(pars['tmax']/pars['dt'])))

    #x[0] = Sinit
    
    r_I = np.zeros(int(pars['tmax']/pars['dt']))
    r_E = np.zeros(int(pars['tmax']/pars['dt']))
    I_E = np.zeros(int(pars['tmax']/pars['dt']))
    I_I = np.zeros(int(pars['tmax']/pars['dt']))  
    
    
    S_AM = x[0]
    S_GABA = x[1]    
    
    S_AM[0] = Sinit[0]
    S_GABA[0] = Sinit[1]
    
    for t in xrange(1,int(pars['tmax']/pars['dt'])):
        
        Istim1 = pars['mu0']     
        Istim2 = 0
        
    
        
        I_E[t-1] = F_E(pars['g_AM_E']*S_AM[t-1] - pars['g_GABA_E']*S_GABA[t-1]  + Istim1) #+ Ieta1[t]
        I_I[t-1] = F_I(pars['g_AM_I']*S_AM[t-1] - pars['g_GABA_I']*S_GABA[t-1] + Istim2) #+ Ieta2[t]
        


        r_E[t-1]  = SeInf_I(I_E[t-1])
        r_I[t-1]  = SiInf_I(I_I[t-1])
        
        [dSAdt, dSGdt] = eqs_fn(S_AM[t-1],S_GABA[t-1],pars,r_I[t-1],r_E[t-1])
        S_AM[t] = S_AM[t-1] + pars['dt']*dSAdt           
        S_GABA[t] = S_GABA[t-1] + pars['dt']*dSGdt
        
    
    x = np.array([S_AM, S_GABA, I_E, I_I])
    print r_E
    return x

def eqs_fn(SA,SG,pars,r_I,r_E): # Dynamical equations for FitzHugh-Nagumo, returns derivatives
    dSAdt = (-SA/pars['tauAM'] + (1-SA)*pars['alpha_1']*r_E/pars['tauAM'])
    dSGdt = (-SG/pars['tauGABA'] + (1-SG)*pars['alpha_2']*r_I/pars['tauGABA'])
    z = np.array([dSAdt, dSGdt])
    return z

# initialize variables


pars = pars()

# Set plotting properties
params = {'axes.labelsize': 16,
          'text.fontsize': 16,
          'legend.fontsize': 12,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10}
mpl.rcParams.update(params)
mpl.rc('mathtext', fontset='stixsans',default='regular')

# Make figure
fig = plt.figure(figsize=(10,10))
ax = fig.add_axes([.07,.1,.85,.275])
ax1 = fig.add_axes([.07,.475,.425,.425])
ax.set_ylim(0,1)
ax1.set_xlim(-0.1,1)
ax1.set_ylim(-0.1,1)
ax.set_xlabel('Time')
ax.set_ylabel('Synaptic Paramter')

axcolor = 'lightgoldenrodyellow'
axsInject = plt.axes([0.6, 0.7, 0.35, 0.04], axisbg=axcolor)
axsg_AM_E  = plt.axes([0.6, 0.65, 0.35, 0.04], axisbg=axcolor)
axsg_AM_I  = plt.axes([0.6, 0.6, 0.35, 0.04], axisbg=axcolor)
axsg_GABA_E  = plt.axes([0.6, 0.55, 0.35, 0.04], axisbg=axcolor)
axsg_GABA_I  = plt.axes([0.6, 0.50, 0.35, 0.04], axisbg=axcolor)
axstau_G  = plt.axes([0.6, 0.45, 0.35, 0.04], axisbg=axcolor)
axstau_A  = plt.axes([0.6, 0.40, 0.35, 0.04], axisbg=axcolor)
axh = plt.axes([-1,-1,1,1])




# Make sliders that control parameters
sInj = Slider(axsInject, r'Current', 0, 2, valinit=0.14,color='maroon')
sg_AM_E = Slider(axsg_AM_E, r'AM E', 0, 10.0, valinit=1.8,color='midnightblue')
sg_AM_I = Slider(axsg_AM_I, r'AM I', 0.0, 10.0, valinit=1,color='midnightblue')
sg_GABA_E = Slider(axsg_GABA_E, r'GABA E', 0.0, 10.0, valinit=3.7,color='midnightblue')
sg_GABA_I = Slider(axsg_GABA_I, r'GABA I', 0.0, 10.0, valinit=.5,color='midnightblue')
stau_G = Slider(axstau_G, r'Tau GABA', 0.0, 20, valinit=10,color='midnightblue')
stau_A = Slider(axstau_A, r'Tau AMPA', 0.0, 20, valinit=2,color='midnightblue')
sxinit = Slider(axh ,'x',-5,5,valinit=0)
syinit = Slider(axh,'y',-5,5,valinit=0)


# Plot trajectories and nullclines
l, = ax.plot(0,0, lw=2, color='b',label='E Synapse')
lb, = ax.plot(0,0, lw=2, color='r',label='I Synapse')
l1 = ax.legend(loc=2,frameon=False)
l1, = ax1.plot(0,0, lw=2, color='k')


as_lim = (0, 1)
gs_lim = (0, 1)
#for flowfeild arrows
aes = np.linspace(as_lim[0], as_lim[1],20)
gees = np.linspace(gs_lim[0], gs_lim[1],20)
as_grid, gs_grid = np.meshgrid(aes, gees)

#q1 = ax1.quiver(as_grid,gs_grid,0*as_grid,0*gs_grid,scale=25,
               # scale_units='xy',angles='xy',headwidth=3,width=0.005,
              #  facecolor='gray')



#for trav
'''
aes = np.linspace(as_lim[0], as_lim[1],20)
gees = np.linspace(gs_lim[0], gs_lim[1],20)
as_grid, gs_grid = np.meshgrid(aes, gees)
'''



# Add figure text
fig.text(.5,.95,'Gamma Model',ha='center',size=18)

fig.text(.68,.90,r'$\frac{dS_{AMPA}}{dt} = - \frac{S_{AMPA}}{\tau_{AMPA}} -\alpha_1 FR_E $',size=14,color='r')
fig.text(.68,.85,r'$\frac{dS_{GABA}}{dt} = - \frac{S_{GABA}}{\tau_{GABA}} -\alpha_2 FR_I$',size=14,color='b')

fig.text(.625,.80,r'$I_E = g_{AM_E}S_{AM} - g_{GABA_E} S_{GABA}  + I_{stim1}$',size=14,color='k')
fig.text(.665,.75,r'$I_I = g_{AM_I}S_{AM} - g_{GABA_I} S_{GABA}$',size=14,color='k')



def plot_flow_field(ax,x,y,dxdt,dydt,n_skip=1,scale=None,facecolor='gray'):
    v = ax.quiver(x[::n_skip,::n_skip], y[::n_skip,::n_skip], 
              dxdt[::n_skip,::n_skip], dydt[::n_skip,::n_skip], 
              angles='xy', scale_units='xy', scale=scale,facecolor=facecolor, linewidths = widths)
    return v 

def plot_nullcline(ax,x,y,z,color='k',label=''):
    
    #SA = - (pars['tauAM']*pars['alpha_1'])*r_E
    nc = ax.contour(x,y,z,levels=[0],colors=color, linewidths = 2.0) # S1 nullcline
    
    nc.collections[0].set_label(label)
    return nc

# Update initial condition and parameters





def update(val):
    


    ax1.cla()
    
    l1, = ax1.plot(0,0, lw=2, color='k')
    
    #q1 = ax1.quiver(as_grid,gs_grid,0*as_grid,0*gs_grid,scale=25,
    #            scale_units='xy',angles='xy',headwidth=3,width=0.005,
    #            facecolor='gray')
    ax1.set_xlabel('S AMPA')
    ax1.set_ylabel('S GABA')
    
    Sinit = [sxinit.val,syinit.val]
    
    
    pars['g_AM_E'] = sg_AM_E.val
    pars['g_AM_I'] = sg_AM_I.val
    
    pars['g_GABA_E'] = sg_GABA_E.val
    pars['g_GABA_I'] = sg_GABA_I.val
    

    pars['mu0'] = sInj.val
    
    pars['tauGABA'] = stau_G.val
    pars['tauAM'] = stau_A.val
    
    #current 

    
    I_E = F_E(pars['g_AM_E']*as_grid- pars['g_GABA_E']*gs_grid  + pars['mu0']) #+ Ieta1[t]
    I_I = F_I(pars['g_AM_I']*as_grid  - pars['g_GABA_I']*gs_grid) #+ Ieta2[t]
    
    
    r_I  = SeInf_I(I_I)
    r_E  = SiInf_I(I_E)

    
    m = dyn_fn(Sinit,pars)
    t = np.linspace(0,pars['tmax'],int(pars['tmax']/pars['dt']),endpoint=False)
    
    l.set_xdata(t)
    l.set_ydata(m[0,:])
    lb.set_xdata(t)
    lb.set_ydata(m[1,:])
    ax.set_xlim(0,pars['tmax'])
    
    

    #l1.set_xdata(m[0,:])
    #l1.set_ydata(m[1,:])



    z = eqs_fn(as_grid,gs_grid,pars,r_I, r_E)
    dx, dy = z[0],z[1]
    
    #plot_flow_field(ax,as_grid,gs_grid,dx,dy,n_skip=12,scale=40)]
    plot_nullcline(ax1, as_grid, gs_grid, dx, color='blue', label='S1 nullcline')
    plot_nullcline(ax1, as_grid, gs_grid, dy, color='red', label='S1 nullcline')
    plt.legend(loc=1)
    # w nullcline

    q1.set_UVC(dx,dy)
    
    
    #fft
    maxi = np.max(m[0,1000:])
    mini = np.min(m[0,1000:])
    half = maxi-mini
    periodarray = []

    for t in xrange(1,int(pars['tmax']/pars['dt'])):
        if m[0,t]>half and m[0,t-1]<half:
            periodarray.append(t)
    if len(periodarray) >2:
        print 1000/float(periodarray[-2]-periodarray[-1]),  pars['mu0']
                
    
                
    plt.draw()
sInj.on_changed(update)
sg_AM_E.on_changed(update)
sg_AM_I.on_changed(update)
sg_GABA_E.on_changed(update)
sg_GABA_I.on_changed(update)
stau_G.on_changed(update)
stau_A.on_changed(update)





# Make reset button


# Make mouse event to set initial conditions for trajectory
def onpick4(event):
    if event.inaxes == ax1:
        sxinit.val = event.xdata
        syinit.val = event.ydata
        update(0)

fig.canvas.mpl_connect('button_press_event',onpick4)

plt.show(block=False)

