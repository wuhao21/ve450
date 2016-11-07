import numpy as np
#import random, math
import os, sys, psycopg2
import datetime

from config import *

def idx_to_type(i):
    if (i < num_types):
        return recog_types(i)
    else:
        return 'ERROR'

def type_to_idx(name):
	for i in range(num_types):
		if (recog_types(i)==name): return i
	return -1

def key_to_idx(key):
    for i in range(num_keys):
        if (db_keys(i)==name): return i
    return -1

def vec_to_type(res):
	tmp = 0
	ans = -1
	for x in range(res.shape[1]):
		if res[0,x]>tmp:
			tmp=res[0,x]
			ans=x
	return idx_to_type(ans)

def string_to_datetime(TIME):
    return datetime.datetime.strptime(TIME, '%Y-%m-%d|%H:%M:%S:%f')

def get_time():
    return datetime.datetime.strftime(datetime.datetime.now(), 'Y-m-%d|%H:%M:%S:%f')

def read_from_db(dbname, user, password, content): # read the database
    conn = psycopg2.connect(host="localhost", dbname=dbname, user=user, password=password) #database configuration
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT %s FROM cnclinear "%content) #table name
        records = cursor.fetchall()
    except:
        print("Table is not find\n")
    conn.commit()
    cursor.close()
    return records

def data_clean(raw_data): # raw_data should be (key, data) pair
    clean_data = []
    last_line = None;
    for line in raw_data:
        if (last_line == None or line[1]!=last_line[1]):
            clean_data.append(line)
        last_line = line
    return clean_data

def data_to_feature(raw_data):
    xp = []
    fp = []
    for line in raw_data:
        xp.append((string_to_datetime(line[0])-string_to_datetime(raw_data[0][0])).total_seconds())
        fp.append(float(line[1]))
    return np.interp(np.linspace(0, xp[-1], sample_num), xp, fp)

def sliding(data, TYPE): # data should be (key, data) pair
    l = r = 0
    res = []
    y = []
    while (l<=r and r<len(data)):
        while (r<len(data) and (string_to_datetime(data[r][0])-string_to_datetime(data[l][0])).total_seconds() < window_size): r=r+1
        if (r>=len(data)): break;
        res.append(data_to_feature(data[l:r]))
        y.append(TYPE)
        l = l + 1
    l = r = len(data) - 1
    while (l<=r and l>=0):
        while (l>=0 and (string_to_datetime(data[r][0])-string_to_datetime(data[l][0])).total_seconds() < window_size): l=l-1
        if (l<0): break;
        res.append(data_to_feature(data[l:r]))
        y.append(TYPE)
        r = r - 1
    return res, y
