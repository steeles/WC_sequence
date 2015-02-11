# basic bare bones WC unit
# this guy wants to know its parameters and how to update its value
#from numpy import exp
#print "exp loaded"
#import numpy as np

class WC_unit:

	nUnits = 0
	def __init__(self,**kwargs):
		self.__dict__.update(dict(
				ke=.1,the=.2,
				gee = .6,
				tau=100.,dt=.1,r=0.,Iapp=1.), **kwargs)
		WC_unit.nUnits +=1

	def update(self,t=0):
		def f(x,k=self.ke,th=self.the):
			return 1/(1+np.exp(-(x-th)/k))
		x = self.Iapp + self.gee * self.r
		self.dr = self.dt/self.tau * (-self.r + f(x))
		self.r += self.dr

	def update(self,t=0):		
		self.r += self.calc_dr(t)
	


	@staticmethod
	def integrator(func,dt,T):
	 	tax=np.arange(dt,T,dt)