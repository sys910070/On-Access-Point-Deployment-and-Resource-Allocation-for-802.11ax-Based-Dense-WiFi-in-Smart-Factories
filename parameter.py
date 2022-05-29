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
powerlevel = [30, 28, 26, 24, 22, 0] #還沒決定要用除的還是用減的，其他論文上是用減的
frequency_channel_20 = [1,2,3,4,5,6,7,8,9,10,11]
frequency_channel_40 = [12,13,14,15,16]
frequency_channel_80 = [17,18]
frequency_channel_160 = [19]

#factory setup
factory_width = 200
factory_length = 180

