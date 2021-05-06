import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
from matplotlib.widgets import Slider, Button

poll_data = pd.read_csv('generic_polllist.csv')
poll_data['modeldate'] = pd.to_datetime(poll_data['modeldate'])
poll_data['startdate'] = pd.to_datetime(poll_data['startdate'])
poll_data['enddate'] = pd.to_datetime(poll_data['enddate'])
poll_data['adj_advantage'] = poll_data['adjusted_dem'] - poll_data['adjusted_rep']
poll_data['advantage'] = poll_data['dem'] - poll_data['rep']
poll_data['undecided'] = 100 - poll_data['dem'] - poll_data['rep']

n = 0

counts = [10, 12, 13, 15, 20, 30]
r = [5, 7, 9, 11, 13, 15]
locations = []
for i in range(6):
  for j in range(counts[i]):
    x = (r[i]*np.cos(np.pi/(counts[i]-1)*j))
    y = (r[i]*np.sin(np.pi/(counts[i]-1)*j))
    theta = np.arctan(x/y)
    locations.append([x, y, theta])
data = pd.DataFrame(locations, columns=['x', 'y', 'theta'])

data = data.sort_values('theta')

for i in range(len(poll_data['dem'])):
  data[poll_data['poll_id'][i]] = ['Dem.']*(int)(poll_data['dem'][i]) + ['Other']*(100 - (int)(poll_data['dem'][i]) - (int)(poll_data['rep'][i])) + ['Rep.']*(int)(poll_data['rep'][i])
data['actual'] = ['Dem.']*50 + ['Rep.']*50

poll_visibility = 1
dot_size = 100
line_width = 5
legend_font_size = 14
tick_font_size = 15
title_font_size = 25
description_font_size = 20

h = 10

fig, axs = plt.subplots(3, 2, figsize = (2*(h-0.5), h), gridspec_kw={'height_ratios': [(h-.5)/2,(h-.5)/2, .5]})
ax1 = axs[0, 0]
ax2 = axs[0, 1]
gs3 = axs[1, 0].get_gridspec()
gs4 = axs[2, 0].get_gridspec()
axs[1, 0].remove()
axs[2, 0].remove()
axs[1, 1].remove()
axs[2, 1].remove()
ax3 = fig.add_subplot(gs3[1,:])
ax4 = fig.add_subplot(gs4[2,:])
plt.rcParams['font.family'] = "meiryo"

ax1.axis('off')
reals = ['Dem.', 'Rep.']
labels = ['Dem.', 'Rep.', 'Other']
colors = ['b', 'r', 'lightgrey']
for i in range(2):
  subset = data[data['actual'] == reals[i]]
  ax1.scatter(subset['x'], subset['y'], s = 400, c = 'w', ec = colors[i], label = 'Elected ' + reals[i])
for i in range(3):
  subset = data[data[poll_data['poll_id'][n]] == labels[i]]
  ax1.scatter(subset['x'], subset['y'], s = 300, c = colors[i], label = 'Polled ' + labels[i])
ax1.legend(bbox_to_anchor = [1, .75], fontsize = legend_font_size, frameon=False, handletextpad = 0.2)


ax2.axis('off')
title = 'How did pollsters see the race for Congress?'
ax2.text(-0.5, 1.2, title, transform=ax2.transAxes, fontsize=title_font_size,
        verticalalignment='top')
description = '\n'.join((
    r'Polling Period: %s - %s' % (poll_data['startdate'][n].date().strftime("%d %B, %Y"), poll_data['enddate'][n].date().strftime("%d %B, %Y")),
    r'Sample Size: %i' % (poll_data['samplesize'][n]),
    r'Dem. Support: %.2i%%    Adj. Dem. Support: %.2f%%' % (poll_data['dem'][n], poll_data['adjusted_dem'][n]),
    r'Rep. Support:  %.2i%%    Adj. Rep. Support: %.2f%%' % (poll_data['rep'][n], poll_data['adjusted_rep'][n]),
    r'Polling Source: %s' % (poll_data['pollster'][n])))
ax2.text(0.15, 0.8, description, transform=ax2.transAxes, fontsize=description_font_size,
        verticalalignment='top', linespacing = 1.5)
navigate = 'To explore the dataset, adjust the slider below the scatterplot.'
ax2.text(-0.1, 0.1, navigate, transform=ax2.transAxes, fontsize=description_font_size,
        verticalalignment='top')


ax3.spines['right'].set_visible(False)
ax3.spines['top'].set_visible(False)

