from enum import(IntEnum, unique)
from parameter import*
from utils import distance



@unique
class State(IntEnum):
    init = 1
    active = 2
    underpopulated = 3
    idle = 4

class AP:
    def __init__(self, x, y, capacity, id, type_ap):
        self.x = x
        self.y = y
        self.power = 0
        self.channel = 0
        self.user = []
        self.capacity = capacity
        self.id = id
        self.type = type_ap
        self.timer = 0
        self.state = State.init
        self.cci = 0
        self.neighbor = []
        self.interference_range = 0
        self.communication_range = 0

    def power_change(self, power):
        self.power = power
        self.interference_range = 10**((power+GTX+GRX-P_REF-CHI-THETA_INTERFERENCE)/(10*ETA))
        self.communication_range = 10**((power+GTX+GRX-P_REF-CHI-THETA_DECODE)/(10*ETA))

    # define neighbor ap(power!=0) as is there exist ap in interference range
    def add_neighbor_ap(self, ap_list):
        for aps in ap_list:
            for ap in aps:
                if self.interference_range + ap.interference_range >= distance((self.x, self.y), (ap.x, ap.y)) and ap != self and ap.power and self.power:
                    self.neighbor.append(ap.id)

    def adduser(self, user):
        self.user.append(user)

    def cci_calculation(self, id_to_ap):
        self.cci = 0
        for neighbor_id in self.neighbor:
            if id_to_ap[neighbor_id].channel == self.channel:
                self.cci = self.cci + 1

    def check_state_change(self, t, timer, user, lowerbound):
        if timer == 0 or t%30 == 0 or len(user)< lowerbound: 
            return True

    def action():
        pass
    
    def update():
        pass

