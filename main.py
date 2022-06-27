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
from optimization import*
from data_visualization import*

class Device_animate():
    def __init__(self, device):
        self.x = device.x*scale
        self.y = device.y*scale
        self.vx = device.vx*scale
        self.vy = device.vy*scale
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
                self.x = device.x*scale
                self.y = device.y*scale
                self.vx = device.vx*scale
                self.vy = device.vy*scale
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
            if boundary((self.x + self.vx)/scale, (self.y + self.vy)/scale):
                self.x = self.x + self.vx
                self.y = self.y + self.vy
                break
            else:
                continue

class AP_animate():
    def __init__(self, ap):
        self.x = ap.x*scale
        self.y = ap.y*scale
        self.power = ap. power
        self.channel = ap.channel
        self.id = ap.id
        self.type = ap.type
        self.timer = ap.timer
        self.state = ap.state
        self.cci = ap.cci
        self.interference_range = ap.interference_range*scale
        self.communication_range = ap.communication_range*scale
        self.throughput = ap.throughput
        self.lowerbound = ap.lowerbound
        self.upperbound = ap.upperbound

    def animation_attribute_update(self, ap_list):
        for ap in ap_list:
            if ap.id == self.id:
                self.x = ap.x*scale
                self.y = ap.y*scale
                self.power = ap. power
                self.channel = ap.channel
                self.id = ap.id
                self.type = ap.type
                self.timer = ap.timer
                self.state = ap.state
                self.cci = ap.cci
                self.interference_range = ap.interference_range*scale
                self.communication_range = ap.communication_range*scale
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
    else:
        device_list[i].vx = 0
        device_list[i].vy = 0

# resource initialization
init(ap_list, device_list) 
log_info(ap_list, device_list)
print('t = ', t)
print(loss_device_count(device_list))

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
win = pygame.display.set_mode((factory_width*scale, factory_length*scale))
pygame.display.set_caption("Simulation")
clock = pygame.time.Clock()

#main loop
run = True
while run :
    clock.tick(60)
    keys = pygame.key.get_pressed()
    win.fill(WHITE)  
    animation(ap_list, device_list, ap_animate, device_animate, win)
        
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT :
            run = False 
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
        # if keys[pygame.K_DOWN]:
    t += 1
    print('t = ', t)
    for device in device_list:
        device.move()
    for device in device_list:
        flag_device, device_next_state = device.state_change(ap_list)
        if flag_device:
            device.action(device_next_state, ap_list)
        device.dis_cal()
    for ap in ap_list:
        flag_ap, ap_next_state = ap.state_change(ap_list, device_list)
        if flag_ap:
            ap.action(ap_next_state, ap_list, device_list)
        # user selected_ap reset
        if ap.state == A_State.active:
            for user in ap.user: 
                user.selected = None
        elif ap.state == A_State.underpopulated:
            for user in ap.user:
                user.selected = None

    cci_calculation(ap_list)  
    throughput_cal(ap_list, device_list)
    all_timer_minus_one(device_list, ap_list)
    log_info(ap_list, device_list)

    if t == 30:
        for ap in ap_list:
            power_adjustment(ap, ap_list)
        channel_amplification(ap_list)

    if  not everything_ok(ap_list, device_list):
        print('no ok')
    else:
        print('ok')

    pygame.display.update()
pygame.quit()

# all kinds of info to print in console
            # cci_total = 0
            # for ap in ap_list:
            #     cci_total += ap.cci
            # total_throughput_ap, total_throughput_device = throughput_cal(ap_list, device_list)
            # print('total_throughput_ap = ', total_throughput_ap)
            # print('total_throughput_device = ', total_throughput_device)
            # print('total cci = ', cci_total)
            # print(loss_device_count(device_list))
            # print(fairness(ap_list))