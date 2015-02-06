# stim_maker_ML - for Morris Lecar sequence detector. 1/22/2014

from pylab import *
from numpy import *
from matplotlib.mlab import *
import pdb

#global stim_maker_WC

#T = 5
#dt = .001
#nUnits = 3
#ITI = .5
#df = 7
#bPlot = 1

def rpt_stim_maker(T,dt,nUnits,ITI,df,bPlot=False):

	tone_length = .030
	#exc_gain = 300
	tax = arange(0,T,dt) # s 
	stim_length = len(tax)
	fq_axis = 440 * (2.**(1/12.))**arange(-12,13)
	tuning_curve = normpdf(linspace(-7,7,len(fq_axis)),0,3)
	tuning_curve/= max(tuning_curve) # rescale to equal 1
	tone_length = tone_length/dt
	#df = 5
	TRT = ITI/dt
	stim = zeros((nUnits,stim_length))


	A_ind = 12; B_ind = A_ind - df
	#pdb.set_trace()
	stim[0,:tone_length] = tuning_curve[A_ind]
	stim[1,TRT:TRT+tone_length] = tuning_curve[B_ind]
	stim[2,2*TRT:2*TRT+tone_length] = tuning_curve[A_ind]

	period = 4 * TRT
	ncycles = ceil(stim_length/period)
	triplet = stim[:,:period]
	tmp = tile(triplet,[1,ncycles])
	stim = tmp[:,:stim_length]

	if bPlot:
			fig = figure()
			foo = gca()
			title('ITI = ' + str(ITI*1000) + ' ms, df = ' + str(df))
			foo.axes.get_xaxis().set_ticks([]) # turn off those nasty ticks
			foo.axes.get_yaxis().set_ticks([])
			xlabel('time')


			for ind in xrange(nUnits):
				ax=fig.add_subplot(nUnits,1,ind+1)
				ylabel('u' + str(ind+1))
				ylim(-.2,1)
			#	ax.plot(tax,E[ind,:],'b'); 
			#	ax.plot(tax,a[ind,:],'r');
				ax.plot(tax,stim[ind,:],'g')
			#	ax.plot(tax,Isyn[ind,:],'c')
				#title(str(ind+1)) 
			# plot(tax,E,'b')
			# plot(tax,I,'r')
			# plot(tax,Inp_e,'g')
			show(block=False)

	# trip_activation = zeros(ITI*4)
	# trip_activation[:tone_length] = tuning_curve[A_ind]
	# trip_activation[ITI:ITI+tone_length] = tuning_curve[B_ind]
	# trip_activation[2*ITI:2*ITI+tone_length] = tuning_curve[A_ind]

	return stim