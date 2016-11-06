import numpy as np
import random, math, os, sys, psycopg2
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils

from config import *

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

def read_from_db(): # read the database
    global conn
    global records
    conn = psycopg2.connect(host="localhost", dbname="ve450", user='root', password='1234') #database configuration
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM cnclinear WHICH processing>0") #table name
        records = cursor.fetchall()
    except:
        print("Table is not find\n")
    conn.commit()
    cursor.close()
    for i in records:
        print(str(i)+"\n")    #data is in global list records, print it out each line
    return 
