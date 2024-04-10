import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm

# Importing textured data
# np.loadtxt(name,delimiter='\t',skiprows=161)
def import_textured(name):
    t_data = np.loadtxt(name,delimiter='\t')
    return t_data**4
# ctrl_t_data = import_textured("Data/t-E.txt")
total_t_data = import_textured("Data/Au_t-E-opt.txt")
# np_t_data = total_t_data - ctrl_t_data

# Importing solid data
def import_solid(dir,layers):
    s_data = np.zeros((76,76))
    for layer in range(layers):
        data_txt = dir+f"{layer}.txt"
        data_array = np.loadtxt(data_txt,delimiter='\t')
        for i,row in enumerate(data_array):
            for j,E in enumerate(row):
                if E > s_data[i,j]:
                    s_data[i,j] = E
    return s_data**4
# ctrl_s_data = import_solid("Data/s-E/",78)
total_s_data = import_solid("Data/Au_s-E-opt/",78)
# np_s_data = np.zeros((76,76))
# for layer in range(len(ctrl_s_data)):
#     ctrl_s_array = np.loadtxt(f"Data/s-E/{layer}.txt",delimiter='\t')
#     total_s_array = np.loadtxt(f"Data/Au_s-E/{layer}.txt",delimiter='\t')
#     np_s_array = total_s_array - ctrl_s_array
#     for i,row in enumerate(np_s_array):
#         for j,E in enumerate(row):
#             if E > np_s_data[i,j]:
#                 np_s_data[i,j] = E
# np_s_data = np_s_data**4

# Plotting bins
def binning(data_bin,data,E_max,bin_vals):
    for row in data:
        for E in row:
            for bin, bin_val in enumerate(bin_vals):
                if E <= bin_val:
                    data_bin[bin]+=1
                    break
                elif E >= E_max:
                    data_bin[-1]+=1
                    break
    return data_bin
def bin_plot(name,t_data,s_data,E_max,num_bins):
    db = E_max/num_bins
    bin_vals = np.round(np.arange(0, E_max+db, db),2)
    t_bins = [0]*len(bin_vals)
    s_bins = [0]*len(bin_vals)
    t_bins = binning(t_bins,t_data,E_max,bin_vals)
    s_bins = binning(s_bins,s_data,E_max,bin_vals)
    fig,ax=plt.subplots()
    width = 0.9
    x = range(len(bin_vals))
    ax.bar(x,t_bins,width=width)
    ax.bar(x,s_bins,width=width*0.8,alpha=0.6)
    plt.legend(["Textured","Solid"])
    # plt.xlim(right=E_max+0.3)
    ax.set_xlabel(u"|E|\u2074")
    ax.set_ylabel("Count")
    ax.set_xticks([i + width/2 for i in x])
    tick_labels = [str(round(val)) for val in bin_vals]
    tick_labels[-1] = "$\geq$" + tick_labels[-1]
    ax.set_xticklabels(tick_labels, rotation=45)
    plt.tight_layout()
    plt.savefig(f"Analysis/{name}-hist-opt.png")
# bin_plot("ctrl",ctrl_t_data,ctrl_s_data,25,25)
# bin_plot("np",np_t_data,np_s_data,25,25)
bin_plot("total",total_t_data,total_s_data,5000,25)

# Plotting enhancement  
def enhance_plot(name,data,E_max,gam):
    fig,ax=plt.subplots()
    plot = ax.imshow(data,cmap='rainbow',norm=PowerNorm(gamma=gam,vmin=0,vmax=E_max))
    cbar = plt.colorbar(plot)
    ax.set_xticks([0,76/4,76/2,(76/2+75.5)/2,75.5])
    ax.set_yticks([0,74/4,74/2,(74/2+73.5)/2,73.5])
    ax.set_xticklabels([-300,-150,0,150,300])
    ax.set_yticklabels([300,150,0,-150,-300])
    ax.set_xlabel("x(nm)")
    ax.set_ylabel("y(nm)")
    cbar.set_label(u"|E|\u2074")
    cbar_ticks = list(cbar.get_ticks())
    cbar_ticks[-1] = E_max
    cbar.set_ticks(cbar_ticks)
    cbar_labels = [f'{round(tick)}' for tick in cbar_ticks[:-1]]
    cbar_labels.append(f"$\geq{round(E_max,3)}$")
    cbar.set_ticklabels(cbar_labels)
    print(f"{name[9:-4]}: avg = {np.average(data)},  max = {np.max(data)}")
    plt.savefig(name)
# enhance_plot("Analysis/ctrl-t-E.png",ctrl_t_data,2.5)
# enhance_plot("Analysis/ctrl-s-E.png",ctrl_s_data,10)
# enhance_plot("Analysis/np-t-E.png",np_t_data,0.025)
# enhance_plot("Analysis/np-s-E.png",np_s_data,0.025)
enhance_plot("Analysis/total-t-E-opt.png",total_t_data,250,0.25)
enhance_plot("Analysis/total-s-E-opt.png",total_s_data,1e3,1)

# Plotting bin's enhancements
def bin_enhance_plot(dir,data,E_max,bins):
    fig,ax=plt.subplots()
    plt.axis('off')
    db = E_max/3.0
    # bins = np.arange(0,E_max+db,db)
    print(f"{dir[9:-1]}:")
    for i in range(len(bins)-1):
        bin = np.copy(data)
        low = bins[i]
        high = bins[i+1]
        bin[bin < low] = 0
        bin[bin > high] = 0
        ax.imshow(bin,cmap='hot',vmin=low,vmax=high)
        print(low,high)
        plt.savefig(dir + f"{i}.png")
    bin = np.copy(data)
    bin[bin < high] = 0
    ax.imshow(bin,cmap='hot')
    print(high)
    plt.savefig(dir + f"{i+1}.png")
# bin_enhance_plot("Analysis/ctrl-t-bin/",ctrl_t_data,2.5)
# bin_enhance_plot("Analysis/ctrl-s-bin/",ctrl_s_data,10)
# bin_enhance_plot("Analysis/np-t-bin/",np_t_data,0.025)
# bin_enhance_plot("Analysis/np-s-bin/",np_s_data,0.025)
bins = [0,50,150,250]
bin_enhance_plot("Analysis/total-t-bin-opt/",total_t_data,250,bins)
bins = [0,5e3,15e3,25e3]
bin_enhance_plot("Analysis/total-s-bin-opt/",total_s_data,25000,bins)