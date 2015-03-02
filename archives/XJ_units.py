# 1/30/15 - playing with synapses from XJ's CCNSS assignment
# also look to Wong & Wang (2006) appendix

from pylab import *
from numpy import *
from matplotlib.mlab import *

bPlot = True

def f(I, a=270, b=108, d=.154):
	return (a*I-b)/(1-exp(-d*(a*I-b))) 

t_in_ms = 2000
dt = 1
t_tot = int(t_in_ms/dt)
tax = linspace(dt,t_in_ms,t_tot)

u0 = 30

s1 = zeros(t_tot)
s2 = zeros(t_tot)
x1 = zeros(t_tot)
x2 = zeros(t_tot)

gE,gI,gExt = .2609, .0497, .00052
c = zeros(t_tot)

#s1[0] = .1

tau_s = 100
gamma = .641 
I_0=.3255

# E pop:
for t in xrange(t_tot-1):
	x1[t+1] = gE * s1[t] - gI * s2[t] + I_0 + (gExt * u0 *(1+c[t]/100))
	x2[t+1] = gE * s2[t] - gI * s1[t] + I_0 + (gExt * u0 *(1-c[t]/100))

	s1[t+1] = s1[t] + (-s1[t]/tau_s + (1-s1[t]) * gamma * f(x1[t+1])/1000) * dt
	s2[t+1] = s2[t] + (-s2[t]/tau_s + (1-s2[t]) * gamma * f(x2[t+1])/1000) * dt

nUnits = 2
if bPlot:
	fig = figure()
	foo = gca()
	#title('ITI = ' + str(ITI*1000) + ' ms, df = ' + str(df))
	foo.axes.get_xaxis().set_ticks([]) # turn off those nasty ticks
	foo.axes.get_yaxis().set_ticks([])
	xlabel('time')


	#for ind in xrange(nUnits):
	ax=fig.add_subplot(nUnits,1,1)
	ylabel('u1')
		#ylim(-.2,1)
	ax.plot(tax,s1,'b') 
	ax.plot(tax,x1,'c')

	ax=fig.add_subplot(nUnits,1,2)
	ylabel('u2')
	ax.plot(tax,s2,'b')
	ax.plot(tax,x2,'c')

		#ax.plot(tax,I[ind,:],'r');
		#ax.plot(tax,r[ind,:]*1000,'g')

		#title(str(ind+1)) 
	# plot(tax,E,'b')
	# plot(tax,I,'r')
	# plot(tax,Inp_e,'g')
	show(block=False)

	figure()
	plot(tax,f(s1),'r')
	plot(tax,f(s2),'b')
	show(block=False)

	#return tax,E,a,Isyn,stim
