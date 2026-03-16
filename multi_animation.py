import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from simulation_engine import run_simulation


# ---------- Scenario List ----------
scenarios = [
    {"battery": "healthy", "driver": "eco",        "road": "flat",   "traffic": "light"},
    {"battery": "healthy", "driver": "normal",     "road": "uphill", "traffic": "heavy"},
    {"battery": "aged",    "driver": "normal",     "road": "flat",   "traffic": "heavy"},
    {"battery": "aged",    "driver": "aggressive", "road": "uphill", "traffic": "light"},
]

# ---------- Simulation Settings ----------
num_steps = 120
dt = 0.08

# ---------- Run all scenarios ----------
all_data = []

for sc in scenarios:
    data = run_simulation(
        driver_mode=sc["driver"],
        road_type=sc["road"],
        traffic_level=sc["traffic"],
        battery_state=sc["battery"],
        num_steps=num_steps,
        dt=dt,
        verbose=False
    )

    all_data.append({
        "scenario": sc,
        "data": data
    })

# ---------- Figure ----------
fig = plt.figure(figsize=(15, 8))
gs = fig.add_gridspec(2, 2, height_ratios=[2, 1.2], hspace=0.35, wspace=0.25)

ax_anim = fig.add_subplot(gs[0, :])
ax_speed = fig.add_subplot(gs[1, 0])
ax_soc = fig.add_subplot(gs[1, 1])

fig.suptitle("Mini EV Digital Twin - Multi Scenario Animation", fontsize=18, fontweight="bold")

# ---------- Animation Area ----------
ax_anim.set_xlim(0, 100)
ax_anim.set_ylim(0, 22)
ax_anim.set_xticks([])
ax_anim.set_yticks([])
ax_anim.set_title("Vehicle Motion")

# road line
road_line, = ax_anim.plot([0, 100], [5, 5], linewidth=3)

# car
car = Rectangle((0, 5.5), 8, 3, fill=True)
ax_anim.add_patch(car)

wheel1, = ax_anim.plot([], [], marker="o", markersize=10, linestyle="")
wheel2, = ax_anim.plot([], [], marker="o", markersize=10, linestyle="")

info_text = ax_anim.text(
    2, 20,
    "",
    fontsize=11,
    verticalalignment="top",
    bbox=dict(boxstyle="round", alpha=0.15)
)

scenario_text = ax_anim.text(
    70, 20,
    "",
    fontsize=11,
    verticalalignment="top",
    bbox=dict(boxstyle="round", alpha=0.15)
)

# ---------- Speed Plot ----------
ax_speed.set_title("Speed")
ax_speed.set_xlabel("Time (s)")
ax_speed.set_ylabel("Speed (m/s)")
ax_speed.grid(True)

speed_line, = ax_speed.plot([], [], linewidth=2)
speed_point, = ax_speed.plot([], [], marker="o", linestyle="")

# ---------- SOC Plot ----------
ax_soc.set_title("SOC")
ax_soc.set_xlabel("Time (s)")
ax_soc.set_ylabel("SOC (%)")
ax_soc.grid(True)

soc_line, = ax_soc.plot([], [], linewidth=2)
soc_point, = ax_soc.plot([], [], marker="o", linestyle="")

# ---------- Global frame count ----------
frames_per_scenario = num_steps
total_frames = frames_per_scenario * len(all_data)

# ---------- Init ----------
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

# ---------- Update ----------
def update(global_frame):
    scenario_index = global_frame // frames_per_scenario
    local_frame = global_frame % frames_per_scenario

    current = all_data[scenario_index]
    sc = current["scenario"]
    data = current["data"]

    time_data = data["time"]
    speed_data = data["speed"]
    soc_data = data["soc"]
    power_data = data["power"]
    position_data = data["position"]

    # dynamic road appearance
    ax_anim.lines.clear()
    ax_anim.plot([0, 100], [5, 5], linewidth=3)
    if sc["road"] == "uphill":
        ax_anim.plot([0, 100], [5, 9], linestyle="--", linewidth=1)

    # normalize position
    max_pos = max(position_data) if max(position_data) > 0 else 1.0
    x = position_data[local_frame] / max_pos * 80

    # ---------- move car on road ----------
    if sc["road"] == "uphill":
        road_y = 5 + (4 / 100) * x   # slope from y=5 to y=9
    else:
        road_y = 5

    car.set_xy((x, road_y + 0.5))
    wheel1.set_data([x + 1.5], [road_y + 0.3])
    wheel2.set_data([x + 6.5], [road_y + 0.3])

    # update axis limits per scenario
    ax_speed.set_xlim(min(time_data), max(time_data))
    ax_speed.set_ylim(0, max(speed_data) * 1.1 if max(speed_data) > 0 else 1)

    ax_soc.set_xlim(min(time_data), max(time_data))
    ax_soc.set_ylim(min(soc_data) - 0.2, max(soc_data) + 0.2)

    # update speed plot
    speed_line.set_data(time_data[:local_frame + 1], speed_data[:local_frame + 1])
    speed_point.set_data([time_data[local_frame]], [speed_data[local_frame]])

    # update soc plot
    soc_line.set_data(time_data[:local_frame + 1], soc_data[:local_frame + 1])
    soc_point.set_data([time_data[local_frame]], [soc_data[local_frame]])

    # info text
    info_text.set_text(
        f"Time: {time_data[local_frame]:.2f} s\n"
        f"Position: {position_data[local_frame]:.2f} m\n"
        f"Speed: {speed_data[local_frame]:.2f} m/s\n"
        f"SOC: {soc_data[local_frame]:.2f} %\n"
        f"Power: {power_data[local_frame]:.2f} W"
    )

    scenario_text.set_text(
        f"Scenario {scenario_index + 1}/{len(all_data)}\n"
        f"Battery: {sc['battery']}\n"
        f"Driver: {sc['driver']}\n"
        f"Road: {sc['road']}\n"
        f"Traffic: {sc['traffic']}"
    )

    return car, wheel1, wheel2, speed_line, speed_point, soc_line, soc_point, info_text, scenario_text

# ---------- Animation ----------
ani = FuncAnimation(
    fig,
    update,
    frames=total_frames,
    init_func=init,
    interval=70,
    blit=False,
    repeat=False
)

plt.show()