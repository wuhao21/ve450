from utils import *
from config import *

import numpy as np
import time
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils

train_x = []
train_y = []

#bigsin 0
records = read_from_db("ve450","root","1234","bigsin","time,displacement")
flags = read_from_db("ve450","root","1234","bigsin","processing")
print(len(records))
l = r = 0
while l<=r and r<len(flags):
    if (flags[r][0] == 0):
        if (l == r):
            l = l + 1
            r = r + 1
            continue
        else:
            #print(l,r)
            raw_data = data_clean(records[l:r])
            tmp_x, tmp_y = sliding(raw_data, 0)
            train_x.extend(tmp_x)
            train_y.extend(tmp_y)
            l = r
    else:
        r = r + 1

#linear 1
records = read_from_db("ve450","root","1234","linear","time,displacement")
flags = read_from_db("ve450","root","1234","linear","processing")
print(len(records))
l = r = 0
while l<=r and r<len(flags):
    if (flags[r][0] == 0):
        if (l == r):
            l = l + 1
            r = r + 1
            continue
        else:
            #print(l,r)
            #start = time.clock()
            raw_data = data_clean(records[l:r])
            #flag1 = time.clock()
            tmp_x, tmp_y = sliding(raw_data, 1)
            #flag2 = time.clock()
            #print("clean: %f s, sliding: %f s."%(flag1-start, flag2-flag1))
            train_x.extend(tmp_x)
            train_y.extend(tmp_y)
            l = r
    else:
        r = r + 1

print('data extraction finished...')
train_x = np.array(train_x)
train_y = np.array(train_y)
train_y = np_utils.to_categorical(train_y, nb_classes)
model = Sequential()
model.add(Dense(64, input_dim=sample_num))
model.add(Activation('tanh'))
model.add(Dropout(0.2))
model.add(Dense(64))
model.add(Activation('tanh'))
model.add(Dropout(0.2))
model.add(Dense(nb_classes))
model.add(Activation('sigmoid'))
model.summary()
model.compile(loss='binary_crossentropy', optimizer='rmsprop',metrics=['accuracy'])
print('start training...')
model.fit(train_x, train_y, nb_epoch=nb_epoch, validation_split=validation_split, shuffle=True)
model.save('brain.h5')

