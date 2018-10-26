from pylab import plt
import pandas as pd
import seaborn as sns; sns.set()


ax = []
ax2=[]
data = pd.DataFrame(trace_dict, index=sim.tax) \
    [['tax', 'u1_r', 'u1_a', 'stim']]
df = data[['tax', 'u1_r', 'u1_a']].melt(
    'tax', var_name='trace', value_name='values'
)

lines = []
ax = sns.lineplot(x='tax', y='values',
                  hue='trace', data=df,
                  legend=False)
ylim = list(ax.get_ylim())
ylim[1] *= 1.25
ylim[0] -= .5
ax.set_ylim(ylim)
ax.lines[0].set_label('u1_r')
ax.lines[1].set_label('u1_a')
lines += ax.lines
print(lines)

ax2 = plt.twinx()
ax2.set_ylim([-1.3, 0])
ax2.set_yticks([])
ax2.set_ylabel("")
data_n = data[['tax', 'stim']]
data_n['stim'] = data_n['stim'].apply(lambda x: x * -.1)
sns.lineplot(x='tax', y='stim',
             data=data_n, ax=ax2, color='grey',
             legend=False)
ax2.lines[0].set_label('stim')
lines += ax2.lines
labs = [l.get_label() for l in lines]
ax.legend(lines, labs, loc='best', bbox_to_anchor=(.5, .5, .45, .45))