import numpy as np
import random, math

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
import os

def simu(v, lst, level):
# level 0: nothing changed
# level 1: with fluctuation 90%~110%
# level 2: with 10% possibilty to lose value (become last recorded value)
# level 3: ...
	if level == 0: return v
	v = v * (1+(random.random()-0.5)/5.0)
	if level == 1: return v
	if (int(random.random()*1000) < 100): return 0;
	return v;

def data_generator(l,r,step,num_for_each,K,level):
	X=[]
	Y=[]
	x=[]
	while(l<=r):
		x.append(l)
		l = l + step
	for i in range(num_for_each):
		#SIN 0
		A = random.random()+1
		b = random.random()*math.pi
		c = random.random()
		k = random.random()+1
		y = []
		for j in x:
			v = A*math.sin(k*j+b)+c
			val = simu(v,0 if len(y)==0 else y[-1],level)
			y.append(val)
		X.append(y);
		Y.append(0);
		#LINEAR 1
		A = random.random()+1
		c = random.random()
		y = []
		for j in x:
			v = A*j+c
			val = simu(v,0 if len(y)==0 else y[-1],level)
			y.append(val)
		X.append(y);
		Y.append(1);
		#QUADRATIC 2
		A = random.random()+1
		b = random.random()
		c = random.random()
		y = []
		for j in x:
			v = A*j*j+b*j+c
			val = simu (v,0 if len(y)==0 else y[-1],level)
			y.append(val)
		X.append(y);
		Y.append(1);
	thres = int(len(Y)*K)
	x_test = np.array(X[:thres]);
	y_test = np.array(Y[:thres]);
	x_train = np.array(X[thres:]);
	y_train = np.array(Y[thres:]);
	return (x_train, y_train), (x_test, y_test)

def raw_to_array_from_file(file, k):
	fin=open(file,'r')
	x = []
	y = []
	num = 0
	for line in fin:
		num = num + 1
		data=str(line).split('\t')
		x.append(data[1:len(data)-1])
		y.append(data[-1])
	thres = int(num*k)
	x_test = np.array(x[:thres]);
	y_test = np.array(y[:thres]);
	x_train = np.array(x[thres:]);
	y_train = np.array(y[thres:]);
	return (x_train, y_train), (x_test, y_test)

nb_classes = 3
nb_epoch = 5
(X_train, y_train), (X_test, y_test) = data_generator(-5.0,5.0,0.1,1000,0.3,2)
#(X_train, y_train), (X_test, y_test) = raw_to_array('raw_data.txt', 0.2)
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)
print('x_train shape:', X_train.shape)
print('y_train shape:', Y_train.shape)
print('x_test shape:', X_test.shape)
print('y_test shape:', Y_test.shape)


model = Sequential()
model.add(Dense(64, input_dim=X_train.shape[1]))
model.add(Activation('tanh'))
model.add(Dropout(0.2))
model.add(Dense(64))
model.add(Activation('tanh'))
model.add(Dropout(0.2))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.summary()

sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

model.fit(X_train, Y_train, nb_epoch=nb_epoch, verbose=1)
score = model.evaluate(X_test, Y_test, verbose=0)
print(score)
