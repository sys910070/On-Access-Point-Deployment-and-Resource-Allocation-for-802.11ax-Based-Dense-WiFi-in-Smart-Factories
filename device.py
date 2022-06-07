from enum import(IntEnum, unique)
import random
from parameter import*
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

    def state_change():
        pass