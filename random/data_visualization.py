# this file is for all data, including animation, log file, performance graph
import pygame
import matplotlib.pyplot as plt
from parameter import*
import logging
import os

# log file
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

def log_info(ap_list, device_list):
    # open a log file
    ap_logger = setup_logger('AP', 'AP.txt')                    # open file
    device_logger = setup_logger('Device', 'Device.txt')        # open file
    ap_logger.info('id, users, power, state, timer')
    for ap in ap_list:   
        if ap.power!= 0 and len(ap.neighbor_decode)!=0:
            ap_logger.info(f'{ap.id}, {ap.power}, {[neighbor.id for neighbor in ap.neighbor_decode]}, {[user.id for user in ap.user]}, {ap.state.name}')
        else:
            ap_logger.info(f'{ap.id}, {ap.power}, {None}, {None}, {ap.user_throughput}, {None}, {None}, {ap.state.name}')

    device_logger.info('id, ap, power, state, timer, x, y')
    for device in device_list:
        if device.ap != None:
            device_logger.info(f'{device.id}, {device.ap.id}, {device.power}, {device.state.name}, {device.throughput}')
        else:
            device_logger.info(f'{device.id}, {None}, {device.power}, {device.state.name}, {device.timer}')

#graph
def graph_device(ap_list, device_list):
    plt.title('simulation display')
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
   
    for ap in ap_list:
        if ap.channel == 0:
            continue
        elif ch_id_to_bw[ap.channel] == 20:
            plt.plot(ap.y, ap.x,'ro', color = 'lime') # AP
            plt.text(ap.y+1, ap.x+1, ap.id, color='lime')
        elif ch_id_to_bw[ap.channel] == 40:
            plt.plot(ap.y, ap.x,'ro', color = 'red') # AP
            plt.text(ap.y+1, ap.x+1, ap.id, color='red')
        elif ch_id_to_bw[ap.channel] == 80:
            plt.plot(ap.y, ap.x,'ro', color = 'blue') # AP
            plt.text(ap.y+1, ap.x+1, ap.id, color='blue')
        elif ch_id_to_bw[ap.channel] == 160:
            plt.plot(ap.y, ap.x,'ro', color = 'purple') # AP
            plt.text(ap.y+1, ap.x+1, ap.id, color='purple')
    for device in device_list:
        if device.ap != None:
            plt.plot(device.y, device.x, 'ro', color = 'black') # device
            plt.text(device.y+1, device.x+1, device.id, color='black')
        else:
            plt.plot(device.y, device.x, 'ro', color = 'dimgrey') # device
            plt.text(device.y+1, device.x+1, device.id, color='dimgrey')
    plt.axis([0, factory_width, 0, factory_length])
    plt.show()

def graph_fairness(t, fairness):
    plt.figure(figsize=(16,12))
    plt.title('fairness index')
    plt.xlabel('time')
    plt.ylabel('fairness')
    plt.plot(t, fairness, '-o')
    plt.xlim(0, operation_time+1)
    plt.ylim(0, 1)
    plt.savefig('fig/fairness without optimize')
    # plt.show()

def graph_throughput(t, total_throughput_device):
    plt.figure(figsize=(16,12))
    plt.title('total throughput')
    plt.xlabel('time')
    plt.ylabel('fairness')
    plt.plot(t, total_throughput_device, '-o')
    plt.savefig('fig/total throughput without optimize')
    # plt.show()

def graph_loss_device(t, lost_device):
    plt.figure(figsize=(16,12))
    plt.title('loss device')
    plt.xlabel('time')
    plt.ylabel('loss_device')
    plt.plot(t, lost_device, '-o')
    plt.savefig('fig/loss device number without optimize')
    # plt.show()

# animation
def animation(ap_list, device_list, ap_animate, device_animate, win):
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
        pygame.draw.circle(win, (255, 160, 122), (ap.y, ap.x), ap.communication_range, 1)
        text, textRect = txt(ap)
        win.blit(text, textRect)

# animation text
def txt(obj):
    font = pygame.font.Font('freesansbold.ttf', 10)
    text = font.render(str(obj.id), True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (obj.y+10, obj.x-10)
    return text, textRect