#this file is for all parameter
from enum import(IntEnum, unique)

@unique
class Type(IntEnum):
    throughput = 1
    latency = 2

#ap, device setup
ap_num = 10
device_num = 100
operation_time = 300
lowerbound = 1 #minimum device for an AP
p_max = 30 #dbm
power_level = [0, 22, 24, 26, 28, 30]
frequency_channel_20 = [1,2,3,4,5,6,7,8,9,10,11]
frequency_channel_40 = [12,13,14,15,16]
frequency_channel_80 = [17,18]
frequency_channel_160 = [19]
ch_dic = {}
ch_dic[2] = [12]
ch_dic[3] = [12]
ch_dic[4] = [13, 17, 19]
ch_dic[5] = [13, 17, 19]
ch_dic[6] = [14, 17, 19]
ch_dic[7] = [14, 17, 19]
ch_dic[8] = [15, 18, 19]
ch_dic[9] = [15, 18, 19]
ch_dic[10] = [16, 18, 19]
ch_dic[11] = [16, 18, 19]
ch_dic[12] = [2, 3]
ch_dic[13] = [4, 5, 17, 19]
ch_dic[14] = [6, 7, 17, 19]
ch_dic[15] = [8, 9, 18, 19]
ch_dic[16] = [10, 11, 18, 19]
ch_dic[17] = [4, 5, 6, 7, 13, 14, 19]
ch_dic[18] = [8, 9, 10, 11, 15, 16, 19]
ch_dic[19] = [4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18]

#factory setup
factory_width = 200
factory_length = 180

#all mathematical model constant  
GTX = 4 #sender antenna gain
GRX = 4 #receiver antenna gain
ETA = 4 #path-loss exponent
CHI = 5 #standard deviation association with the degree of shadow fading
P_REF = 46 #the path loss at a reference distance(1m)
THETA_DECODE = -68 #threshold of decode signal strength
THETA_INTERFERENCE = -77 #threshold of interference signal strength