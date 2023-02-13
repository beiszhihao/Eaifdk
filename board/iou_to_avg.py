import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

path=__file__
base_dir=os.path.dirname(path)

with open(base_dir + '/' + sys.argv[1]) as f:
    list1 = f.read().splitlines()

#del x_lines[0:len(x_lines) - 1000]

dictionary = {'x': list1}
data = pd.DataFrame(dictionary)
data.head()
data.tail()
data['x'] = pd.to_numeric(data['x'])
data.dtypes

print(data['x'])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(data['x'].values,label='iou_loss')
ax.legend(loc='best')
ax.set_title('The iou curves')
ax.set_xlabel('batches')
ax.set_ylabel('iou')
fig.savefig(base_dir + '/images/avg_iou')
