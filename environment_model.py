import math
import config
from driver_model import Driver

class Environment:
    def __init__(self, road_type="flat", traffic_level="light"):
        self.road_type = road_type.lower()
        self.traffic_level = traffic_level.lower()

    def get_slope_angle_deg(self):
        if self.road_type == "flat":
            return 0.0
        elif self.road_type == "uphill":
            return 5.0
        else:
            return 0.0

    def get_traffic_resistance(self):
        if self.traffic_level == "light":
            return 50.0
        elif self.traffic_level == "heavy":
            return 200.0
        else:
            return 50.0

    def get_slope_force(self):
        angle_deg = self.get_slope_angle_deg()
        angle_rad = math.radians(angle_deg)
        return config.mass * config.g * math.sin(angle_rad)
    
    
    
    
    
    
    
    
    #import matplotlib
#matplotlib.use('TkAgg')


#driver = Driver(mode="eco")                # eco / normal / aggressive
driver = Driver(mode="normal")              # eco / normal / aggressive
#driver = Driver(mode="aggressive")         # eco / normal / aggressive

#env = Environment(road_type="flat", traffic_level="light")   # flat/uphill + light/heavy   test1
#env = Environment(road_type="uphill", traffic_level="light")   # flat/uphill + light/heavy test2
#env = Environment(road_type="flat", traffic_level="heavy")   # flat/uphill + light/heavy   test3
env = Environment(road_type="uphill", traffic_level="heavy")   # flat/uphill + light/heavy  test4