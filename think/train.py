from utils import *

import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
ALL = read_from_db("ve450","root","1234","*")
records = read_from_db("ve450","root","1234","time,displacement")
flags = read_from_db("ve450","root","1234","processing")
print(len(records))
l = r = 0
train_x = []
train_y = []
while l<=r and r<len(flags):
    if (flags[r][0] == 0):
        if (l == r):
            l = l + 1
            r = r + 1
            continue
        else:
            raw_data = data_clean(records[l:r])
            tmp_x, tmp_y = sliding(raw_data, 0)
            train_x.extend(tmp_x)
            train_y.extend(tmp_y)
            l = r
    else:
        r = r + 1
train_x = np.array(train_x)
print(train_x.shape)

