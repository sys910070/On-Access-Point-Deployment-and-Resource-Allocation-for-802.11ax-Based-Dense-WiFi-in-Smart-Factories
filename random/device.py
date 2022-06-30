import random
from matplotlib.pyplot import disconnect, flag
from parameter import*
from action import*
from utils import*


class DEVICE:
    def __init__(self, x, y, id, type_device):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.power = 0
        self.channel = 0
        self.id = id
        self.type = type_device
        self.state = D_State.random
        self.ap = None
        self.throughput = 0
        self.timer = float('inf')
        self.selected = None
        self.dis = 0
        self.throughput = 0

    def move(self):
        if self.type == 2:
            while True:
                self.vx = random.randint(-5, 5)
                self.vy = random.randint(-5, 5)
                if boundary_no_obstacle(self.x + self.vx, self.y + self.vy):
                # if boundary_symmetric_obstacle(self.x + self.vx, self.y + self.vy):
                # if boundary_asymmetric_obstacle(self.x + self.vx, self.y + self.vy):
                    self.x = self.x + self.vx
                    self.y = self.y + self.vy
                    break

    def dis_cal(self):
        if self.ap == None:
            self.dis = 0
        else:
            self.dis = distance((self.x, self.y), (self.ap.x, self.ap.y))

    def throughput_cal(self):
        if self.ap != None:
            self.throughput = (self.ap.throughput*(T_ULPPDU+T_DLPPDU)/((self.ap.cci+1)*(T_UL+T_DL)))/len(self.ap.user)
            self.ap.user_throughput = self.throughput
        else:
            self.throughput = 0
        
    def action(self, ap_list):
        # for detached device, find active ap first. If no active AP around, open a new idle AP as serving AP and randomly select channel
        if self.ap == None:
            dis = float('inf')
            selected_ap = None
            for ap in ap_list:
                if distance((self.x, self.y), (ap.x, ap.y)) < range_decode(ap.power):
                    if distance((self.x, self.y), (ap.x, ap.y)) < dis and ap.type == self.type and len(ap.user) <= ap.upperbound:
                        dis = distance((self.x, self.y), (ap.x, ap.y))
                        selected_ap = ap
            if selected_ap != None:            
                device_connect(self, selected_ap)
            else:
                dis = float('inf')
                selected_ap = None
                for ap in ap_list:
                    if ap.power == 0:
                        if distance((self.x, self.y), (ap.x, ap.y)) < range_decode(p_max):
                            if distance((self.x, self.y), (ap.x, ap.y)) < dis and ap.type == self.type and len(ap.user) <= ap.upperbound:
                                dis = distance((self.x, self.y), (ap.x, ap.y))
                                selected_ap = ap
                if selected_ap != None:
                    selected_ap.power_change(p_max, ap_list)
                    power_adjustment(selected_ap, ap_list)
                    selected_ap.channel = random.randint(1, 19)
                    device_connect(self, selected_ap)
        else:
            if distance((self.x, self.y), (self.ap.x, self.ap.y)) > range_decode(self.ap.power):
                self.ap.user.remove(self)
                self.ap = None
                for ap in ap_list:
                    dis = float('inf')
                    selected_ap = None
                    if distance((self.x, self.y), (ap.x, ap.y)) < range_decode(ap.power):
                        if distance((self.x, self.y), (ap.x, ap.y)) < dis and ap.type == self.type and len(ap.user) <= ap.upperbound:
                            dis = distance((self.x, self.y), (ap.x, ap.y))
                            selected_ap = ap
                if selected_ap != None:            
                    device_connect(self, selected_ap)
                else:
                    dis = float('inf')
                    selected_ap = None
                    for ap in ap_list:
                        if ap.power == 0:
                            if distance((self.x, self.y), (ap.x, ap.y)) < range_decode(p_max):
                                if distance((self.x, self.y), (ap.x, ap.y)) < dis and ap.type == self.type and len(ap.user) <= ap.upperbound:
                                    dis = distance((self.x, self.y), (ap.x, ap.y))
                                    selected_ap = ap
                    if selected_ap != None:
                        selected_ap.power_change(p_max, ap_list)
                        power_adjustment(selected_ap, ap_list)
                        selected_ap.channel = random.randint(1, 19)
                        device_connect(self, selected_ap)