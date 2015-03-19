import numpy as np
import matplotlib.pyplot as plt
import pdb
import collections
import pandas as pd 

# let's see if any of my imports work...
import WC_net_class as WC
import stim_maker_WC as sm 

T=500
stim = np.zeros((5,T))

tmp = sm.stim_maker_WC(T=T, ITI=100, df=0)
# add pooled inhibition and feedback (no stim) entry
stim[:3,:] = tmp
stim[3,:] = sum(stim[:3,:])

stim_rev = stim[(1,0,2,3,4),:]
# empty out the registry so we get a new network
WC.WC_net_unit._registry=[]
try:
	del U1, U2, U3, fastInh, slowInh
except NameError:
	pass


excParsDict = dict(ke=0.1, the=0.5, kS=0.1, thS=0.8, gee = 0.8, 
	gSFA = .5, tauA = 50)
# low threshold to increase FR, high threshold to activate NMDARs, sensitive to stim
excParsDict.update(gStim=.5)

U1=WC.WC_net_unit(**excParsDict)

excParsDict.update(gStim=.25)

U2=WC.WC_net_unit(**excParsDict)
U3=WC.WC_net_unit(**excParsDict)

slowInh = WC.WC_net_unit(tau=50)
fastInh = WC.WC_net_unit(tau=5, the = .5, gSFA = 0.3, gee = 0.8, tauA = 50)

gFB_exc = 1
gFB_ie = -.2
gFB_ii = -1
gFF_ie = -.1 

fastInh.addNewCurrent(source=U1.r,weight=gFB_exc,name="FB_exc_1")
fastInh.addNewCurrent(source=U2.r,weight=gFB_exc,name="FB_exc_2")
fastInh.addNewCurrent(source=U3.r,weight=gFB_exc,name="FB_exc_3")

slowInh.addNewCurrent(source=fastInh.r,weight=gFB_ii,name="FB_inh")
U1.addNewCurrent(source=fastInh.r,weight = gFB_ie, name="FB_inh")
U2.addNewCurrent(source=fastInh.r,weight = gFB_ie, name="FB_inh")
U3.addNewCurrent(source=fastInh.r,weight = gFB_ie, name="FB_inh")


U2.addNewCurrent(source=U1.S,weight=.3,name="NMDA_12")
U1.addNewCurrent(source=slowInh.r,weight=-.1,name="FF_inh")
U2.addNewCurrent(source=slowInh.r,weight=-.1,name="FF_inh")
U3.addNewCurrent(source=slowInh.r,weight=-.1,name="FF_inh")
U3.addNewCurrent(source=U2.S,weight=.3,name="NMDA_23")


netnames=["E1","E2","E3","FF inhibitor","FB disinhibitor"]

# forward
WC.WC_net_unit.integrator(stimSource=stim, T=T)
WC.WC_net_unit.plot_timecourses(netnames)
#U2.plot_derivatives("each")

# reverse
WC.WC_net_unit.integrator(stimSource=stim_rev)
WC.WC_net_unit.plot_timecourses(netnames)
plt.title("reverse")
U2.plot_derivatives("each")

# if 1:
# #fig = plt.figure()
# #tmp = plt.gca()
# #plt.title('foo-bar')
# #tmp.axes.get_xaxis().set_ticks([]) # turn off those nasty ticks
# #tmp.axes.get_yaxis().set_ticks([])
# #plt.xlabel('time')

# 	nUnits = len(WC.WC_net_unit._registry)

# 	fig, axes = plt.subplots(nrows=nUnits)

# 	for ind in xrange(nUnits):
# 		unit=WC.WC_net_unit._registry[ind]

# 		ax=axes[ind]
# #		plt.legend(loc='right')
# 		#plt.title(netnames[ind])
# 		unit.records.plot(ax=ax)
# 		ax.set_title(netnames[ind])
# 		ax.legend(loc='right')

# 		#title(str(ind+1)) 
# 	# plot(tax,E,'b')
# 	# plot(tax,I,'r')
# 	# plot(tax,Inp_e,'g')
# 	plt.show(block=False)