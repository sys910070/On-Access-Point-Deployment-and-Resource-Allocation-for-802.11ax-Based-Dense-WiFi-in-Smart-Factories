#this file is for all parameter
from enum import(IntEnum, unique)
from turtle import delay
import numpy as np

@unique
class Type(IntEnum):
    throughput = 1
    delay = 2

#ap, device setup
#type 1(high throughput device, AP), type 2(delat sensitive device)
ap_num1 = 41
ap_num2 = 40
ap_num = ap_num1+ap_num2
device_num1 = 100
device_num2 = 100
device_num = device_num1+device_num2
upperbound_throughput = 7 # maxixmum device for an AP
upperbound_delay = 10
lowerbound_throughput = 2 #minimum device for an AP
lowerbound_delay = 2
transition_upperbound = 5
p_max = 30 #dbm
power_level = [0, 22, 24, 26, 28, 30] 
frequency_channel_20 = np.arange(1,12) # 1~11
frequency_channel_40 = np.arange(12,17) # 12~16
frequency_channel_80 = np.arange(17,19) # 17~18
frequency_channel_160 = np.arange(19,20) #19

# all timer parameter
operation_time = 30 # second
d_state_timer_handover = 2
d_state_timer_detached = 2
d_state_timer_search = 5
a_state_timer_underpopulate = 2
a_state_timer_idle = 2

# qos reqirement
total_throughput_qos = 7000
device_throughput_qos = 20
device_throughput_ratio_reqirment = 0.5

# channel overlap dictionary
ch_dic = {}
ch_dic[1] = [1]
ch_dic[2] = [2, 12]
ch_dic[3] = [3, 12]
ch_dic[4] = [4, 13, 17, 19]
ch_dic[5] = [5, 13, 17, 19]
ch_dic[6] = [6, 14, 17, 19]
ch_dic[7] = [7, 14, 17, 19]
ch_dic[8] = [8, 15, 18, 19]
ch_dic[9] = [9, 15, 18, 19]
ch_dic[10] = [10, 16, 18, 19]
ch_dic[11] = [11, 16, 18, 19]
ch_dic[12] = [2, 3, 12]
ch_dic[13] = [4, 5, 13, 17, 19]
ch_dic[14] = [6, 7, 14, 17, 19]
ch_dic[15] = [8, 9, 15, 18, 19]
ch_dic[16] = [10, 11, 16, 18, 19]
ch_dic[17] = [4, 5, 6, 7, 13, 14, 17, 19]
ch_dic[18] = [8, 9, 10, 11, 15, 16, 18, 19]
ch_dic[19] = [4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19]

# channel id to bandwidth dictionary
ch_id_to_bw = {}
for idx, channel_group in enumerate((frequency_channel_20, frequency_channel_40,
    frequency_channel_80, frequency_channel_160)):
    for channel in channel_group:
        ch_id_to_bw[channel] = 20 * 2 ** idx

#factory setup
factory_width = 200
factory_length = 180

# function if device hit boundary return False, else return True
def boundary(x, y):
    if x < 0 or y < 0 or x > factory_length or y > factory_width:
        return False
    else:
        return True

#all mathematical model constant  
GTX = 4 #sender antenna gain
GRX = 4 #receiver antenna gain
ETA = 4 #path-loss exponent
CHI = 5 #standard deviation association with the degree of shadow fading
P_REF = 46 #the path loss at a reference distance(1m)
THETA_DECODE = -68 #threshold of decode signal strength(dBm)
THETA_INTERFERENCE = -77 #threshold of interference signal strength(dBm)
NOISE = -90 # in db
TRANSMITTING_RATE = 7500000/8 #MB/s
T_TF = 68/TRANSMITTING_RATE # 68B
T_MBA = 118/TRANSMITTING_RATE
T_OFDMABA = 32/TRANSMITTING_RATE
T_SIFS = 0.00001
TXOP = 0.003
T_ULPPDU = TXOP-2*T_SIFS-T_TF-T_MBA
T_DLPPDU = 2*T_ULPPDU
T_UL = TXOP
T_DL = 2*T_SIFS+T_DLPPDU+T_OFDMABA

# animation factor
scale = 5

# color
# background
WHITE = (255, 255, 255)
# AP
LIME = (204, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
# Device
BLACK = (0, 0, 0)
DIMGRAY = (105, 105, 105)
# text
GREEN = (0, 255, 0)

CADEBLUE1 = (152,245,255)