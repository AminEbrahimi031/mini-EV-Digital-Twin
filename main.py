import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import os
import csv

from simulation_engine import run_simulation
from plotter import plot_single_dashboard, plot_comparison


# ---------- Create Results Folder ----------

results_folder = "results"

if not os.path.exists(results_folder):
    os.makedirs(results_folder)


# ---------- Helper Functions ----------

def save_dict_to_csv(filename, data_dict):
    keys = list(data_dict.keys())
    rows = zip(*[data_dict[key] for key in keys])

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        writer.writerows(rows)


def save_comparison_to_csv(filename, data1, data2):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "time",
            "speed_healthy", "soc_healthy", "power_healthy",
            "speed_aged", "soc_aged", "power_aged"
        ])

        for i in range(len(data1["time"])):
            writer.writerow([
                data1["time"][i],
                data1["speed"][i], data1["soc"][i], data1["power"][i],
                data2["speed"][i], data2["soc"][i], data2["power"][i]
            ])


def save_scenario_results_to_csv(filename, scenario_results):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "battery", "driver", "road", "traffic",
            "time", "speed", "soc"
        ])

        for result in scenario_results:
            for i in range(len(result["time"])):
                writer.writerow([
                    result["battery"],
                    result["driver"],
                    result["road"],
                    result["traffic"],
                    result["time"][i],
                    result["speed"][i],
                    result["soc"][i]
                ])


# ---------- Phase 6 ----------

data_single = run_simulation(
    driver_mode="normal",
    road_type="uphill",
    traffic_level="heavy",
    battery_state="healthy",
    verbose=True
)

plot_single_dashboard(data_single)
plt.gcf().savefig(f"{results_folder}/figure1_vehicle_behavior.png", dpi=300)

save_dict_to_csv(
    f"{results_folder}/phase6_single_simulation.csv",
    data_single
)


# ---------- Phase 7 ----------

data_healthy = run_simulation(
    driver_mode="normal",
    road_type="uphill",
    traffic_level="heavy",
    battery_state="healthy",
    verbose=False
)

data_aged = run_simulation(
    driver_mode="normal",
    road_type="uphill",
    traffic_level="heavy",
    battery_state="aged",
    verbose=False
)

plot_comparison(data_healthy, data_aged)
plt.gcf().savefig(f"{results_folder}/figure2_battery_comparison.png", dpi=300)

save_comparison_to_csv(
    f"{results_folder}/phase7_battery_comparison.csv",
    data_healthy,
    data_aged
)


# ---------- Scenario Sweep Better Visualization ----------

driver_modes = ["eco", "normal", "aggressive"]
road_types = ["flat", "uphill"]
traffic_levels = ["light", "heavy"]
battery_states = ["healthy", "aged"]

scenario_results = []

scenario_duration = 10
dt = 0.02
num_steps = int(scenario_duration / dt)

for battery_state in battery_states:
    for driver_mode in driver_modes:
        for road_type in road_types:
            for traffic_level in traffic_levels:

                print("\n==============================")
                print("Scenario:", battery_state, driver_mode, road_type, traffic_level)
                print("==============================")

                data = run_simulation(
                    driver_mode=driver_mode,
                    road_type=road_type,
                    traffic_level=traffic_level,
                    battery_state=battery_state,
                    num_steps=num_steps,
                    dt=dt,
                    verbose=False
                )

                scenario_results.append({
                    "battery": battery_state,
                    "driver": driver_mode,
                    "road": road_type,
                    "traffic": traffic_level,
                    "label": f"{road_type}-{traffic_level}",
                    "time": data["time"],
                    "speed": data["speed"],
                    "soc": data["soc"]
                })


def plot_battery_dashboard(results, battery_name):
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))

    driver_order = ["eco", "normal", "aggressive"]
    env_order = [
        ("flat", "light"),
        ("flat", "heavy"),
        ("uphill", "light"),
        ("uphill", "heavy")
    ]

    for row, driver in enumerate(driver_order):
        driver_results = [r for r in results if r["driver"] == driver]

        ax_speed = axes[row, 0]
        for road, traffic in env_order:
            for r in driver_results:
                if r["road"] == road and r["traffic"] == traffic:
                    ax_speed.plot(r["time"], r["speed"], label=f"{road}-{traffic}")

        ax_speed.set_title(f"{driver.capitalize()} - Speed")
        ax_speed.set_xlabel("Time (s)")
        ax_speed.set_ylabel("Speed (m/s)")
        ax_speed.grid(True)
        ax_speed.legend(fontsize=8)

        ax_soc = axes[row, 1]
        for road, traffic in env_order:
            for r in driver_results:
                if r["road"] == road and r["traffic"] == traffic:
                    ax_soc.plot(r["time"], r["soc"], label=f"{road}-{traffic}")

        ax_soc.set_title(f"{driver.capitalize()} - SOC")
        ax_soc.set_xlabel("Time (s)")
        ax_soc.set_ylabel("SOC (%)")
        ax_soc.grid(True)
        ax_soc.legend(fontsize=8)

    fig.suptitle(f"Scenario Sweep Dashboard - {battery_name.capitalize()} Battery", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.97])


healthy_results = [r for r in scenario_results if r["battery"] == "healthy"]
aged_results = [r for r in scenario_results if r["battery"] == "aged"]

plot_battery_dashboard(healthy_results, "healthy")
plt.gcf().savefig(f"{results_folder}/figure3_healthy_scenarios.png", dpi=300)

plot_battery_dashboard(aged_results, "aged")
plt.gcf().savefig(f"{results_folder}/figure4_aged_scenarios.png", dpi=300)

save_scenario_results_to_csv(
    f"{results_folder}/scenario_sweep_all.csv",
    scenario_results
)

plt.show()



#نحوه اجرای کد ها 
#1  python main.py
#2  python analysis.py
#3  python advanced_visualization.py
#4  python summary_dashboard.py
#5  python multi_animation.py