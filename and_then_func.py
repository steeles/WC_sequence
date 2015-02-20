# andthen in WC
from pylab import *
from numpy import *
from matplotlib.mlab import *

def and_then(ke=.1,the=.2,kS=.1,thS=.8,
	G=.1,gee=.56,gNMDA=.02,gInp2=.03,gInp1=.07):

	def f_exc(x, k=ke, theta=the,):
		return 1/(1+exp(-(x-theta)/k)) - 1/(1+exp(theta/k))

	def f_S(x,k=kS,th=thS):
		return 1/(1+exp(-(x-th)/k)) # - 1/(1+exp(theta/k))



	t_in_ms = 500
	dt = 1
	t_tot = int(t_in_ms/dt)
	tax = linspace(dt,t_in_ms,t_tot)

	E1 = zeros(t_tot) # excitatory unit receiving the first input
	E2 = zeros(t_tot) # excitatory unit receiving second input
	Isyn = zeros(t_tot)
	Iext = zeros(t_tot)
	S_NMDA_1 = zeros(t_tot) # synaptic variable activated by unit 1

	stim_length = 30 # ms
	stim_strength = 1
	SOA = 100
	Inp1 = zeros(t_tot)
	Inp1[:stim_length/dt] = stim_strength
	Inp2 = zeros(t_tot)
	Inp2[SOA:SOA+stim_length] = stim_strength

	tau_NMDA = 100
	tau_r = 10

	pars = {'ke':ke,'the':the,'kS':kS,'thS':thS,'G':G,'gee':gee,
	'gNMDA':gNMDA,'gInp2':gInp2,'gInp1':gInp1}
	# Let's set S_NMDA_1 to its E1=0 steady state
	P = G*tau_NMDA*f_S(0)
	S_NMDA_1[0] = P/(1+P)

	for t in xrange(t_tot-1):
 

 		E1[t+1] = E1[t] + \
 			(-E1[t] + f_exc(gInp1 * Inp1[t] + gee*E1[t])) * dt/tau_r
		S_NMDA_1[t+1] = S_NMDA_1[t] + \
			(-S_NMDA_1[t]/tau_NMDA + (1-S_NMDA_1[t]) *G* f_S(E1[t+1]))*dt # NMDA gating for FF input

		Isyn[t+1] = gNMDA*S_NMDA_1[t+1]
		Iext[t+1] = gInp2*Inp2[t+1]

		E2[t+1] = E2[t] + \
			(-E2[t] + f_exc(Isyn[t+1] + Iext[t+1] + gee*E2[t]))*dt/tau_r 

	return {'E1':E1, 'E2':E2, 'Isyn':Isyn, 
		'Iext':Iext, 'S_NMDA_1':S_NMDA_1, 'tax':tax, 'pars':pars}#,
		#'f_exc':f_exc,'f_S':f_S}

if __name__=="__main__":
	and_then()

