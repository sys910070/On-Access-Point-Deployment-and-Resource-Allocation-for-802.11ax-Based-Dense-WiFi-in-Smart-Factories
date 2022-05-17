import numpy as np
import random
import math
import matplotlib.pyplot as plt
import ap
import device

power_level = [p_max, p_max/2, p_max/4, p_max/8, p_max/16, 0]
frequency_channel_20 = []
frequency_channel_40 = []
frequency_channel_80 = []
frequency_channel_160 = []

#distance between two device(AP or STA)
def distance(a, b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)
