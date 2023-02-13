import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
#%matplotlib inline

path=__file__
base_dir=os.path.dirname(path)
lines =sys.argv[1]    #改为自己生成的train_log_loss.txt中的行数
result = pd.read_csv(base_dir + '/train_log_loss.txt', skiprows=[x for x in range(int(lines)) if ((x%10!=9) |(x<1000))] ,error_bad_lines=False, names=['loss', 'avg', 'rate', 'seconds', 'images'])
result.head()
 
result['loss']=result['loss'].str.split(' ').str.get(1)
result['avg']=result['avg'].str.split(' ').str.get(1)
result['rate']=result['rate'].str.split(' ').str.get(1)
result['seconds']=result['seconds'].str.split(' ').str.get(1)
result['images']=result['images'].str.split(' ').str.get(1)
result.head()
result.tail()
 
# print(result.head())
# print(result.tail())
# print(result.dtypes)
 
#print(result['loss'])
print(result['avg'])
#print(result['rate'])
#print(result['seconds'])
#print(result['images'])
 
result['loss']=pd.to_numeric(result['loss'])
result['avg']=pd.to_numeric(result['avg'])
result['rate']=pd.to_numeric(result['rate'])
result['seconds']=pd.to_numeric(result['seconds'])
result['images']=pd.to_numeric(result['images'])
result.dtypes
 
 
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(result['avg'].values,label='avg_loss')
# ax.plot(result['loss'].values,label='loss')
ax.legend(loc='best')  #图列自适应位置
ax.set_title('The loss curves')
ax.set_xlabel('batches')
ax.set_ylabel('avg')
fig.savefig(base_dir + '/images/avg_loss')
# fig.savefig('loss')