ax3.scatter(poll_data['enddate'], poll_data['adjusted_dem'], c = 'b', s = dot_size, alpha = poll_visibility, label = 'Dem. Poll Res.', zorder=4 )
ax3.scatter(poll_data['enddate'], poll_data['adjusted_rep'], c = 'r', s = dot_size, alpha = poll_visibility, label = 'Rep. Poll Res.', zorder=3 )

period = ax3.fill_betweenx([30, 60], poll_data['startdate'][n], poll_data['enddate'][n], color = 'lightgrey', label = 'Poll Period', zorder =0)
ax3.grid(zorder = 1)
plt.ylim(30, 60)
fmt = '%.0f%%'
yticks = mtick.FormatStrFormatter(fmt)
ax3.yaxis.set_major_formatter(yticks)
plt.xticks(fontsize = tick_font_size)
plt.yticks(fontsize = tick_font_size)
fmtx = mdates.DateFormatter('%B %Y')
ax3.xaxis.set_major_formatter(fmtx)

ax3.legend(bbox_to_anchor=(1, .35), fontsize = legend_font_size, frameon = False)

def update(n):
  ax1.clear()
  ax1.axis('off')
  for i in range(2):
      subset = data[data['actual'] == reals[i]]
      ax1.scatter(subset['x'], subset['y'], s = 400, c = 'w', ec = colors[i], label = 'Elected ' + reals[i])
  for i in range(3):
      subset = data[data[poll_data['poll_id'][n]] == labels[i]]
      ax1.scatter(subset['x'], subset['y'], s = 300, c = colors[i], label = 'Polled ' + labels[i])
  ax1.legend(bbox_to_anchor = [1, .75], fontsize = legend_font_size, frameon=False, handletextpad = 0.2)

  ax2.clear()
  ax2.axis('off')
  ax2.text(-0.5, 1.2, title, transform=ax2.transAxes, fontsize=title_font_size,
          verticalalignment='top')
  description = '\n'.join((
      r'Polling Period: %s - %s' % (poll_data['startdate'][n].date().strftime("%d %B, %Y"), poll_data['enddate'][n].date().strftime("%d %B, %Y")),
      r'Sample Size: %i' % (poll_data['samplesize'][n]),
      r'Dem. Support: %.2i%%    Adj. Dem. Support: %.2f%%' % (poll_data['dem'][n], poll_data['adjusted_dem'][n]),
      r'Rep. Support:  %.2i%%    Adj. Rep. Support: %.2f%%' % (poll_data['rep'][n], poll_data['adjusted_rep'][n]),
      r'Polling Source: %s' % (poll_data['pollster'][n])))
  ax2.text(0.15, 0.8, description, transform=ax2.transAxes, fontsize=description_font_size,
          verticalalignment='top', linespacing = 1.5)
  navigate = 'To explore the dataset, adjust the slider below the scatterplot.'
  ax2.text(-0.1, 0.1, navigate, transform=ax2.transAxes, fontsize=description_font_size,
          verticalalignment='top')

  ax3.clear()
  ax3.spines['right'].set_visible(False)
  ax3.spines['top'].set_visible(False)

  ax3.scatter(poll_data['enddate'], poll_data['adjusted_dem'], c = 'b', s = dot_size, alpha = poll_visibility, label = 'Dem. Poll Res.' )
  ax3.scatter(poll_data['enddate'], poll_data['adjusted_rep'], c = 'r', s = dot_size, alpha = poll_visibility, label = 'Rep. Poll Res.' )

  period = ax3.fill_betweenx([30, 60], poll_data['startdate'][n], poll_data['enddate'][n], color = 'lightgrey', label = 'Poll Period', zorder = 0)

  plt.ylim(30, 60)
  fmt = '%.0f%%'
  yticks = mtick.FormatStrFormatter(fmt)
  ax3.yaxis.set_major_formatter(yticks)
  plt.xticks(fontsize = tick_font_size)
  plt.yticks(fontsize = tick_font_size)
  fmtx = mdates.DateFormatter('%B %Y')
  ax3.xaxis.set_major_formatter(fmtx)

  ax3.legend(bbox_to_anchor=[1, .75], fontsize = legend_font_size, frameon = False)


slider = Slider(
    label = '',
    ax=ax4,
    valstep=1,
    valmin=0,
    valmax=len(poll_data)-1,
    valinit=0,
)
ax4.margins(0)

slider.on_changed(update)
plt.gcf().subplots_adjust(left = 0.06, right = .83)
plt.savefig('temp.png', bbox_inches = 'tight')
plt.show()
