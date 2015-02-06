from pylab import *
from numpy import *
from matplotlib.mlab import *


tau_E = 1
tau_I = 50

def f(I, k = .1, theta = .2):
	return 1/(1+exp(-(I-theta)/k))


timescale, dt, T_in_seconds = .01, .1, 5
timesteps = T_in_seconds / timescale
t_tot = int(timesteps/dt)

tax = linspace(dt*timescale,T_in_seconds,t_tot)

#Inp_e = linspace(0,1,t_tot)
Inp_e = zeros(t_tot)
Inp_i = zeros(t_tot)+.1 # so we can see
Inp_e[arange(100)]=1.0
 # brief input

E = zeros(t_tot)
I = zeros(t_tot)
ee = .7#.5
ei = .7#4
ie = .9#50#.11
ii = 0#0.5#.1

E_line = linspace(-1,1.5,100)
I_line = E_line
# E pop:
for t in xrange(t_tot-1):
	E[t+1] =E[t] + dt/tau_E * (-E[t] + f(ee * E[t] - ei * I[t] + Inp_e[t]))
	I[t+1] =I[t] + dt/tau_I * (-I[t] + f(ie * E[t] - ii * I[t] + Inp_i[t]))

#I(t+1) =I(t) + 1/tau_I * (-I + f_i(ie * I - ii * I + I_i))
plot(tax,E,'b')
plot(tax,I,'c')
plot(tax,Inp_e,'r')
plot(tax,Inp_i,'m')
show(block=False)


# E_dot_zero = f(ee * E_line - ei * I_line + Inp_e[-1]) # nullcline of E for final input val
# I_dot_zero = f(ie * E_line - ii * I_line + Inp_e[-1])

# #plot nullclines
# figure()
# plot(I_line,E_dot_zero,'b')
# plot(I_dot_zero, E_line,'c')
# show(block=False)