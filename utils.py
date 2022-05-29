#this file is for small function
import matplotlib.pyplot as plt

#distance between two device(AP or STA)
def distance(a, b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)

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