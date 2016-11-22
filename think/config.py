db_keys=('time','room_temp','mot_temp','current','displacement','processing')
num_keys=len(db_keys)
recog_types=('Sin','Linear')
num_types=len(recog_types)
window_size=3# seconds
sample_num=window_size*10
wait_interval=0.5
confidence_thres=0.99

least_votes=10
#fit parameters
nb_classes=2
nb_epoch=20
validation_split=0.2

#temp_alarm
temp_diff_limit = 5
temp_upper_limit = 30

#current_alarn
current_upper_limit = 200

#cut_blocking
block_window=1#seconds
block_sample_num=block_window*20
