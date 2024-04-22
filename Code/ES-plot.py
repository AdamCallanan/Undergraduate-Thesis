import matplotlib.pyplot as plt
import numpy as np

def solid_ES(dir,n):
    s_ES = np.zeros((n,2))
    for layer in range(5):
        data = np.loadtxt(dir+f"{layer}.txt")
        s_ES += data[:n,:]
    return s_ES/5

t_ES = np.loadtxt("Data/Au_t-ES_1.txt")[:101,:]
s_ES = solid_ES("Data/Au_s-ES_1/",101)

optimal_lam = lambda x,y: print(f"{y}: {round(x[np.argmin(x[:,1]),0])}")
optimal_lam(t_ES,'t')
optimal_lam(s_ES,'s')

fig,ax = plt.subplots()
ax.plot(t_ES[:,0],t_ES[:,1],label=u"Au@t-SiO\u2082")
ax.plot(s_ES[:,0],s_ES[:,1],label=u"Au@s-SiO\u2082")
ax.set_xlabel("Wavelength (nm)")
ax.set_ylabel("Power Transmission")
plt.legend()
plt.savefig("Analysis/ES-1.png")
