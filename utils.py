import numpy as np
import matplotlib.pylab as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

cp = {'S':'#BF9937', 'I':'#7D2E2B', 'R':'#336259'} # SIR colormap

def set_plot_style(ax, title=None, xlabel=None, ylabel=None, xscale='linear', yscale='linear', xlims=None, ylims=None, xticks=None, yticks=None, xticklabels=None, yticklabels=None, legend=True, legend_args={}, xticklabels_args={}, yticklabels_args={}):
    ax.set_title(title, fontweight='semibold')
    ax.set_xlabel(xlabel, fontweight='semibold', color='#454545')
    ax.set_ylabel(ylabel, fontweight='semibold', color='#454545')
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    if legend: ax.legend(frameon = False,**legend_args)
    if not xlims is None: ax.set_xlim(xlims)
    if not ylims is None: ax.set_ylim(ylims)
    if not xticks is None: ax.set_xticks(xticks)
    if not yticks is None: ax.set_xticks(yticks)
    if not xticklabels is None: ax.set_xticklabels(xticklabels, **xticklabels_args)
    if not yticklabels is None: ax.set_xticklabels(yticklabels, **yticklabels_args)

    for spine in ('top', 'right'): 
        ax.spines[spine].set_visible(False)

#### Lotka-volterra plots
def LV_field(ax, LV_cc, r1, r2, K1, K2, a21, a12, nb_points=20, cmap='gist_gray', alpha=0.5):
    # plot isocline
    ax.plot([0,K2/a21], [K2,0], color='purple', ls="-", alpha=alpha)
    ax.plot([0,K1], [K1/a12,0], color='g', ls="-", alpha=alpha)

    # define a grid and compute direction at each point
    ymax = ax.set_ylim(ymin=0)[1]                        # get axis limits
    xmax = ax.set_xlim(xmin=0)[1]

    # reset axix lims
    ax.set_xlim((-0.2,K1*11/10))
    ax.set_ylim((-0.2,K2*11/10))
    
    x = np.linspace(0, xmax, nb_points)
    y = np.linspace(0, ymax, nb_points)

    X1 , Y1  = np.meshgrid(x, y)                           # create a grid
    DX1, DY1 = LV_cc(0,[X1, Y1], r1, r2, K1, K2, a21, a12) # compute growth rate on the gridt
    M = (np.hypot(DX1, DY1))                               # Norm of the growth rate 
    M[ M == 0] = 1.                                        # Avoid zero division errors 
    DX1 /= M                                               # Normalize each arrows
    DY1 /= M

    #-------------------------------------------------------
    # Drow direction fields, using matplotlib 's quiver function
    # I choose to plot normalized arrows and to use colors to give information on the growth speed
    Q = ax.quiver(X1, Y1, DX1, DY1, M, pivot='mid', cmap=cmap, alpha=alpha)


### Lattice ABM plot
opinion_colors = ['#304B58','#5B958D','#F3E08D','#ECAD74','#C16E54','#842D2D']
def plot_lattice(ax, model_status, opinions, kwargs={'legend':False}):
    cABM = {opinion:opinion_colors[i] for i,opinion in enumerate(opinions)} # ABM colormap
    """Plot the grid of agents. Each opinion will have a different color."""
    if np.min(model_status) == 0: cmap = ListedColormap(['#EEEEEE']+list(cABM.values())[:np.unique(model_status).shape[0]-1])
    else:                      cmap = ListedColormap(list(cABM.values())[:np.unique(model_status).shape[0]-1])
    ax.imshow(model_status, cmap=cmap, interpolation='nearest')
    # Create a legend
    legend_labels = [Patch(facecolor=cABM[opinion], edgecolor='k', label=opinion) for opinion in opinions]
    
    set_plot_style(ax, legend=False, **{k:v for k,v in kwargs.items() if k !='legend'})
    ax.legend(handles=legend_labels, bbox_to_anchor=(0., 1), loc='upper left', borderaxespad=0., framealpha=1)   


