# 1/21/15 - making an array of WC units
# array info coming from 3_cell_stim_func
# let's use stim_maker.py; we can update
# 

from pylab import *
from numpy import *
from matplotlib.mlab import *

execfile('stim_maker_WC.py')
def WC_pop_func(df = 3, ITI = .07, bPlot = False):
	
	def f(x, k = .1, theta = .2):
		return 1/(1+exp(-(x-theta)/k)) - 1/(1+exp(theta/k))

	timescale, dt, T_in_seconds = .01, .1, 2.5
	timesteps = T_in_seconds / timescale
	t_tot = int(timesteps/dt)

	tax = linspace(dt*timescale,T_in_seconds,t_tot)

	nUnits = 3
	#df, ITI = 5, .05

	stimscale = 0.1
	stim = stim_maker_WC(T_in_seconds,dt*timescale,nUnits,ITI,df) * stimscale

	E = zeros((nUnits,t_tot))
	I = zeros((nUnits,t_tot))
	Isyn = zeros((nUnits,t_tot))

	weights = array([[0,0,0],[1,0,0],[-2,1,0]]) * .08

	# we are in a timescale of .01 sec
	tau_E = 1
	tau_I = 50

	ee = .7#.5
	ei = .7#4
	ie = .9#50#.11
	ii = 0#0.5#.1

	threshs = array([0.2,0.3,0.3])

	# E pop:
	for t in xrange(t_tot-1):
		Isyn[:,t+1] = dot(weights,(E[:,t]>0)*E[:,t])
		E[:,t+1] =E[:,t] + dt/tau_E * (-E[:,t] + 
			f(ee * E[:,t] - ei * I[:,t] + stim[:,t] + Isyn[:,t], 
				theta = threshs))
		I[:,t+1] =I[:,t] + dt/tau_I * (-I[:,t] + f(ie * E[:,t] - ii * I[:,t]))

	if bPlot:
		fig = figure()
		foo = gca()
		title('ITI = ' + str(ITI) + ', df = ' + str(df))
		foo.axes.get_xaxis().set_ticks([]) # turn off those nasty ticks
		foo.axes.get_yaxis().set_ticks([])
		xlabel('time')


		for ind in xrange(nUnits):
			ax=fig.add_subplot(nUnits,1,ind+1)
			ylabel('u' + str(ind+1))
			ylim(-.2,1)
			ax.plot(tax,E[ind,:],'b'); 
			ax.plot(tax,I[ind,:],'r');
			ax.plot(tax,stim[ind,:],'g')
			ax.plot(tax,Isyn[ind,:],'c')
			#title(str(ind+1)) 
		# plot(tax,E,'b')
		# plot(tax,I,'r')
		# plot(tax,Inp_e,'g')
		show(block=False)

	return tax,E,I,Isyn,stim
