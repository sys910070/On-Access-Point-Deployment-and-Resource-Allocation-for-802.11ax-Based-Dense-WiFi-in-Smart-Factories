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
from environment_setting import*

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
            if boundary_no_obstacle((self.x + self.vx)/scale, (self.y + self.vy)/scale):
                self.x = self.x + self.vx
                self.y = self.y + self.vy
                break

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
ap_list = create_ap()
# create device list
if factory_environment == 'no_obstacle':
    device_list = create_device_no_obstacle()
elif factory_environment == 'symmetric_obstacle':
    device_list = create_device_symmetric_obstacle()
elif factory_environment == 'asymmetric_obstacle':
    device_list = create_device_asymmetric_obstacle()

# resource initialization
init(ap_list, device_list) 
log_info(ap_list, device_list)
cci_cal(ap_list)
throughput_cal(ap_list, device_list)
fairness_cal(ap_list)

print('t = ', t)

# save all kinds of data in a list and store initial(t=0) data first
fairness_record = []
total_throughput_record = []
lost_device_record = []
active_ap_record = []

# record an interval of data
fairness_record_interval = []
total_throughput_record__interval = []
lost_device_record_interval = []
active_ap_record_interval = []

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

    if factory_environment == 'symmetric_obstacle':
        symmetric_obstacle_draw(win)
    elif factory_environment == 'asymmetric_obstacle':
        asymmetric_obstacle_draw(win)  
    animation(ap_list, device_list, ap_animate, device_animate, win)
    
    if t == operation_time:
        if not os.path.exists('fig'):
            os.mkdir('fig')
        x = np.arange(0, len(fairness_record))
        graph_fairness(x, fairness_record)
        graph_throughput(x, total_throughput_record)
        graph_loss_device(x, lost_device_record)
        graph_active_ap(x, active_ap_record)
        if not os.path.exists('data'):
            os.mkdir('data')
        np.save(f'data/fairness_{factory_environment}', fairness_record)
        np.save(f'data/total_throughput_{factory_environment}', total_throughput_record)
        np.save(f'data/lost_device_{factory_environment}', lost_device_record)
        np.save(f'data/active_ap_{factory_environment}', active_ap_record)
        pygame.quit()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
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
        device.action(ap_list)
        device.dis_cal()
    for ap in ap_list:
        if len(ap.user)==0:
            ap.power_change(0, ap_list)
            ap.channel = 0
    cci_cal(ap_list)
    log_info(ap_list, device_list)

    fairness_record_interval.append(fairness_cal(ap_list))
    total_throughput_record__interval.append(throughput_cal(ap_list, device_list))
    lost_device_record_interval.append(loss_device_count(device_list))
    active_ap_record_interval.append(active_ap_count(ap_list))

    if t % interval == 0:
        fairness, throughput, loss_device, active_ap = calculate_interval_average(fairness_record_interval, total_throughput_record__interval, lost_device_record_interval, active_ap_record_interval)
        fairness_record.append(fairness)
        total_throughput_record.append(throughput)
        lost_device_record.append(loss_device)
        active_ap_record.append(active_ap)

        fairness_record_interval.clear()
        total_throughput_record__interval.clear()
        lost_device_record_interval.clear()
        active_ap_record_interval.clear()

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
            # print(throughput_lower)