# basic bare bones WC unit
# this guy wants to know its parameters and how to update its value

class WC_unit:
	nUnits = 0
	def __init__(self,**kwargs):
		self.__dict__.update(dict(
				ke=.1,the=.2,
				tau=100,dt=1,r=0,Iapp=0), **kwargs)
		nUnits +=1

	def f(self,x):
		return 1/(1+exp(-x-self.the)/self.ke)
	def update(self):
		self.r += self.dt/self.tau * (-self.r + f(x))
	def computeX(self):
		return 




		