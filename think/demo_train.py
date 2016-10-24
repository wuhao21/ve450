import numpy as np

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
import os

def raw_to_array(file, k):
	fin=open(file,'r')
	x=[]
	y=[]
	num = 0
	for line in fin:
		num = num + 1
		data=str(line).split('\t')
		x.append(data[1:len(data)-1])
		y.append(data[-1])
	thres = int(num*k)
	x_test=np.array(x[:thres]);
	y_test=np.array(y[:thres]);
	x_train=np.array(x[thres:]);
	y_train=np.array(y[thres:]);
	return (x_train, y_train), (x_test, y_test)

nb_classes = 3
nb_epoch = 20

(X_train, y_train), (X_test, y_test) = raw_to_array('raw_data.txt', 0.2)
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)
print('x_train shape:', X_train.shape)
print('y_train shape:', Y_train.shape)
print('x_test shape:', X_test.shape)
print('y_test shape:', Y_test.shape)


'''
model = Sequential()
model.add(Dense(64, input_dim=x_train.shape[1], init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))
model.add(Dense(64, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes, init='uniform'))
model.add(Activation('softmax'))

sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model.fit(X_train, y_train,
          nb_epoch=20,
          batch_size=16)
score = model.evaluate(X_test, y_test, batch_size=16)
'''