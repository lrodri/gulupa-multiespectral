import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('estadisticas5.csv')
sns.set(style="ticks")
print (data.describe())
sns.pairplot(data,hue="AUSENCIA DE N")
plt.savefig('estadisticas5.pdf', dpi=400, bbox_inches='tight', pad_inches=0.1)
