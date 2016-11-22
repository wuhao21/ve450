from utils import *
import signal
import time
import numpy as np
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils

def quit(signum, frame):
    print()
    print('%s|Stopping the thinking part...'%get_time())
    #tcpCliSock.close()
    sys.exit()


signal.signal(signal.SIGINT, quit)
signal.signal(signal.SIGTERM, quit)

print("%s|initialization..."%get_time())
last_timestamp = None
pool = []
tmp_data = []
votes = []
print("%s|loading model..."%get_time())
model = load_model('brain.h5')
while True:
    if (last_timestamp == None):
        pool = read_from_db("ve450","root","1234","cnclinear","*","WHERE time >'%s'"%get_1minago())
        if (len(pool) == 0):
            #print(pool)
            print("%s|Database is empty... Wait for %.2f sec"%(get_time(),window_size))
            time.sleep(window_size)
            continue
        last_timestamp = pool[-1][key_to_idx("time")]
        for i in range(nb_classes):
            votes.append(0)
    else:
        tmp_data = read_from_db("ve450","root","1234","cnclinear","*","WHERE time>'%s'"%last_timestamp)
        if (len(tmp_data) == 0):
            print("%s|No new data... Wait for %.2f sec"%(get_time(),wait_interval))
            time.sleep(wait_interval)
            continue
        data_point = tmp_data[-1]
        #print(last_timestamp, data_point)
        if data_point[key_to_idx("processing")]:
            last_timestamp = data_point[key_to_idx("time")]
            if pool_add(pool, data_point):
#enough length to predict
                #print("pool length is %d"%len(pool))
                X=[]
                X.append(data_to_feature(pool))
                X=np.array(X)
                #print(X.shape)
                res = model.predict(X)
                votes[type_to_idx(vec_to_type(res))] += 1
                winner = election(votes)
                if winner == -1:
                    print("%s|Too less points... Still voting..."%get_time())
                else:
                    print("%s|It Should be %s"%(get_time(),recog_types[winner]))
            else:
                print("%s|Too less information!!"%get_time())
#too less info
        else:
            print("%s|Not working..."%get_time())
            for i in range(nb_classes):
                votes[i]=0
            last_timestamp = None
            continue


