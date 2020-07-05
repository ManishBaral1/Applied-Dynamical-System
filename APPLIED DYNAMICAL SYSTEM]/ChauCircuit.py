import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def fV_1(V_1, G_a, G_b, V_b):
    if V_1 < -V_b:
        fV_1 = G_b*V_1+(G_b-G_a)*V_b
    elif -V_b <= V_1 and V_1 <=V_b:
        fV_1 = G_a*V_1
    elif V_1 > V_b:
        fV_1 = G_b*V_1+(G_a-G_b)*V_b
    else:
        print "Error!"
    return fV_1

def ChuaDerivatives(state,t):
    #unpack the state vector
    V_1 = state[0]
    V_2 = state[1]
    I_3 = state[2]

    #definition of constant parameters
    L = 0.018 #H, or 18 mH
    C_1 = 0.00000001 #F, or 10 nF
    C_2 = 0.0000001 #F, or 100 nF
    G_a = -0.000757576 #S, or -757.576 uS
    G_b = -0.000409091 #S, or -409.091 uS
    V_b = 1 #V (E)
    G = 0.000550 #S, or 550 uS VARIABLE

    #compute state derivatives
    dV_1dt = (G/C_1)*(V_2-V_1)-(1/C_1)*fV_1(V_1, G_a, G_b, V_b)
    dV_2dt = -(G/C_2)*(V_2-V_1)+(1/C_2)*I_3
    dI_3dt = -(1/L)*V_2

    #return state derivatives
    return dV_1dt, dV_2dt, dI_3dt

#set up time series
state0 = [0.1, 0.1, 0.0001]
t = np.arange(0.0, 53.0, 0.1)

#populate state information
state = odeint(ChuaDerivatives, state0, t)

# do some fancy 3D plotting
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(state[:,0],state[:,1],state[:,2])
ax.set_xlabel('V_1')
ax.set_ylabel('V_2')
ax.set_zlabel('I_3')
plt.show()
