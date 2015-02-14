# basic bare bones WC unit
# this guy wants to know its parameters and how to update its value
#from numpy import exp
#print "exp loaded"
import numpy as np


'''if i need to make changes to the default parameters,
i should do it here'''
defaultPars=dict(		
				gee = .6,				
				ke=.1,the=.2,			
				tau=10.,r=0.,Iapp=1.)
#import numpy as np
class WC_unit(object):

	""" Creates a basic WC unit. To assign pars from a dictionary, 
	use WC_unit(**parsDict) """

	_registry = []

	def __init__(self,**kwargs):
		#if !type(**kwargs)==dict:
		self.__dict__.update(defaultPars, **kwargs)
	#	else:
	#		self.__dict__.update(**kwargs)

		self._registry.append(self)

	def currents(self):
		return self.Iapp + self.gee*self.r

	def updateR(self,dt=1):
		def f(x,k=self.ke,th=self.the):
			return 1/(1+np.exp(-(x-th)/k))
		dr = dt/self.tau * (-self.r + f(self.currents()))
		
		self.r += dr


	@staticmethod
	# integrator just runs the integration for a specified T and dt, 
	# recording the trace. it also has to initialize the trace vect.
	def integrator(dt=1.,T=500.):
		
	 	tax=np.arange(dt,T,dt)
	 	ttot=len(tax)
	 	for unit in WC_unit._registry:
	 		unit.rRecord=np.zeros(ttot)
	 		unit.tax=tax

	 	for t in xrange(ttot):
	 		for unit in WC_unit._registry:
	 			unit.updateR(dt)
	 			unit.rRecord[t]=unit.r

	 	#return rRecord,tax





	