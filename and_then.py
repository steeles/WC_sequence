# andthen in WC
from pylab import *
from numpy import *
from matplotlib.mlab import *

def f_exc(x, k = .1, theta = .2):
	return 1/(1+exp(-(x-theta)/k)) - 1/(1+exp(theta/k))

def f_S(x,k=.1,theta=.8):
	return 1/(1+exp(-(x-theta)/k)) # - 1/(1+exp(theta/k))

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

gee = .56
G = .0641
gNMDA = .03
gExc = .02
gInp1 = .07

bPlot = 1

for i in xrange(1):
	gNMDA /=1.1
	gExc /=1.
	for t in xrange(t_tot-1):
 

 		E1[t+1] = E1[t] + \
 			(-E1[t] + f_exc(gInp1 * Inp1[t] + gee*E1[t])) * dt/tau_r
		S_NMDA_1[t+1] = S_NMDA_1[t] + \
			(-S_NMDA_1[t]/tau_NMDA + (1-S_NMDA_1[t]) *G* f_S(E1[t+1]))*dt # NMDA gating for FF input

		Isyn[t+1] = gNMDA*S_NMDA_1[t+1]
		Iext[t+1] = gExc*Inp2[t+1]

		E2[t+1] = E2[t] + \
			(-E2[t] + f_exc(Isyn[t+1] + Iext[t+1] + gee*E2[t]))*dt/tau_r 

	if bPlot:

		figure()
		title(str(gNMDA) + '; max(Isyn)=' + str(Isyn.max()))
		plot(tax,Isyn,'c')
		plot(tax,E2,'b')
		plot(tax,Iext,'g')
		plot(tax,gInp1*Inp1,'y')
		plot(tax,E1,'m')

		plot(tax,S_NMDA_1,'k')
		show(block=False)
bNull = 1 # carry out an analysis of the nullclines?
if bPlot & bNull:
	minInp = min(gInp1*Inp1)
	maxInp = max(Isyn+Iext)
	def dE(E,iapp):    return (-E + f_exc(iapp + gee*E))/tau_r
	xax=arange(0,1,.01)
	zline = zeros(len(xax))
	figure()
	plot(xax,dE(xax,maxInp),'r')
	plot(xax,dE(xax,minInp),'b')
	plot(xax,zline,'k')
	show(block=False)

dSdown = -xax/tau_NMDA
dSUp = (1-xax) * G * f_S(0)
dSUp2 = (1-xax) * G * f_S(1)
dS0 = dSdown + dSUp
dS1 = dSdown + dSUp2
figure()
plot(xax,dSdown,'r')
plot(xax,dSUp,'g')
plot(xax,dSUp2,'y')
plot(xax,dS0,'b')
plot(xax,dS1,'c')
plot(xax,zline,'k')
xlabel('S')
ylabel('dS [E1 = 0]')
show(block=False)






