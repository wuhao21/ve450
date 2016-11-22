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
conn = psycopg2.connect(host="localhost", dbname="ve450", user='root', password='1234') #database configuration
cursor = conn.cursor()
try:
    cursor.execute("CREATE TABLE CNCLinear_result (time varchar, mot_temp real, room_temp real, current real, displacement real, wave varchar, temp_high int, current_high int, is_cutblocking int);")
    except:
        print("Table CNCLinear_result exists, skipped\n")
conn.commit()
cursor.close()

last_timestamp = None
pool = []
tmp_data = []
votes = []
flag = False
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
        
        curr_time = datapoint[0]
        mot_temp = datapoint[1]
        room_temp = datapoint[2]
        current = datapoint[3]
        displacement = datapoint[4]
        is_processing = datapoint[5]



        
        #print(last_timestamp, data_point)
        last_timestamp = data_point[key_to_idx("time")]
        winner = -1;
        if data_point[key_to_idx("processing")]:
            if pool_add(pool, data_point):
#enough length to predict
                flag = True
                #print("pool length is %d"%len(pool))
                X=[]
                X.append(data_to_feature(pool, idx=key_to_idx("displacement")))
                X=np.array(X)
                #print(X.shape)
                res = model.predict(X)
                #votes[type_to_idx(vec_to_type(res))] += 1
                #winner = election(votes)
                winner = vec_to_idx(res)       
                if winner != -1:
                    print("%s|It Should be %s"%(get_time(),idx_to_type(winner)))
                    #print(X)
            else:
                if (not flag):
                    print("%s|Too less information!!"%get_time())
                else:
                    continue
#too less info
        else:
            if (len(pool)!=0):
                print("%s|Not working..."%get_time())
            for i in range(nb_classes):
                votes[i]=0
            pool=[]
            tmp_data=[]
            flag = False
            continue
        if(is_processing == 0):
            wave = "not working"
        else:
            wave = idx_to_type(winner)
        if(temp_alarm(room_temp,mot_temp)==True):
            temp_high = 1
        else:
            temp_high = 0
        if(current_alarm(current)==True):
            current_high = 1
        else:
            current_high = 0
        is_cutblocking= 0     
        write_data=(datapoint[0],datapoint[1],datapoint[2],datapoint[3],datapoint[4],wave,temp_high,current_high,is_cutblocking)
        write_db(write_data);

    
        


