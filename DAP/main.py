from dis import dis
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

random.seed(1674)

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
initial_throughput_estimation = throughput_cal(ap_list, device_list)
ap_fairness_cal(ap_list)
device_fairness_cal(ap_list)

print('t = ', t)

# loss device vs timer
loss_device_list = []

# all qos record
throughput_record = []
throughput_qos_record = []
detached_qos_record = []

# save all kinds of data in a list and store initial(t=0) data first
ap_fairness_record = []
device_fairness_record = []
total_throughput_record = []
lost_device_record = []
active_ap_record = []
# record an interval of data
ap_fairness_record_interval = []
device_fairness_record_interval = []
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

# # animation setup
# pygame.init()
# win = pygame.display.set_mode((factory_width*scale, factory_length*scale))
# pygame.display.set_caption("Simulation")
# clock = pygame.time.Clock()

#main loop
run = True
while run :
    # clock.tick(60)
    # keys = pygame.key.get_pressed()
    # win.fill(WHITE)

    # if factory_environment == 'symmetric_obstacle':
    #     symmetric_obstacle_draw(win)
    # elif factory_environment == 'asymmetric_obstacle':
    #     asymmetric_obstacle_draw(win)  
    # elif factory_environment == 'real_factory_layout':
    #     real_factory_layout_draw(win)

    # animation(ap_list, device_list, ap_animate, device_animate, win)
    
    # events = pygame.event.get()
    # for event in events:
    #     if event.type == pygame.QUIT :
    #         run = False
    #     if event.type == KEYDOWN:
    #         if event.key == K_ESCAPE:
    #             pygame.quit()
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
        if device.ap == None and device.type == 2:
            for ap in ap_list:
                if ap.type == device.type and distance((ap.x, ap.y), (device.x, device.y)) < ap.communication_range:
                    device.detached_time += 1
                    break
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

    # if t % update_timer == 0:
    #     if throughput_cal(ap_list, device_list) > 0.7*initial_throughput_estimation:
    #         print('resource improvement')
    #         for ap in ap_list:
    #             power_adjustment(ap, ap_list)
    #         channel_amplification(ap_list)
    #     else:
    #         print('fairness improvement')
    #         fairness_adjust_version2(ap_list, device_list)

    # if t % update_timer == 0:
    #     if ap_fairness_cal(ap_list) > 0.6:
    #         print('resource improvement')
    #         for ap in ap_list:
    #             power_adjustment(ap, ap_list)
    #         channel_amplification(ap_list)
    #     else:
    #         print('fairness improvement')
    #     fairness_adjust_version2(ap_list, device_list)

    cci_cal(ap_list)
    all_timer_minus_one(device_list, ap_list)
    log_info(ap_list, device_list)

    loss_device_list.append(loss_device_count(device_list))
    num_throughput_under_qos = 0
    for device in device_list:
        if device.type == 1 and device.throughput < throughput_qos:
            num_throughput_under_qos += 1
    throughput_qos_record.append(num_throughput_under_qos)

    ap_fairness_record_interval.append(ap_fairness_cal(ap_list))
    device_fairness_record_interval.append(device_fairness_cal(ap_list))
    total_throughput_record__interval.append(throughput_cal(ap_list, device_list))
    lost_device_record_interval.append(loss_device_count(device_list))
    active_ap_record_interval.append(active_ap_count(ap_list))

    if t % interval == 0:
        ap_fairness, device_fairness, throughput, loss_device, active_ap = calculate_interval_average(ap_fairness_record_interval, device_fairness_record_interval, total_throughput_record__interval, lost_device_record_interval, active_ap_record_interval)
        ap_fairness_record.append(ap_fairness)
        device_fairness_record.append(device_fairness)
        total_throughput_record.append(throughput)
        lost_device_record.append(loss_device)
        active_ap_record.append(active_ap)

        ap_fairness_record_interval.clear()
        device_fairness_record_interval.clear()
        total_throughput_record__interval.clear()
        lost_device_record_interval.clear()
        active_ap_record_interval.clear()

    if t == operation_time:
        total_loss_device = 0
        for i in range(start_time-1, end_time):
            total_loss_device += loss_device_list[i]
        average_loss_device = total_loss_device/(end_time-start_time)
        # print('experiment: other timer =', all_timer , 'search timer = ', d_state_timer_search)
        # print('average loss device = ', average_loss_device)
        for device in device_list:
            if device.type == 2:
                detached_qos_record.append(device.detached_time)
        num_delay_under_qos = 0
        num_delay_under_qos = len(detached_qos_record)
        print(factory_environment)
        print('throughput_qos_record = ', 100-average_of_list(throughput_qos_record))
        print('detached_qos_record = ', average_of_list(detached_qos_record)/operation_time)

        if not os.path.exists('fig'):
            os.mkdir('fig')
        x = np.arange(0, len(ap_fairness_record))
        graph_ap_fairness(x, ap_fairness_record)
        graph_device_fairness(x, device_fairness_record)
        graph_throughput(x, total_throughput_record)
        graph_loss_device(x, lost_device_record)
        graph_active_ap(x, active_ap_record)
        if not os.path.exists('data'):
            os.mkdir('data')
        np.save(f'data/test_ap_fairness_{factory_environment}', ap_fairness_record)
        np.save(f'data/test_device_fairness_{factory_environment}', device_fairness_record)
        np.save(f'data/test_total_throughput_{factory_environment}', total_throughput_record)
        np.save(f'data/test_lost_device_{factory_environment}', lost_device_record)
        np.save(f'data/test_active_ap_{factory_environment}', active_ap_record)
        run = False
#     pygame.display.update()
# pygame.quit()

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