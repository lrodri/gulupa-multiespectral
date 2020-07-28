import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import numpy as np
import scipy as sp
import seaborn as sns


#%matplotlib inline
#3
data = pd.read_csv('ausenciacm.csv')
#print 'tabla', data
#4
print (list(data))
#5
#data = data.loc[:, ['Position', 'Gross pay', 'Phi-h', 'Pressure', 'Random 1', 'Random 2', 'Gross pay transform', 'Production']]
print (data.describe())
#6
print (data.isnull().values.any())
import warnings
warnings.filterwarnings("ignore")
#
def corrfunc(x, y, **kws):
    r, _ = sp.stats.spearmanr(x, y)
    ax = plt.gca()
    ax.annotate("CC = {:.2f}".format(r), xy=(.1, .9),           xycoords=ax.transAxes, color = 'g', fontsize = 15)
####
plt.rcParams["axes.labelsize"] = 11
g = sns.PairGrid(data, diag_sharey=False)
axes = g.axes

g.map_upper(plt.scatter,  linewidths=1, edgecolor="w", s=90, alpha = 0.5)
#g.map_upper(corrfunc)

g.map_diag(sns.kdeplot, lw = 4, legend=False)
g.map_lower(sns.kdeplot, cmap="Blues_d")

#plt.savefig('estadisticas.pdf', dpi=400, bbox_inches='tight', pad_inches=0.1)
plt.show()
