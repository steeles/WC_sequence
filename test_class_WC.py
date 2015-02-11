import numpy as np
import WC_class
reload(WC_class)

from WC_class import WC_unit

E1 = WC_unit(Iapp=100)
E1.update()
print E1.r

# if bPlot:

# 	figure()
# 	title(str(gNMDA) + '; max(Isyn)=' + str(Isyn.max()))
# 	plot(tax,Isyn,'c')
# 	plot(tax,E2,'b')
# 	plot(tax,Iext,'g')
# 	plot(tax,gInp1*Inp1,'y')
# 	plot(tax,E1,'m')

# 	plot(tax,S_NMDA_1,'k')
# 	show(block=False)
# bNull = 1 # carry out an analysis of the nullclines?
# if bPlot & bNull:
# 	minInp = min(gInp1*Inp1)
# 	maxInp = max(Isyn+Iext)
# 	def dE(E,iapp):    return (-E + f_exc(iapp + gee*E))/tau_r
# 	xax=arange(0,1,.01)
# 	zline = zeros(len(xax))
# 	figure()
# 	plot(xax,dE(xax,maxInp),'r')
# 	plot(xax,dE(xax,minInp),'b')
# 	plot(xax,zline,'k')
# 	show(block=False)

# if 0:
# 	xax=arange(0,1,.01)
# 	zline = zeros(len(xax))
# 	dSdown = -xax/tau_NMDA
# 	dSUp = (1-xax) * G * f_S(0)
# 	dSUp2 = (1-xax) * G * f_S(1)
# 	dS0 = dSdown + dSUp
# 	dS1 = dSdown + dSUp2
# 	figure()
# 	#plot(xax,dSdown,'r')
# 	#plot(xax,dSUp,'g')
# 	#plot(xax,dSUp2,'y')
# 	plot(xax,dS0,'b')
# 	plot(xax,dS1,'c')
# 	plot(xax,zline,'k')
# 	xlabel('S')
# 	ylabel('dS [E1 = 0,1]')
# 	show(block=False)

