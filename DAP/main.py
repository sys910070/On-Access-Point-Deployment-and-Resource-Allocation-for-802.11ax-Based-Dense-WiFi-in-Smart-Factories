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
        self.gv = device.gv

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

random.seed(1356)

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
elif factory_environment == 'real_factory_layout':
    device_list = create_device_real_factory_layout()

# resource initialization
init(ap_list, device_list) 
log_info(ap_list, device_list)
cci_cal(ap_list)
throughput_cal(ap_list, device_list)
fairness_cal(ap_list)

print('t = ', t)


loss_device_list = []

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
    # win.fill(WHITE)

    # if factory_environment == 'symmetric_obstacle':
    #     symmetric_obstacle_draw(win)
    # elif factory_environment == 'asymmetric_obstacle':
    #     asymmetric_obstacle_draw(win)  
    # elif factory_environment == 'real_factory_layout':
    #     real_factory_layout_draw(win)

    # animation(ap_list, device_list, ap_animate, device_animate, win)
    
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

    if t % update_timer == 0:
        if fairness_cal(ap_list) > 0.6:
            print('resource improvement')
            for ap in ap_list:
                power_adjustment(ap, ap_list)
            channel_amplification(ap_list)
        else:
            print('fairness improvement')
        fairness_adjust_version2(ap_list, device_list)
    cci_cal(ap_list)
    all_timer_minus_one(device_list, ap_list)
    log_info(ap_list, device_list)

    
    loss_device_list.append(loss_device_count(device_list))

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

    if t == operation_time:
        total_loss_device = 0
        for i in range(99, 600):
            total_loss_device += loss_device_list[i]
        average_loss_device = total_loss_device/500
        print('experiment: other timer =', global_timer , 'search timer = ', 5)
        print('average loss device = ', average_loss_device)
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
            # if  not everything_ok(ap_list, device_list):
            #     print('no ok')
            # else:
            #     print('ok')