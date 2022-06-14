import numpy as np
import random
import logging
import pygame
from pygame.locals import *
from itertools import chain
from ap import AP 
from device import DEVICE
from information_center import*
from utils import* 
from parameter import*

# create two log file for APs and devices
formatter = logging.Formatter('%(levelname)s %(message)s')
def setup_logger(name, log_file, level=logging.DEBUG):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file, mode='w')        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers = []
    logger.addHandler(handler)

    return logger

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

# initialization
init(ap_list, device_list) 
power_allocation(ap_list)
channel_allocation(ap_list)
channel_enhancement(ap_list)
device_resource(device_list)

 ####################test####################

pygame.init()

win = pygame.display.set_mode((factory_width*5, factory_length*5))
pygame.display.set_caption("Simulation")
clock = pygame.time.Clock()
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
        self.user = ap.user
        self.id = ap.id
        self.type = ap.type
        self.timer = ap.timer
        self.state = ap.state
        self.cci = ap.cci
        self.neighbor = ap.neighbor
        self.interference_range = ap.interference_range*5
        self.communication_range = ap.communication_range*5
        self.throughput = ap.throughput
        self.lowerbound = ap.lowerbound
        self.upperbound = ap.upperbound

device_animate = []
ap_animate = []
for device in device_list:
    device_animate.append(Device_animate(device)) 
for ap in ap_list:
    ap_animate.append(AP_animate(ap))

fullscreen = False

#main loop
run = True
while run :
    clock.tick(27)
    keys = pygame.key.get_pressed()

    win.fill(WHITE)
    for device in device_animate:
        pygame.draw.circle(win, BLACK, (device.y, device.x), 3)    
    for ap in ap_animate:
        pygame.draw.circle(win, LIME, (ap.y, ap.x), 3) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            run = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
        if keys[pygame.K_SPACE]:
            for device in device_animate:
                device.move()

    pygame.display.update()

pygame.quit()

# # simulation starts
# while t!=operation_time:
#     # open a log file
#     ap_logger = setup_logger('AP', 'AP.txt')                    # open file
#     device_logger = setup_logger('Device', 'Device.txt')        # open file
#     ap_logger.info('id, users, power, state, timer')
#     for ap in ap_list:    
#         ap_logger.info(f'{ap.id}, {[user.id for user in ap.user]}, {ap.power}, {ap.state.name}, {ap.timer}')
#     device_logger.info('id, ap, power, state, timer')
#     for device in device_list:
#         if device.ap != None:
#             device_logger.info(f'{device.id}, {device.ap.id}, {device.power}, {device.state.name}, {device.timer}')
#         else:
#             device_logger.info(f'{device.id}, {None}, {device.power}, {device.state.name}, {device.timer}')
#     # graph
#     graph_device(ap_list, device_list)
#     count = 0
#     for device in device_list:
#         if device.ap == None:
#             count += 1
#     print(count)

#     for device in device_list:
#         device.move()
#     for device in device_list:
#         flag_device, device_next_state = device.state_change(ap_list)
#         if flag_device:
#             device.action(device_next_state, ap_list)
#     for ap in ap_list:
#         flag_ap, ap_next_state = ap.state_change(ap_list, device_list)
#         if flag_ap:
#             ap.action(ap_next_state, ap_list, device_list)
#     for device in device_list:
#         device.timer -= 1
#     for ap in ap_list:
#         ap.timer -= 1
#     t += 1

    #################### Animation ########################

# animation initialization
# pygame.init()
# screen = pygame.display.set_mode((factory_width, factory_length))
# clock = pygame.time.Clock()
# pygame.display.set_caption('simulation display')

# class Device_animate(pygame.sprite.Sprite):
#     def __init__(self, device):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.Surface(10, 20)
#         self.image.fill(LIME)
#         self.rect = self.image.get_rect() # 框框
#         self.rect.center = (device.x, device.y)
#         self.vx = device.vx
#         self.vy = device.vy
    
#     def update(self):
#         key_pressed = pygame.key.get_pressed()
#         if key_pressed[pygame.K_RIGHT]:
#             self.rect.centerx += self.vx
#             self.rect.centery += self.vy

# class AP_animate(pygame.sprite.Sprite):
#     def __init__(self, ap):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.Surface((30, 20))
#         self.image.fill(LIME)
#         self.rect = self.image.get_rect()
#         self.rect.center = (ap.x, ap.y)

# all_sprites = pygame.sprite.Group()
# for device in device_list:
#     all_sprites.add(Device_animate(device))

# for ap in ap_list:
#     all_sprites.add(AP_animate(ap))

# running = True
# while running:
#     clock.tick(60) # control FPS
#     # input
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.Keydown:
#             if pygame.mouse.get_pressed() and pygame.mouse.getpos() == device:
#                 pass
#     # update
#     all_sprites.update()

#     # display
#     screen.fill((255, 255, 255))
#     all_sprites.draw(screen)
#     pygame.display.update()

# pygame.quit()