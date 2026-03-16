import os
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# ---------- Paths ----------
results_folder = "results"
summary_file = os.path.join(results_folder, "scenario_summary.csv")

# ---------- Load Data ----------
df = pd.read_csv(summary_file)

print("\nLoaded summary data:")
print(df.head())

# ---------- Figure 1: Max Speed by Driver Style ----------
plt.figure(figsize=(10, 6))

for battery in ["healthy", "aged"]:
    subset = df[df["battery"] == battery]
    grouped = subset.groupby("driver")["max_speed"].mean()
    plt.plot(grouped.index, grouped.values, marker="o", label=battery.capitalize())

plt.title("Average Max Speed by Driver Style")
plt.xlabel("Driver Style")
plt.ylabel("Average Max Speed (m/s)")
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(results_folder, "figure5_driver_vs_max_speed.png"), dpi=300)

# ---------- Figure 2: SOC Drop by Driver Style ----------
plt.figure(figsize=(10, 6))

for battery in ["healthy", "aged"]:
    subset = df[df["battery"] == battery]
    grouped = subset.groupby("driver")["soc_drop"].mean()
    plt.plot(grouped.index, grouped.values, marker="o", label=battery.capitalize())

plt.title("Average SOC Drop by Driver Style")
plt.xlabel("Driver Style")
plt.ylabel("Average SOC Drop (%)")
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(results_folder, "figure6_driver_vs_soc_drop.png"), dpi=300)

# ---------- Figure 3: Road Impact on Final Speed ----------
plt.figure(figsize=(10, 6))

for road in ["flat", "uphill"]:
    subset = df[df["road"] == road]
    grouped = subset.groupby("battery")["final_speed"].mean()
    plt.plot(grouped.index, grouped.values, marker="o", label=road.capitalize())

plt.title("Road Type Impact on Final Speed")
plt.xlabel("Battery")
plt.ylabel("Average Final Speed (m/s)")
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(results_folder, "figure7_road_impact_final_speed.png"), dpi=300)

# ---------- Figure 4: Traffic Impact on SOC Drop ----------
plt.figure(figsize=(10, 6))

for traffic in ["light", "heavy"]:
    subset = df[df["traffic"] == traffic]
    grouped = subset.groupby("battery")["soc_drop"].mean()
    plt.plot(grouped.index, grouped.values, marker="o", label=traffic.capitalize())

plt.title("Traffic Impact on SOC Drop")
plt.xlabel("Battery")
plt.ylabel("Average SOC Drop (%)")
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(results_folder, "figure8_traffic_impact_soc_drop.png"), dpi=300)

# ---------- Figure 5: Battery Comparison for Max Speed ----------
plt.figure(figsize=(10, 6))

battery_group = df.groupby("battery")["max_speed"].mean()
plt.bar(battery_group.index, battery_group.values)

plt.title("Battery Health Impact on Max Speed")
plt.xlabel("Battery State")
plt.ylabel("Average Max Speed (m/s)")
plt.grid(True, axis="y")
plt.savefig(os.path.join(results_folder, "figure9_battery_max_speed_bar.png"), dpi=300)

# ---------- Figure 6: Top 10 Worst Scenarios by SOC Drop ----------
plt.figure(figsize=(14, 7))

df["scenario"] = (
    df["battery"] + " | " +
    df["driver"] + " | " +
    df["road"] + " | " +
    df["traffic"]
)

top10 = df.sort_values("soc_drop", ascending=False).head(10)

plt.barh(top10["scenario"], top10["soc_drop"])
plt.gca().invert_yaxis()

plt.title("Top 10 Scenarios with Highest SOC Drop")
plt.xlabel("SOC Drop (%)")
plt.ylabel("Scenario")
plt.grid(True, axis="x")
plt.tight_layout()
plt.savefig(os.path.join(results_folder, "figure10_top10_soc_drop.png"), dpi=300)

plt.show()