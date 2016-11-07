db_keys=('time','room_temp','mot_temp','current','displacement','processing')
num_keys=len(db_keys)
recog_types=('Sin','SmallSin','Linear')
num_types=len(recog_types)
window_size=5# seconds
sample_num=window_size*20
