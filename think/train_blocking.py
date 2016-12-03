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

def data_to_featureb(raw_data, T, idx=1):
    xp = []
    fp = []
    #print(raw_data[0])
    for line in raw_data:
        #print(line)
        xp.append((string_to_datetime(line[0])-string_to_datetime(raw_data[0][0])).total_seconds())
        fp.append(float(line[idx]))
    #fp = fp - np.mean(fp)
    #x = np.interp(np.linspace(0, xp[-1], block_sample_num), xp, fp)
    x = np.array(fp)
    x = x - np.mean(x)
    xp = [0,np.var(x)]
    for idx in range(len(x)):
        if (idx > 0 and x[idx]*x[idx-1]<0):
            xp[0] += 1
    #        xp[1] += np.abs(x[idx]-x[idx-1])
    #print(T)
    #print(xp)
    return xp

def slidingb(data, TYPE): # data should be (key, data) pair
    l = r = 0
    res = []
    y = []
    while (l<=r and r<len(data)):
        while (r<len(data) and (string_to_datetime(data[r][0])-string_to_datetime(data[l][0])).total_seconds() < block_window): r=r+1
        if (r>=len(data)): break;
        res.append(data_to_featureb(data[l:r], TYPE))
        y.append(TYPE)
        l = l + 1
    l = r = len(data) - 1
    while (l<=r and l>=0):
        while (l>=0 and (string_to_datetime(data[r][0])-string_to_datetime(data[l][0])).total_seconds() < block_window): l=l-1
        if (l<0): break;
        res.append(data_to_featureb(data[l:r], TYPE))
        if TYPE != -1:
            y.append(TYPE)
        r = r - 1
    if TYPE != -1:
        return res, y
    else:
        return res

if __name__ == "__main__":
    #normal 0
    records = read_from_db("ve450","root","1234","bigsin","time,displacement")
    flags = read_from_db("ve450","root","1234","bigsin","processing")
    #print(len(records))
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
                tmp_x, tmp_y = slidingb(raw_data, 0)
                train_x.extend(tmp_x)
                train_y.extend(tmp_y)
                l = r
        else:
            r = r + 1
    records = read_from_db("ve450","root","1234","linear","time,displacement")
    flags = read_from_db("ve450","root","1234","linear","processing")
    #print(len(records))
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
                tmp_x, tmp_y = slidingb(raw_data, 0)
                #flag2 = time.clock()
                #print("clean: %f s, sliding: %f s."%(flag1-start, flag2-flag1))
                train_x.extend(tmp_x)
                train_y.extend(tmp_y)
                l = r
        else:
            r = r + 1

    #print(get_time())
    records = read_from_db("ve450","root","1234","block","time,displacement","WHERE time>'2016-12-01|00:15:51:752206'")
    flags = read_from_db("ve450","root","1234","block","processing","WHERE time>'2016-12-01|00:15:51:752206'")
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
                tmp_x, tmp_y = slidingb(raw_data, 1)
                #flag2 = time.clock()
                #print("clean: %f s, sliding: %f s."%(flag1-start, flag2-flag1))
                train_x.extend(tmp_x)
                train_y.extend(tmp_y)
                l = r
        else:
            r = r + 1

    l = r = 0
    while l<=r and r<len(flags):
        if (flags[r][0] == 1):
            if (l == r):
                l = l + 1
                r = r + 1
                continue
            else:
                #print(l,r)
                #start = time.clock()
                raw_data = data_clean(records[l:r])
                #flag1 = time.clock()
                tmp_x, tmp_y = slidingb(raw_data, 0)
                #flag2 = time.clock()
                #print("clean: %f s, sliding: %f s."%(flag1-start, flag2-flag1))
                train_x.extend(tmp_x)
                train_y.extend(tmp_y)
                l = r
        else:
            r = r + 1

    #print('data extraction finished...')
    train_x = np.array(train_x)
    train_y = np.array(train_y)
    train_y = np_utils.to_categorical(train_y, nb_classes)
    model = Sequential()
    model.add(Dense(8, input_dim=block_sample_num))
    model.add(Activation('tanh'))
    model.add(Dropout(0.2))
    model.add(Dense(8))
    model.add(Activation('tanh'))
    model.add(Dropout(0.2))
    model.add(Dense(nb_classes))
    model.add(Activation('sigmoid'))
    model.summary()
    model.compile(loss='binary_crossentropy', optimizer='rmsprop',metrics=['accuracy'])
    #print('start training...')
    model.fit(train_x, train_y, nb_epoch=nb_epoch, validation_split=validation_split, shuffle=True)
    model.save('block.h5')
    model.save_weights('block_weights.h5')

