import config


class Battery:
    def __init__(self, health_state="healthy"):
        self.health_state = health_state.lower()
        self.soc = config.initial_soc
        self.power_w = 0.0
        self.energy_used_kwh = 0.0

    def get_health_factor(self):
        if self.health_state == "healthy":
            return 1.0
        elif self.health_state == "aged":
            return 0.85
        else:
            return 1.0

    def get_efficiency(self):
        if self.health_state == "healthy":
            return 0.90
        elif self.health_state == "aged":
            return 0.80
        else:
            return 0.90

    def update(self, motor_force, speed):
        mechanical_power = motor_force * speed

        if mechanical_power < 0:
            mechanical_power = 0

        efficiency = self.get_efficiency()
        self.power_w = mechanical_power / efficiency

        energy_used_kwh_step = self.power_w * config.dt / 3600 / 1000
        self.energy_used_kwh += energy_used_kwh_step

        soc_drop = (energy_used_kwh_step / config.battery_capacity_kwh) * 100
        self.soc -= soc_drop

        if self.soc < 0:
            self.soc = 0

        return self.soc, self.power_w, self.energy_used_kwh