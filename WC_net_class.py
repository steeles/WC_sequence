# basic bare bones WC unit
# this guy wants to know its parameters and how to update its value
#from numpy import exp
#print "exp loaded"
import numpy as np
import matplotlib.pyplot as plt
import pdb
import collections
import pandas as pd 

Current = collections.namedtuple("Current", ['source','weight'])
'''if i need to make changes to the default parameters,
i should do it here'''

defaultPars=dict(		
				ke=.1,the=.2,  # IO params
				kS=.1,thS=.5,
				r0=0., a0=0.,S0=0.,stim0=1., # time varying values
				gee=.57,
				gStim=1.,
				gSFA=0,

				tau=10.,tauNMDA=100., tauA=200., G=.64)


class WC_net_unit(object):

	_registry = []

	""" Creates a basic WC unit. To assign pars from a dictionary, 
	use WC_unit(**parsDict) """

	"""adding capacity for units to form connections with other units"""

	def __init__(self,**kwargs):
		self.__dict__.update(defaultPars, **kwargs)
		# update the registry; this 
		print self
		self._registry.append(self) 

		self.currents = dict()
		self.cxParams = dict()
		self.r=[self.r0]
		self.a=[self.a0]
		self.S=[self.S0]
		self.stim=[self.stim0]


		self.init_intrinsicCurrents()

	def init_intrinsicCurrents(self):
		if self.gee != 0:
			self.addNewCurrent(source=self.r,weight=self.gee,name="self_excitation")

		if self.gStim != 0:
			self.addNewCurrent(source=self.stim,weight=self.gStim,name="stim_current")

		if self.gSFA != 0:
			self.addNewCurrent(source=self.a,weight=-self.gSFA,name="SFA")

	def getCxParams(self):
		return self.cxParams

# wanna be able to do with one or many
	def setCxParams(self,new_connections_dict):
		self.cxParams.update(new_connections_dict)

# probably with this one too
	def addNewCurrent(self,source, weight, name):
		
		self.currents[name] = Current(source=source,weight=weight)
		self.cxParams[name] = weight

	def removeCurrent(self,name):
		if name in self.currents:
			del self.currents[name]

	#@profile
	def currentValues(self):
		#ind = self.currents.keys()
		cvals = np.zeros(len(self.currents))
		counter=0
		for c in self.currents.itervalues():
			#print c.source
			val= c.source[0] * c.weight
			cvals[counter]=val
			counter+=1
		self.cvals = cvals

		#self.cvals = pd.Series(cvals,index=ind)

	def stimFeed(self,stimSource):

		self.stim[0]=stimSource

	def f_r(self,x):
		th=self.the
		k=self.ke

		return 1/(1+np.exp(-(x-th)/k))

	def f_S(self,x):
		th=self.thS
		k=self.kS
		return 1/(1+np.exp(-(x-th)/k))
#	= [c.value for c.value in self.currents]
# update the this-unit dependent gating variable for its synapses; presyn
# maybe there's a way to make this optional? so only if it makes a cxn?
	def updateS(self,dt=1):
		dS = (-self.S[0]/self.tauNMDA + (1-self.S[0]) *self.G* self.f_S(self.r[0]))*dt
		self.S[0] += dS 

	def updateA(self,dt=1):
		da = dt/self.tauA * (-self.a[0] + self.r[0])
		self.a[0] += da

	def updateR(self,dt=1):
		self.currentValues()
		
		dr = dt/self.tau * (-self.r[0] + self.f_r(sum(self.cvals)))		
		self.r[0] += dr

	# wanna do this in some sort of way that lets me record all the currents too
	@staticmethod
	def integrator(dt=1.,T=500.,stimSource=None,restart=True):
		
	 	tax=np.arange(dt,T+dt,dt)
	 	ttot=len(tax)

# here I'm going to want a data.frame # UPDATE- GOT IT!

	 	for unit in WC_net_unit._registry:
	 		unit.rTrace=np.zeros(ttot)
	 		unit.aTrace=np.zeros(ttot)
	 		unit.Strace=np.zeros(ttot)

	 		if restart:

		 		unit.r[0]=unit.r0
				unit.a[0]=unit.a0
				unit.S[0]=unit.S0
				unit.stim[0]=unit.stim0



	 		unit.tax=tax
	 		unit.currentValues()
	 		unit.currentTrace = np.zeros((ttot,len(unit.currents)))
	 		#pd.DataFrame(index=unit.tax,columns=unit.currents.keys())
	 		#unit.currentTrace.fillna(0)

	 	for t in xrange(ttot):
	 		counter=0
	 		for unit in WC_net_unit._registry:

	 			''' lets me put vectorized stim in there '''
	 			if stimSource is not None:
	 				unit.stim[0]=stimSource[counter,t]

	 			unit.rTrace[t]=unit.r[0]
	 			unit.aTrace[t]=unit.a[0]
	 			unit.Strace[t]=unit.S[0]

	 			unit.currentTrace[t,:]=unit.cvals
	 			unit.updateR(dt)
	 			unit.updateA(dt)
	 			unit.updateS(dt)
	 			counter += 1
	 	for unit in WC_net_unit._registry:
	 		df = pd.DataFrame(dict(r=unit.rTrace, a=unit.aTrace, \
	 			S=unit.Strace))

	 		df2 = pd.DataFrame(unit.currentTrace,index=unit.tax,columns=unit.currents.keys())

	 		# this concatenation apparently takes forever
	 		unit.records = pd.concat([df,df2],1)

	 		unit.records = unit.records.drop( \
	 			unit.records.tail(1).index)

	 @staticmethod
	 def plot_timecourses(netnames):

	 	nUnits = len(WC_net_unit._registry)

		fig, axes = plt.subplots(nrows=nUnits)

		for ind in xrange(nUnits):
			unit=WC_net_unit._registry[ind]

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


if __name__ == "__main__":

	foo=WC_net_unit(gSFA=.7,gee=0,r0=0.5,the=0., gStim=0.6)
	bar=WC_net_unit(gSFA=.7,gee=0, the=0., gStim=0.6)

	foo.addNewCurrent(bar.r,-1,"bar_inh_foo")

	bar.addNewCurrent(foo.r,-1,"foo_inh_bar")

	netnames=["foo","bar"]

	WC_net_unit.integrator(T=5000)

	if 1:
	#fig = plt.figure()
	#tmp = plt.gca()
	#plt.title('foo-bar')
	#tmp.axes.get_xaxis().set_ticks([]) # turn off those nasty ticks
	#tmp.axes.get_yaxis().set_ticks([])
	#plt.xlabel('time')

		nUnits = len(WC_net_unit._registry)

		fig, axes = plt.subplots(nrows=nUnits)

		for ind in xrange(nUnits):
			unit=WC_net_unit._registry[ind]

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

		#return tax,E,a,Isyn,stim




		