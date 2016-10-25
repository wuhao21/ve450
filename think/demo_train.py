import numpy as np
import random, math
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
import os

from demo_config import *

def idx_to_type(i):
	if i == 0: return 'SIN'
	if i == 1: return 'LINEAR'
	if i == 2: return 'QUADRATIC'
	if i == 3: return 'TRIANGLE'
	return 'ERROR'

def type_to_idx(name):
	for i in range(supported_type):
		if (idx_to_type(i)==name): return i
	return -1

def vec_to_type(res):
	tmp = 0
	ans = -1
	for x in range(res.shape[1]):
		if res[0,x]>tmp:
			tmp=res[0,x]
			ans=x
	return idx_to_type(ans)

def simu(v, lst, level):
# level 0: nothing changed
# level 1: with fluctuation 90%~110%
# level 2: with 10% possibilty to lose value (become last recorded value)
# level 3: both
	if level == 0: return v
	#v = v * (1+random.uniform(-1,1)/10.0)
	if level == 1: return v * (1+random.uniform(-1,1)/10.0)
	if level == 2:
		if int(random.uniform(-1,1)*1000) < 10: return lst
		else: return v
	if level == 3:
		if int(random.uniform(-1,1)*1000) < 10:
			return lst
		else: return v * (1+random.uniform(-1,1)/10.0)

def signal_generator(x, type, level):
	if type == 0: #SIN
		A = random.uniform(-1,1)
		b = random.uniform(-1,1)*math.pi
		c = random.uniform(-1,1)
		k = random.uniform(-1,1)
		y = []
		for j in x:
			v = A*math.sin(k*j+b)+c
			val = simu(v,0 if len(y)==0 else y[-1],level)
			y.append(val)
	if type == 1: #LINEAR
		A = random.uniform(-1,1)
		c = random.uniform(-50,50)
		y = []
		for j in x:
			v = A*j+c
			val = simu(v,0 if len(y)==0 else y[-1],level)
			y.append(val)
	if type == 2: #QUADRATIC
		A = random.uniform(-10,10)
		b = random.uniform(-1,1)
		c = random.uniform(-1000,1000)
		#print(c)
		y = []
		for j in x:
			v = A*j*j+b*j+c
			val = simu(v,0 if len(y)==0 else y[-1],level)
			y.append(val)
	if type == 3: #TRIANGLE
		A = random.uniform(-1,1)
		c = random.uniform(-50,50)
		A1 = A*-1
		c1 = 2*A*x[int(sample_num/2+1)]+c
		y = []
		for j in x[:int(sample_num/2+1)]:
			v = A*j+c
			val = simu(v,0 if len(y)==0 else y[-1],level)
			y.append(val)
		for j in x[int(sample_num/2+1):]:
			v = A1*j+c1
			val = simu(v,0 if len(y)==0 else y[-1],level)
			y.append(val)
	return y

def data_generator(l,r,num_of_points,num_for_each,K,level):
	X=[]
	Y=[]
	x=np.linspace(l,r,num_of_points)
	for i in range(num_for_each):
		for t in range(supported_type):
			X.append(signal_generator(x, t, level));
			Y.append(t);
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

if __name__=='__main__':
	nb_classes = supported_type
	(X_train, y_train), (X_test, y_test) = data_generator(sample_l,sample_r,sample_num,data_num,test_k,simu_level)
	#(X_train, y_train), (X_test, y_test) = raw_to_array('raw_data.txt', 0.2)
	Y_train = np_utils.to_categorical(y_train, nb_classes)
	Y_test = np_utils.to_categorical(y_test, nb_classes)
	print('x_train shape:', X_train.shape)
	print('y_train shape:', Y_train.shape)
	print('x_test shape:', X_test.shape)
	print('y_test shape:', Y_test.shape)

	input('Enter to go on...')
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
	input('Enter to go on...')
	sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
	model.compile(loss='categorical_crossentropy',
	          optimizer=RMSprop(),
	          metrics=['accuracy'])

	model.fit(X_train, Y_train, nb_epoch=nb_epoch, verbose=1)
	score = model.evaluate(X_test, Y_test, verbose=0)
	print(score)
	input('Enter to go on...')
	x = np.linspace(sample_l, sample_r, sample_num)

	for t in range(supported_type):
		for _ in range(3):
			line, = plt.plot(x, signal_generator(x, t, simu_level), '-', linewidth=2, label=idx_to_type(t)+str(_))
		plt.legend()
		plt.show()
	input('Enter to go on...')
	plt.clf()
	for _ in range(demo_num):
		t = random.randint(0,supported_type-1)
		y = np.array(signal_generator(x, t, simu_level))
		line, = plt.plot(x, y, '-', linewidth=2)
		y.shape=(sample_num, 1)
		y = np.transpose(y)
		res=model.predict(y, verbose=1)

		print('[FACT: '+idx_to_type(t)+' PREDICT: '+vec_to_type(res)+'] CORRECT!' if idx_to_type(t)==vec_to_type(res) else 'WRONG!')
		plt.show()

	


