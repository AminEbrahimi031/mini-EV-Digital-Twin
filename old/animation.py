import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
import numpy as np

from simulation_engine import run_simulation


# ---------- Scenario Selection ----------
driver_mode = "normal"       # eco / normal / aggressive
road_type = "uphill"         # flat / uphill
traffic_level = "heavy"      # light / heavy
battery_state = "healthy"    # healthy / aged

# ---------- Run Simulation ----------
data = run_simulation(
    driver_mode=driver_mode,
    road_type=road_type,
    traffic_level=traffic_level,
    battery_state=battery_state,
    num_steps=200,
    dt=0.1,
    verbose=False
)

time_data = data["time"]
speed_data = data["speed"]
position_data = data["position"]
soc_data = data["soc"]
power_data = data["power"]

# ---------- Normalize Road Display ----------
max_position = max(position_data) if max(position_data) > 0 else 1.0
display_x = [p / max_position * 80 for p in position_data]

# ---------- Create Figure ----------
fig = plt.figure(figsize=(14, 8))
gs = fig.add_gridspec(2, 2, height_ratios=[2, 1.3], hspace=0.35, wspace=0.25)

ax_anim = fig.add_subplot(gs[0, :])
ax_speed = fig.add_subplot(gs[1, 0])
ax_soc = fig.add_subplot(gs[1, 1])

fig.suptitle("Mini EV Digital Twin Animation", fontsize=18, fontweight="bold")

# ---------- Animation Area ----------
ax_anim.set_xlim(0, 100)
ax_anim.set_ylim(0, 20)
ax_anim.set_title("Vehicle Motion")
ax_anim.set_xticks([])
ax_anim.set_yticks([])

# Road
ax_anim.plot([0, 100], [5, 5], linewidth=3)

# Optional slope visual
if road_type == "uphill":
    ax_anim.plot([0, 100], [5, 9], linestyle="--", linewidth=1)

# Car body
car = Rectangle((0, 5.5), 8, 3, angle=0, fill=True)
ax_anim.add_patch(car)

# Wheels
wheel1, = ax_anim.plot([], [], marker="o", markersize=10, linestyle="")
wheel2, = ax_anim.plot([], [], marker="o", markersize=10, linestyle="")

# Text boxes
info_text = ax_anim.text(
    2, 17,
    "",
    fontsize=11,
    verticalalignment="top",
    bbox=dict(boxstyle="round", alpha=0.15)
)

scenario_text = ax_anim.text(
    70, 17,
    "",
    fontsize=10,
    verticalalignment="top",
    bbox=dict(boxstyle="round", alpha=0.15)
)

# ---------- Speed Plot ----------
ax_speed.set_title("Speed")
ax_speed.set_xlabel("Time (s)")
ax_speed.set_ylabel("Speed (m/s)")
ax_speed.set_xlim(min(time_data), max(time_data))
ax_speed.set_ylim(0, max(speed_data) * 1.1 if max(speed_data) > 0 else 1)
ax_speed.grid(True)

speed_line, = ax_speed.plot([], [], linewidth=2)
speed_point, = ax_speed.plot([], [], marker="o", linestyle="")

# ---------- SOC Plot ----------
ax_soc.set_title("SOC")
ax_soc.set_xlabel("Time (s)")
ax_soc.set_ylabel("SOC (%)")
ax_soc.set_xlim(min(time_data), max(time_data))
ax_soc.set_ylim(min(soc_data) - 0.2, max(soc_data) + 0.2)
ax_soc.grid(True)

soc_line, = ax_soc.plot([], [], linewidth=2)
soc_point, = ax_soc.plot([], [], marker="o", linestyle="")

# ---------- Init Function ----------
def init():
    car.set_xy((0, 5.5))
    wheel1.set_data([], [])
    wheel2.set_data([], [])
    speed_line.set_data([], [])
    speed_point.set_data([], [])
    soc_line.set_data([], [])
    soc_point.set_data([], [])
    info_text.set_text("")
    scenario_text.set_text("")
    return car, wheel1, wheel2, speed_line, speed_point, soc_line, soc_point, info_text, scenario_text

# ---------- Update Function ----------
def update(frame):
    x = display_x[frame]

    # Car position
    car.set_xy((x, 5.5))
    wheel1.set_data([x + 1.5], [5.3])
    wheel2.set_data([x + 6.5], [5.3])

    # Update speed plot
    speed_line.set_data(time_data[:frame + 1], speed_data[:frame + 1])
    speed_point.set_data([time_data[frame]], [speed_data[frame]])

    # Update SOC plot
    soc_line.set_data(time_data[:frame + 1], soc_data[:frame + 1])
    soc_point.set_data([time_data[frame]], [soc_data[frame]])

    # Text info
    info_text.set_text(
        f"Time: {time_data[frame]:.1f} s\n"
        f"Position: {position_data[frame]:.2f} m\n"
        f"Speed: {speed_data[frame]:.2f} m/s\n"
        f"SOC: {soc_data[frame]:.2f} %\n"
        f"Power: {power_data[frame]:.2f} W"
    )

    scenario_text.set_text(
        f"Driver: {driver_mode}\n"
        f"Road: {road_type}\n"
        f"Traffic: {traffic_level}\n"
        f"Battery: {battery_state}"
    )

    return car, wheel1, wheel2, speed_line, speed_point, soc_line, soc_point, info_text, scenario_text

# ---------- Animation ----------
ani = FuncAnimation(
    fig,
    update,
    frames=len(time_data),
    init_func=init,
    interval=80,
    blit=False,
    repeat=False
)

plt.show()