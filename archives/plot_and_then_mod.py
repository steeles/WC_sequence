from pylab import *
from numpy import *
from matplotlib.mlab import *
import unittest

import and_then_func as atf 
import pdb



'''needs show() command of one form or another to visualize'''
def plot_FR_timecourses(tax=[],Isyn=[],E2=[],Inp2=[],E1=[],
	S_NMDA_1=[],gInp1=[],gInp2=[],f_exc=[],
	Inp1=[],**kwargs):
	

#	pdb.set_trace()
	figure()
	plot(tax,Isyn,'c')
	plot(tax,E2,'b')
	plot(tax,gInp2*Inp2,'g')
	plot(tax,gInp1*Inp1,'y')
	plot(tax,E1,'m')

	plot(tax,S_NMDA_1,'k')
	#show(block=False)

'''needs show() command of one form or another to visualize'''
def plot_dE_vs_E(gInp2=[],Inp2=[],Isyn=[],tau_r=[],f_exc=[],
		gInp1=[],Inp1=[],gee=[],**kwargs):
	Iext=gInp2 * Inp2
	#pdb.set_trace()
	minInp = min(gInp1*Inp1)
	maxInp = max(Isyn+Iext)
	def dE(E,iapp):    return (-E + f_exc(iapp + gee*E))/tau_r
	xax=arange(0,1,.01)
	zline = zeros(len(xax))
	figure()
	plot(xax,dE(xax,maxInp),'r')
	plot(xax,dE(xax,minInp),'b')
	plot(xax,zline,'k')
	#show(block=False)

'''needs show() command of one form or another to visualize'''
def plot_dS_vs_E(tau_NMDA=[],G=[],f_S=[],**kwargs):
	xax=arange(0,1,.01)
	zline = zeros(len(xax))
	dSdown = -xax/tau_NMDA
	dSUp = (1-xax) * G * f_S(0)
	dSUp2 = (1-xax) * G * f_S(1)
	dS0 = dSdown + dSUp
	dS1 = dSdown + dSUp2
	figure()
	#plot(xax,dSdown,'r')
	#plot(xax,dSUp,'g')
	#plot(xax,dSUp2,'y')
	plot(xax,dS0,'b')
	plot(xax,dS1,'c')
	plot(xax,zline,'k')
	xlabel('S')
	ylabel('dS [E1 = 0,1]')
	#show(block=False)

class PlotAndThenTests(unittest.TestCase):
	def test_timecoursePlots(self):
		pass
	def test_dE_Plots(self):
		pass
	def test_dS_Plots(self):
		pass

if __name__=="__main__":
	unittest.main()


