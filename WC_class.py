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
class WC_unit:

	_registry = []

	def __init__(self,**kwargs):
		self.__dict__.update(defaultPars, **kwargs)
		self._registry.append(self)

	def computeX(self):
		return self.Iapp + self.gee*self.r

	def updateR(self,dt=1):
		def f(x,k=self.ke,th=self.the):
			return 1/(1+np.exp(-(x-th)/k))
		dr = dt/self.tau * (-self.r + f(self.computeX()))
		
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

import unittest

class WC_assign_tests(unittest.TestCase):
	def testWC_defaultPars1(self):  # I want to make sure WC default pars get assigned
		
		tUnit=WC_unit()
		assignedPars=tUnit.__dict__
		
		self.failUnless(assignedPars==defaultPars)

	def testWC_userPars(self):  # but that the user can change them
		tUnit=WC_unit(Iapp=0,the=.5)
		assignedPars=tUnit.__dict__
		
		self.failIf(assignedPars==defaultPars)

	def testWC_defaultpars2(self):	# and that the defaults don't get screwed up when user does that
		tUnit=WC_unit(Iapp=0,the=.5)
		tUnit2=WC_unit()
		assignedPars=tUnit2.__dict__
		self.failUnless(assignedPars==defaultPars)

def main():
	unittest.main()

if __name__=="__main__":
	main()





	