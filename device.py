from enum import(IntEnum, unique)
import random
from parameter import*
from utils import distance, range_decode
@unique
class State(IntEnum):
    init = 1
    connected = 2
    detached = 3
    handover = 4

class DEVICE:
    def __init__(self, x, y, vx, vy, id, type_device):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.power = 0
        self.channel = 0
        self.id = id
        self.type = type_device
        self.state = State.init
        self.ap = None
        self.throughput = 0
        self.timer = float('inf')

    def move(self):
        while True:
            self.vx = random.randint(-5, 5)
            self.vy = random.randint(-5, 5)
            if boundary(self.x + self.vx, self.y + self.vy):
                self.x = self.x + self.vx
                self.y = self.y + self.vy
                break
            else:
                continue

    def throughput_cal(self, ap):
        return ap.throughput/len(ap.user)

    def state_change(self, ap_list):
        flag = False
        # device move out of range
        if self.ap != None:
            if distance((self.x, self.y), (self.ap.x, self.ap.y)) > range_decode(self.power):
                flag = True
        # device timer expired
        if self.timer == 0:
            flag = True
        # device move to overlapp BSS
        if self.ap != None:
            for ap in ap_list:
                if distance((self.x, self.y), (self.ap.x, self.ap.y)) > distance((self.x, self.y), (ap.x, ap.y)):
                    flag = True
        return flag
        
    def action():
        pass