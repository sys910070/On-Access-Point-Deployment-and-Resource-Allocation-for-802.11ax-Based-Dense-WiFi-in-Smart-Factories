#this file is for small function
import matplotlib.pyplot as plt
from parameter import*
import random

#distance between two device(AP or STA)
def distance(a, b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)

# communication range or interference range
def range_(power):
    return 10**((power+GTX+GRX-P_REF-CHI-THETA_DECODE)/(10*ETA))

# maximum distance device in an ap
def max_dis_device(ap):
    dis = 0
    for device in ap.user:
        if distance((device.x, device.y), (ap.x, ap.y)) > dis:
            dis = distance((device.x, device.y), (ap.x, ap.y))
    return dis

# check if channels are overlapped
def overlap(ch1, ch2):
    for channel in ch_dic[ch1]:
        if channel == ch2:
            return True
    return False

# find the channel with minimum neighbor using
def min_user_channel(ap):
    def find_min_user_channel(dic):
        min_user = float("inf")
        candidate_channel = []
        for key, value in dic.items():
            if value < min_user:
                min_user = value
                candidate_channel = [key]
            elif value == min_user:
                candidate_channel.append(key)
        return random.choice(candidate_channel)
    dic = {}
    for neighbor in ap.neighbor:
        if neighbor.channel == 0:
            continue
        if neighbor.channel not in dic.keys():
            dic[neighbor.channel] = 1
        else:
            dic[neighbor.channel] += 1
    return find_min_user_channel(dic)
        
    
#graph
def graph_device(ap_list, device_list):
    for ap in ap_list:
        plt.plot(ap.y, ap.x,'ro', color = 'green') # AP
        plt.text(ap.y+1, ap.x+1, ap.id, color='green')
    for device in device_list:    
        plt.plot(device.y, device.x, 'ro', color = 'red') # device
        plt.text(device.y+1, device.x+1, device.id, color='red')

    plt.axis([0, 200, 0, 180])
    plt.show()


# performance matric
# fairness index
def fairness(ap_list):
    x1 = 0
    x2 = 0
    for ap in ap_list:
        x1 = x1+ap.throughput/len(ap.user)
        x2 = x2+(ap.throughput/len(ap.user))**2
    return x1**2/(ap_num*x2)
