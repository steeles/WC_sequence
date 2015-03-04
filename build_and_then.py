import numpy as np
import matplotlib.pyplot as plt
import pdb
import collections
import pandas as pd 

# let's see if any of my imports work...
import WC_net_class as WC
import stim_maker_WC as sm 

# empty out the registry so we get a new network
WC.WC_net_unit._registry=[]

foo=WC.WC_net_unit(gSFA=.7,gee=0,r0=0.5,the=0., gStim=0.6)
bar=WC.WC_net_unit(gSFA=.7,gee=0, the=0., gStim=0.6)

foo.addNewCurrent(bar.r,-1,"bar_inh_foo")

bar.addNewCurrent(foo.r,-1,"foo_inh_bar")

netnames=["foo","bar"]

WC.WC_net_unit.integrator(T=5000)

if 1:
#fig = plt.figure()
#tmp = plt.gca()
#plt.title('foo-bar')
#tmp.axes.get_xaxis().set_ticks([]) # turn off those nasty ticks
#tmp.axes.get_yaxis().set_ticks([])
#plt.xlabel('time')

	nUnits = len(WC.WC_net_unit._registry)

	fig, axes = plt.subplots(nrows=nUnits)

	for ind in xrange(nUnits):
		unit=WC.WC_net_unit._registry[ind]

		ax=axes[ind]
#		plt.legend(loc='right')
		#plt.title(netnames[ind])
		unit.records.plot(ax=ax)
		ax.set_title(netnames[ind])
		ax.legend(loc='right')

		#title(str(ind+1)) 
	# plot(tax,E,'b')
	# plot(tax,I,'r')
	# plot(tax,Inp_e,'g')
	plt.show(block=False)