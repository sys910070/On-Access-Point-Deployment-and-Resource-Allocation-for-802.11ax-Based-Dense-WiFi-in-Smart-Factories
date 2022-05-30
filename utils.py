#this file is for small function
import matplotlib.pyplot as plt
from parameter import*

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
    for neighbor in ap.neighbor:
        pass
        
    
#graph
def graph_device(ap_list, device_list):
    for aps in ap_list:
        for ap in aps:
            plt.plot(ap.y, ap.x,'ro', color = 'green') # AP
            plt.text(ap.y+1, ap.x+1, ap.id, color='green')
    for device in device_list:    
        plt.plot(device.y, device.x, 'ro', color = 'red') # device
        plt.text(device.y+1, device.x+1, device.id, color='red')

    plt.axis([0, 200, 0, 180])
    plt.show()