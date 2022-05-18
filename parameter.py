from enum import(IntEnum, unique)

@unique
class Type(IntEnum):
    throughput = 1
    latency = 2
    security = 3

ap_num = 50
device_num = 100
p_max = 16
operation_time = 300
lowerbound = 1
powerlevel = [p_max, p_max/2, p_max/4, p_max/8, p_max/16, 0]
frequency_channel_20 = [1,2,3,4,5,6,7,8,9,10,11]
frequency_channel_40 = [12,13,14,15,16]
frequency_channel_80 = [17,18]
frequency_channel_160 = [19]

#distance between two device(AP to AP, AP to device, device to device)
def distance(a, b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)