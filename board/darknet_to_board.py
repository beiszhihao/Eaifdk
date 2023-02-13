# coding=utf-8
 
import inspect
import os
import random
import sys

path=__file__
def extract_log(log_file,new_log_file,key_word):
    with open(log_file, 'r') as f:
      with open(new_log_file, 'w') as train_log:
  #f = open(log_file)
    #train_log = open(new_log_file, 'w')
        for line in f:
    # 去除多gpu的同步log
          if 'Syncing' in line:
            continue
    # 去除除零错误的log
          if 'nan' in line:
            continue
          if key_word in line:
            train_log.write(line)
    f.close()
    train_log.close()
 
base_dir = os.path.dirname(path)
extract_log(base_dir + '/train_output.txt', base_dir + '/train_log_loss.txt', 'images')
extract_log(base_dir + '/train_output.txt', base_dir + '/train_log_iou.txt', 'IOU')
