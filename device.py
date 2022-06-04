from enum import(IntEnum, unique)
import random
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
        self.ap = 0
        self.throughput = 0

    def move(self):
        self.vx = random.randint(-10, 10)
        self.vy = random.randint(-10, 10)
        self.x = self.x + self.vx
        self.y = self.y + self.vy

    def throughput_cal(self, ap):
        return ap.throughput/len(ap.user)

    def state_change():
        pass