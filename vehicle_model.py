import config


class Vehicle:

    def __init__(self):
        self.speed = 0.0
        self.position = 0.0
        self.acceleration = 0.0
        self.motor_force = 0.0

    def update(self, throttle, health_factor=1.0, slope_force=0.0, traffic_resistance=0.0):

        # Effective motor force after battery health effect
        self.motor_force = throttle * config.max_force * health_factor

        # Drag force
        F_drag = config.drag_coefficient * self.speed ** 2

        # Rolling resistance
        F_roll = config.rolling_resistance

        # Net force
        F_net = self.motor_force - F_drag - F_roll - slope_force - traffic_resistance

        # Acceleration
        self.acceleration = F_net / config.mass

        # Update speed
        self.speed = self.speed + self.acceleration * config.dt

        if self.speed < 0:
            self.speed = 0

        # Update position
        self.position = self.position + self.speed * config.dt

        return self.speed, self.position, self.acceleration, self.motor_force