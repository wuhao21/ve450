from utils import *
import signal
import time
import numpy as np
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils

def quit(signum, frame):
    print('Stopping the thinking part...')
    #tcpCliSock.close()
    sys.exit()


signal.signal(signal.SIGINT, quit)
signal.signal(signal.SIGTERM, quit)

print("initialization...")
last_timestamp = None
pool = []
tmp_data = []
votes = []
print("loading model...")
model = load_model('brain.h5')
print("working...")
while True:
    if (last_timestamp == None):
        pool = read_from_db("ve450","root","1234","cnclinear")
        if (len(pool) == 0):
            print("Database is empty... Wait for %d sec"%window_size)
            time.sleep(window_size)
            continue
        last_timestamp = pool[-1][key_to_idx("time")]
        for i in range(nb_classes):
            votes.append(0)
    else:
        tmp_data = read_from_db("ve450","root","1234","cnclinear","*","WHERE time>%s"%last_timestamp)
        if (len(tmp_data) == 0):
            print("No new data... Wait for %d sec"%window_size)
            time.sleep(window_size)
            continue
        print(last_timestamp)
        print(len(tmp_data))
        data_point = tmp_data[-1]
        if data_point[key_to_idx("processing")]:
            last_timestamp = data_point[key_to_idx("time")]
            if pool_add(pool, data_point):
#enough length to predict
                X = data_to_feature(pool)
                res = model.predict(X)
                votes[type_to_idx(vec_to_type(res))] += 1
                winner = election(votes)
                if winner == -1:
                    print("Too less points... Still voting...")
                else:
                    print("It Should be %s"%recog_types(winner))
            else:
                print("Too less information!!")
#too less info
        else:
            print("Not working...")
            for i in range(nb_classes):
                votes[i]=0
            last_timestamp = None
            continue


