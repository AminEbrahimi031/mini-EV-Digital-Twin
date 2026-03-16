from vehicle_model import Vehicle
from battery_model import Battery
from driver_model import Driver
from environment_model import Environment


def run_simulation(driver_mode="normal",
                   road_type="uphill",
                   traffic_level="heavy",
                   battery_state="healthy",
                   num_steps=200,
                   dt=0.1,
                   verbose=True):

    car = Vehicle()
    driver = Driver(mode=driver_mode)
    env = Environment(road_type=road_type, traffic_level=traffic_level)
    battery = Battery(health_state=battery_state)

    time_data = []
    speed_data = []
    position_data = []
    acc_data = []
    soc_data = []
    power_data = []
    energy_data = []

    for step in range(num_steps):

        current_time = step * dt
        throttle = driver.get_throttle()

        slope_force = env.get_slope_force()
        traffic_resistance = env.get_traffic_resistance()
        health_factor = battery.get_health_factor()

        speed, position, acc, motor_force = car.update(
            throttle,
            health_factor=health_factor,
            slope_force=slope_force,
            traffic_resistance=traffic_resistance
        )

        soc, power_w, energy_used = battery.update(motor_force, speed)

        if verbose:
            print(
                "Mode:", driver.mode,
                "Road:", env.road_type,
                "Traffic:", env.traffic_level,
                "Battery:", battery.health_state,
                "Speed:", round(speed,2),
                "Position:", round(position,2),
                "Acceleration:", round(acc,2),
                "SOC:", round(soc,2),
                "Power(W):", round(power_w,2),
                "Energy(kWh):", round(energy_used,5)
            )

        time_data.append(current_time)
        speed_data.append(speed)
        position_data.append(position)
        acc_data.append(acc)
        soc_data.append(soc)
        power_data.append(power_w)
        energy_data.append(energy_used)

    return {
        "time": time_data,
        "speed": speed_data,
        "position": position_data,
        "acc": acc_data,
        "soc": soc_data,
        "power": power_data,
        "energy": energy_data
    }