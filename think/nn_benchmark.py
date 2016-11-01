import numpy as np
import random, math
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import LSTM
from keras.layers import Convolution1D, GlobalMaxPooling1D
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
import os, sys

from demo_config import *
from demo_train import *

nb_classes = supported_type
(X_train, y_train), (X_test, y_test) = data_generator(sample_l,sample_r,sample_num,data_num,test_k,simu_level)
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)
print('x_train shape:', X_train.shape)
print('y_train shape:', Y_train.shape)
print('x_test shape:', X_test.shape)
print('y_test shape:', Y_test.shape)
print('Build model...')
model = Sequential()

 #RELU_NN

model.add(Dense(128, input_dim=X_train.shape[1], activation='tanh'))
model.add(Dropout(0.5))
model.add(Dense(128, activation='tanh'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes, activation='softmax'))


'''
#LSTM
model.add(LSTM(input_shape=X_train.shape[1:], output_dim=64, activation='tanh', inner_activation='hard_sigmoid'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes, activation='softmax'))
'''

'''
#CNN
model.add(Convolution1D(64,3,
                        border_mode='same',
                        #activation='tanh',
                        input_dim=X_train.shape[1]))
model.add(GlobalMaxPooling1D())
model.add(Dense(hidden_dims))
model.add(Dropout(0.2))
model.add(Activation('relu'))
model.add(Dense(nb_classes, activation='softmax'))
'''
model.summary()

sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
          optimizer=RMSprop(),
          metrics=['accuracy'])

#tmp_input=[]
#tmp_input.append(X_train)
#X_train = np.array(tmp_input)
#X_train.reshape((X_train.shape[0],X_train.shape[1],1))
#print(X_train.shape)
#X_train = np.reshape(X_train, (1,) + X_train.shape)
#X_test = np.reshape(X_test, (1,) + X_test.shape)
model.fit(X_train, Y_train, nb_epoch=nb_epoch, verbose=1, batch_size=batch_size)
score = model.evaluate(X_test, Y_test, verbose=0)
print(score)