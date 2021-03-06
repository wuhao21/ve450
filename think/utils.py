import numpy as np
import os, sys, psycopg2
import datetime
from datetime import timedelta

from config import *

def idx_to_type(i):
    if (i == -1):
        return "unknown"
    if (i < num_types):
        return recog_types[i]
    else:
        return 'ERROR'

def type_to_idx(name):
	for i in range(num_types):
		if (recog_types[i]==name): return i
	return -1

def key_to_idx(key):
    for i in range(num_keys):
        if (db_keys[i]==key): return i
    return -1

def vec_to_idx(res, ct):
    tmp = 0
    ans = -1
    for x in range(res.shape[1]):
        if res[0,x]>tmp:
            tmp=res[0,x]
            ans=x
    if (tmp > ct):
        return ans
    else:
        return -1

def election(votes):
    if sum(votes) < least_votes:
        return -1
    tmp = 0
    ans = -1
    for x in range(len(votes)):
        if votes[x]>tmp:
            tmp=votes[x]
            ans=x
    return ans

def string_to_datetime(TIME):
    return datetime.datetime.strptime(TIME, '%Y-%m-%d|%H:%M:%S:%f')

def get_time():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d|%H:%M:%S:%f')

def get_1minago():
    return datetime.datetime.strftime(datetime.datetime.now() - timedelta(minutes=1), '%Y-%m-%d|%H:%M:%S:%f')

def read_from_db(dbname, user, password, table="cnclinear", content="*", condition=""): # read the database
    conn = psycopg2.connect(host="localhost", dbname=dbname, user=user, password=password) #database configuration
    cursor = conn.cursor()
    records = []
    try:
        cursor.execute("SELECT %s FROM %s %s"%(content, table, condition)) #table name
        records = cursor.fetchall()
    except:
        print("Table is not find\n")
    conn.commit()
    cursor.close()
    return records

def write_db(write_data):
    conn = psycopg2.connect(host="localhost", dbname="ve450", user="root", password="1234")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO CNCLinear_result values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", write_data)
        #print('Wrote to the database', write_data)
    except:
        print("Insert CNCLinear_result Faild")
    conn.commit()
    cursor.close()
    return



def data_clean(raw_data): # raw_data should be (key, data) pair
    clean_data = []
    last_line = None;
    for line in raw_data:
        if (last_line == None or line[1]!=last_line[1]):
            clean_data.append(line)
        last_line = line
    return clean_data

def data_to_feature(raw_data, idx, sw):
    xp = []
    fp = []
    #print(raw_data[0])
    for line in raw_data:
        #print(line)
        if (sw == 0 or (sw == 1 and (string_to_datetime(raw_data[-1][0])-string_to_datetime(line[0])).total_seconds() <= block_window)):
            xp.append((string_to_datetime(line[0])-string_to_datetime(raw_data[0][0])).total_seconds())
            fp.append(float(line[idx]))
    if sw == 0:
        x = np.interp(np.linspace(0, xp[-1], sample_num), xp, fp)
        return x
    else:
        #x = np.interp(np.linspace(0, xp[-1], block_sample_num), xp, fp)
        #x = x - np.mean(x)
        x = np.array(fp)
        x = x - np.mean(x)
        xp = [0,np.var(x)]
        for idx in range(len(x)):
            if (idx > 0 and x[idx]*x[idx-1]<0):
                xp[0] += 1
        return xp

def sliding(data, TYPE): # data should be (key, data) pair
    l = r = 0
    res = []
    y = []
    while (l<=r and r<len(data)):
        while (r<len(data) and (string_to_datetime(data[r][0])-string_to_datetime(data[l][0])).total_seconds() < win): r=r+1
        if (r>=len(data)):
            break;
        res.append(data_to_feature(data[l:r], 1, 0))
        if TYPE != -1:
            y.append(TYPE)
        l = l + 1
    l = r = len(data) - 1
    while (l<=r and l>=0):
        while (l>=0 and (string_to_datetime(data[r][0])-string_to_datetime(data[l][0])).total_seconds() < win): l=l-1
        if (l<0):
            break;
        res.append(data_to_feature(data[l:r], 1, 0))
        if TYPE != -1:
            y.append(TYPE)
        r = r - 1
    if TYPE != -1:
        return res, y
    else:
        return res

def temp_alarm(room_temp, mot_temp):
    if (mot_temp > room_temp and mot_temp-room_temp > temp_diff_limit):
        return True
    else:
        if (mot_temp > temp_upper_limit):
            return True
        else:
            return False

def current_alarm(current):
    if (current > current_upper_limit):
        return True
    else:
        return False
def pool_add(pool, point, win): # pool should be list of (key, data) pair
    enough = False
    while (len(pool)>0 and (string_to_datetime(point[0])-string_to_datetime(pool[0][0])).total_seconds() > win):
        pool.pop(0)
        enough = True
    pool.append(point)
    return enough

