import random
from matplotlib.pyplot import disconnect, flag
from parameter import*
from action import*
from utils import*

random.seed(1126)
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
        self.gv = 0 # 1 for RGV, 2 for OHT, 3 for AGV, 4 for human
        self.destination_dis = 0
        self.direction = 0
        self.detached_time = 0

    def move(self):
        if self.type == Type.delay:
            if factory_environment == 'real_factory_layout':
                mobility_real_factory(self)
            else:
                mobility(self)

    def dis_cal(self):
        if self.ap == None:
            self.dis = 0
        else:
            self.dis = distance((self.x, self.y), (self.ap.x, self.ap.y))

    def throughput_cal(self):
        if self.ap != None:
            self.throughput = self.ap.throughput/len(self.ap.user)
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
                    channel_list = []
                    for i in range(1, 20):
                        channel_list.append(i)
                    channel_list.reverse()
                    temp_channel = 0
                    temp_cci = float('inf')
                    for channel in channel_list:
                        ap.channel = channel
                        temp_cci_cal(ap_list)
                        if selected_ap.cci < temp_cci:
                            temp_cci = ap.cci
                            temp_channel = channel
                    selected_ap.channel = temp_channel
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
                        selected_ap.channel = random.randint(1, 19)
                        device_connect(self, selected_ap)
                    else:
                        self.power = 0
                        self.channel = 0