import numpy as np
import random
import pygame
from pygame.locals import *
from itertools import chain
from ap import AP 
from device import DEVICE
from information_center import*
from utils import* 
from parameter import*

class Device_animate():
    def __init__(self, device):
        self.x = device.x*5
        self.y = device.y*5
        self.vx = device.vx*5
        self.vy = device.vy*5
        self.power = device.power
        self.channel = device.channel
        self.id = device.id
        self.type = device.type
        self.state = device.state
        self.ap = device.ap
        self.throughput = device.throughput
        self.timer = device.timer

    # connect ap to corresponding ap_animate
    def add_ap(self, ap_animate):
        if self.ap != None:
            for ap in ap_animate:
                if ap.id == self.ap.id:
                    self.ap =  ap

    def animation_attribute_update(self, device_list):
        for device in device_list:
            if device.id == self.id:
                self.x = device.x*5
                self.y = device.y*5
                self.vx = device.vx*5
                self.vy = device.vy*5
                self.power = device.power
                self.channel = device.channel
                self.id = device.id
                self.type = device.type
                self.state = device.state
                self.ap = device.ap  # remember the ap that connect to device_animate is connecting to ap_animate not ap
                self.throughput = device.throughput
                self.timer = device.timer

    def move(self):
        while True:
            self.vx = random.randint(-10, 10)
            self.vy = random.randint(-10, 10)
            if boundary((self.x + self.vx)/5, (self.y + self.vy)/5):
                self.x = self.x + self.vx
                self.y = self.y + self.vy
                break
            else:
                continue

class AP_animate():
    def __init__(self, ap):
        self.x = ap.x*5
        self.y = ap.y*5
        self.power = ap. power
        self.channel = ap.channel
        self.id = ap.id
        self.type = ap.type
        self.timer = ap.timer
        self.state = ap.state
        self.cci = ap.cci
        self.interference_range = ap.interference_range*5
        self.communication_range = ap.communication_range*5
        self.throughput = ap.throughput
        self.lowerbound = ap.lowerbound
        self.upperbound = ap.upperbound

    def animation_attribute_update(self, ap_list):
        for ap in ap_list:
            if ap.id == self.id:
                self.x = ap.x*5
                self.y = ap.y*5
                self.power = ap. power
                self.channel = ap.channel
                self.id = ap.id
                self.type = ap.type
                self.timer = ap.timer
                self.state = ap.state
                self.cci = ap.cci
                self.interference_range = ap.interference_range*5
                self.communication_range = ap.communication_range*5
                self.throughput = ap.throughput
                self.lowerbound = ap.lowerbound
                self.upperbound = ap.upperbound

random.seed(1126)
# set global timer to 0
t = 0

# first simulation setup
# creare ap list
temp_ap = [[AP(18 * (i + 1), 20 * (j + 1), 9 * i + j + 1, Type.throughput) for j in range(9)] for i in range(9)] #2D array
# turn 2D list into 1D list
ap_list = list(chain.from_iterable(temp_ap))
# make half of AP type 2 and assign lowerbound, uppperbound
for i in range(len(ap_list)):
    if i%2 != 0:
        ap_list[i].type = Type.delay
        ap_list[i].lowerbound = lowerbound_delay
        ap_list[i].upperbound = upperbound_delay
    else:
        ap_list[i].lowerbound = lowerbound_throughput
        ap_list[i].upperbound = upperbound_throughput
# create device list
device_list = [DEVICE(random.uniform(0, 180), random.uniform(0, 200), random.randint(1, 3), random.randint(1, 3), i+1, Type.throughput) for i in range(device_num1+device_num2)]
# make half of device type 2
for i in range(len(device_list)):
    if i%2 != 0:
        device_list[i].type = Type.delay

# resource initialization
init(ap_list, device_list) 
power_allocation(ap_list)
channel_allocation(ap_list)
channel_enhancement(ap_list)
device_resource(device_list)
log_info(ap_list, device_list)
print(loss_device_count(device_list))
print(t)

# creare device and ap animation list
device_animate = []
ap_animate = []
for ap in ap_list:
    ap_animate.append(AP_animate(ap))
for device in device_list:
    device_animate.append(Device_animate(device)) 
# add devie_animate ap since the origin is connect to ap_list no ap_animate
for device in device_animate:
    if device.ap != None:
        device.add_ap(ap_animate)

# animation setup
pygame.init()
win = pygame.display.set_mode((factory_width*5, factory_length*5))
pygame.display.set_caption("Simulation")
clock = pygame.time.Clock()
#main loop
run = True
while run :
    clock.tick(60)
    keys = pygame.key.get_pressed()
    win.fill(WHITE)

    for device in device_animate:
        device.animation_attribute_update(device_list)
        device.add_ap(ap_animate)
        if device.ap != None:
            pygame.draw.circle(win, BLACK, (device.y, device.x), 3)
            pygame.draw.line(win, BLACK, (device.y, device.x), (device.ap.y, device.ap.x), 1) 
        else:   
            pygame.draw.circle(win, DIMGRAY, (device.y, device.x), 3)
        text, textRect = txt(device)
        win.blit(text, textRect)       
    for ap in ap_animate:
        ap.animation_attribute_update(ap_list)
        if ap.channel == 0:
            continue
        elif ch_id_to_bw[ap.channel] == 20:
            pygame.draw.circle(win, GREEN, (ap.y, ap.x), 3)
        elif ch_id_to_bw[ap.channel] == 40:
            pygame.draw.circle(win, RED, (ap.y, ap.x), 3)
        elif ch_id_to_bw[ap.channel] == 80:
            pygame.draw.circle(win, BLUE, (ap.y, ap.x), 3)
        elif ch_id_to_bw[ap.channel] == 160:
            pygame.draw.circle(win, PURPLE, (ap.y, ap.x), 3)
        pygame.draw.circle(win, (255, 160, 122), (ap.y, ap.x), ap.interference_range, 1)
        text, textRect = txt(ap)
        win.blit(text, textRect)  
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            run = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
        if keys[pygame.K_SPACE]:
            t += 1
            print('t = ', t)
            for device in device_list:
                device.move()
            for device in device_list:
                # if device.id == 44 and t == 49:
                #      print('here')
                flag_device, device_next_state = device.state_change(ap_list)
                if flag_device:
                    device.action(device_next_state, ap_list)
            for ap in ap_list:
                # if ap.id == 20 or ap.id == 28:
                #     print('here') 
                flag_ap, ap_next_state = ap.state_change(ap_list, device_list)
                if flag_ap:
                    ap.action(ap_next_state, ap_list, device_list)
            for device in device_list:
                device.timer -= 1
            for ap in ap_list:
                ap.timer -= 1
            log_info(ap_list, device_list)  
            print(loss_device_count(device_list))
    pygame.display.update()
pygame.quit()  