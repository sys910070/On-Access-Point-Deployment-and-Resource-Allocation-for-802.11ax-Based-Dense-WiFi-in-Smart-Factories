from enum import(IntEnum, unique)
from parameter import*
from utils import*

@unique
class State(IntEnum):
    init = 1
    active = 2
    underpopulated = 3
    idle = 4

class AP:
    def __init__(self, x, y, id, type_ap):
        self.x = x
        self.y = y
        self.power = 0
        self.channel = 0
        self.user = []
        self.id = id
        self.type = type_ap
        self.timer = 0
        self.state = State.init
        self.cci = 0
        self.neighbor = []
        self.interference_range = 0
        self.communication_range = 0
        self.throughput = 0
        self.lowerbound = 0
        self.upperbound = 0

    def power_change(self, power):
        self.power = power
        self.interference_range = range_interference(power)
        self.communication_range = range_decode(power)

    # define neighbor ap(power!=0) as is there exist ap in interference range
    def add_neighbor_ap(self, ap_list):
        for ap in ap_list:
            if ap not in self.neighbor and self.interference_range + ap.interference_range >= distance((self.x, self.y), (ap.x, ap.y)) and ap != self and ap.power!=0 and self.power!=0:
                self.neighbor.append(ap)

    def adduser(self, users):
        if users not in self.user:
            self.user.append(users)

    def cci_calculation(self):
        self.cci = 0
        for neighbor in self.neighbor:
            for ch in ch_dic[neighbor.channel]:
                if ch == self.channel:
                    self.cci = self.cci + 1

    def check_state_change(self, t, timer, user, lowerbound):
        if timer == 0 or t%30 == 0 or len(user)< lowerbound: 
            return True

    def action():
        pass
    
    def update():
        pass

