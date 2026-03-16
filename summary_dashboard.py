import os
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle

# ---------- Paths ----------

results_folder = "results"
summary_file = os.path.join(results_folder, "scenario_summary.csv")

# ---------- Load Data ----------

df = pd.read_csv(summary_file)

print("\nSummary data loaded")
print(df.head())

# ---------- Prepare Data ----------

driver_speed = df.groupby(["battery", "driver"])["max_speed"].mean().unstack(0)

driver_soc = df.groupby(["battery", "driver"])["soc_drop"].mean().unstack(0)

road_speed = df.groupby(["road", "battery"])["final_speed"].mean().unstack(1)

traffic_soc = df.groupby(["traffic", "battery"])["soc_drop"].mean().unstack(1)

battery_speed = df.groupby("battery")["max_speed"].mean()

top10 = df.sort_values("soc_drop", ascending=False).head(10).copy()
top10["scenario"] = (
    top10["battery"] + " | " +
    top10["driver"] + " | " +
    top10["road"] + " | " +
    top10["traffic"]
)

# ---------- Dashboard 1: Existing Summary Dashboard ----------

fig, axes = plt.subplots(3, 2, figsize=(16, 12))

# 1 Driver vs Speed
ax = axes[0, 0]
driver_speed.plot(ax=ax)
ax.set_title("Driver Style vs Max Speed")
ax.set_ylabel("Speed (m/s)")
ax.grid(True)

# 2 Driver vs SOC
ax = axes[0, 1]
driver_soc.plot(ax=ax)
ax.set_title("Driver Style vs SOC Drop")
ax.set_ylabel("SOC Drop (%)")
ax.grid(True)

# 3 Battery impact
ax = axes[1, 0]
battery_speed.plot(kind="bar", ax=ax)
ax.set_title("Battery Health Impact on Speed")
ax.set_ylabel("Max Speed (m/s)")
ax.grid(True)

# 4 Road impact
ax = axes[1, 1]
road_speed.plot(ax=ax)
ax.set_title("Road Type Impact")
ax.set_ylabel("Final Speed (m/s)")
ax.grid(True)

# 5 Traffic impact
ax = axes[2, 0]
traffic_soc.plot(ax=ax)
ax.set_title("Traffic Impact on SOC Drop")
ax.set_ylabel("SOC Drop (%)")
ax.grid(True)

# 6 Worst scenarios
ax = axes[2, 1]
ax.barh(top10["scenario"], top10["soc_drop"])
ax.invert_yaxis()
ax.set_title("Worst Scenarios (SOC Drop)")
ax.set_xlabel("SOC Drop (%)")

plt.suptitle("EV Digital Twin - Summary Dashboard", fontsize=18)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(results_folder, "EV_summary_dashboard.png"), dpi=300)

# ---------- Prepare KPI Values for New Dashboard ----------

max_speed_overall = df["max_speed"].max()
avg_speed_overall = df["avg_speed"].mean()
max_soc_drop = df["soc_drop"].max()
avg_soc_drop = df["soc_drop"].mean()

best_scenario_row = df.sort_values("soc_drop", ascending=True).iloc[0]
worst_scenario_row = df.sort_values("soc_drop", ascending=False).iloc[0]

best_scenario = (
    f'{best_scenario_row["battery"]} | '
    f'{best_scenario_row["driver"]} | '
    f'{best_scenario_row["road"]} | '
    f'{best_scenario_row["traffic"]}'
)

worst_scenario = (
    f'{worst_scenario_row["battery"]} | '
    f'{worst_scenario_row["driver"]} | '
    f'{worst_scenario_row["road"]} | '
    f'{worst_scenario_row["traffic"]}'
)

healthy_avg_speed = df[df["battery"] == "healthy"]["max_speed"].mean()
aged_avg_speed = df[df["battery"] == "aged"]["max_speed"].mean()
battery_gap_percent = ((healthy_avg_speed - aged_avg_speed) / healthy_avg_speed) * 100

cost_breakdown = df.groupby("driver")["soc_drop"].mean()

# ---------- Dashboard 2: KPI Style Dashboard ----------

fig2 = plt.figure(figsize=(18, 10))
gs = fig2.add_gridspec(3, 4, height_ratios=[1.1, 1.2, 1.8], hspace=0.5, wspace=0.35)

fig2.suptitle("EV Digital Twin - KPI Dashboard", fontsize=20, fontweight="bold")

# ----- KPI cards -----
card_titles = [
    "Max Speed",
    "Average Speed",
    "Max SOC Drop",
    "Battery Performance Gap"
]

card_values = [
    f"{max_speed_overall:.2f} m/s",
    f"{avg_speed_overall:.2f} m/s",
    f"{max_soc_drop:.2f} %",
    f"{battery_gap_percent:.1f} %"
]

for i in range(4):
    ax = fig2.add_subplot(gs[0, i])
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_facecolor("#f2f2f2")
    ax.text(0.05, 0.70, card_titles[i], fontsize=12, fontweight="bold", transform=ax.transAxes)
    ax.text(0.05, 0.30, card_values[i], fontsize=18, color="#1f4e79", transform=ax.transAxes)

# ----- Line chart: driver speed -----
ax1 = fig2.add_subplot(gs[1, 0:2])
driver_speed.plot(ax=ax1, marker="o")
ax1.set_title("Driver Style vs Max Speed")
ax1.set_ylabel("Speed (m/s)")
ax1.grid(True)

# ----- Line chart: driver SOC -----
ax2 = fig2.add_subplot(gs[1, 2:4])
driver_soc.plot(ax=ax2, marker="o")
ax2.set_title("Driver Style vs SOC Drop")
ax2.set_ylabel("SOC Drop (%)")
ax2.grid(True)

# ----- Large left panel: worst scenarios -----
ax3 = fig2.add_subplot(gs[2, 0:2])
ax3.barh(top10["scenario"], top10["soc_drop"])
ax3.invert_yaxis()
ax3.set_title("Top 10 Worst Scenarios by SOC Drop")
ax3.set_xlabel("SOC Drop (%)")
ax3.grid(True, axis="x")

# ----- Donut chart: average SOC drop by driver -----
ax4 = fig2.add_subplot(gs[2, 2])
colors = ["#4CAF50", "#2196F3", "#FF9800"]
ax4.pie(
    cost_breakdown.values,
    labels=cost_breakdown.index,
    startangle=90,
    colors=colors,
    wedgeprops=dict(width=0.42)
)
ax4.set_title("Average SOC Drop Share by Driver")

# ----- Info panel -----
ax5 = fig2.add_subplot(gs[2, 3])
ax5.set_xticks([])
ax5.set_yticks([])
for spine in ax5.spines.values():
    spine.set_visible(False)
ax5.set_facecolor("#f7f7f7")

ax5.text(0.02, 0.92, "Best Scenario", fontsize=12, fontweight="bold", transform=ax5.transAxes)
ax5.text(0.02, 0.82, best_scenario, fontsize=10, wrap=True, transform=ax5.transAxes)

ax5.text(0.02, 0.62, "Worst Scenario", fontsize=12, fontweight="bold", transform=ax5.transAxes)
ax5.text(0.02, 0.52, worst_scenario, fontsize=10, wrap=True, transform=ax5.transAxes)

ax5.text(0.02, 0.32, "Average SOC Drop", fontsize=12, fontweight="bold", transform=ax5.transAxes)
ax5.text(0.02, 0.24, f"{avg_soc_drop:.2f} %", fontsize=14, color="#b22222", transform=ax5.transAxes)

#plt.tight_layout(rect=[0, 0, 1, 0.95])
fig2.subplots_adjust(top=0.90, left=0.05, right=0.97, bottom=0.05, hspace=0.55, wspace=0.35)
plt.savefig(os.path.join(results_folder, "EV_kpi_dashboard.png"), dpi=300)

# ---------- Dashboard 3: Scenario KPI Cards Dashboard ----------

scenario_df = df.copy()

scenario_df["scenario_title"] = (
    scenario_df["battery"].str.capitalize() + " | " +
    scenario_df["driver"].str.capitalize() + " | " +
    scenario_df["road"].str.capitalize() + " | " +
    scenario_df["traffic"].str.capitalize()
)

# مرتب‌سازی برای خوانایی بهتر
driver_order_map = {"eco": 0, "normal": 1, "aggressive": 2}
road_order_map = {"flat": 0, "uphill": 1}
traffic_order_map = {"light": 0, "heavy": 1}
battery_order_map = {"healthy": 0, "aged": 1}

scenario_df["battery_order"] = scenario_df["battery"].map(battery_order_map)
scenario_df["driver_order"] = scenario_df["driver"].map(driver_order_map)
scenario_df["road_order"] = scenario_df["road"].map(road_order_map)
scenario_df["traffic_order"] = scenario_df["traffic"].map(traffic_order_map)

scenario_df = scenario_df.sort_values(
    by=["battery_order", "driver_order", "road_order", "traffic_order"]
).reset_index(drop=True)

# 24 سناریو = 6 سطر × 4 ستون
n_cards = len(scenario_df)
ncols = 4
nrows = (n_cards + ncols - 1) // ncols

fig3, axes = plt.subplots(nrows, ncols, figsize=(18, 16))
fig3.suptitle("EV Digital Twin - Scenario KPI Cards", fontsize=20, fontweight="bold")

axes = axes.flatten()

for i, ax in enumerate(axes):
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    if i < n_cards:
        row = scenario_df.iloc[i]

        # رنگ کارت بر اساس نوع باتری
        if row["battery"] == "healthy":
            face_color = "#eef6ff"
            border_color = "#4a90e2"
        else:
            face_color = "#fff3e8"
            border_color = "#f39c12"

        ax.add_patch(
            Rectangle(
                (0.02, 0.02), 0.96, 0.96,
                transform=ax.transAxes,
                facecolor=face_color,
                edgecolor=border_color,
                linewidth=2
            )
        )

        ax.text(
            0.05, 0.84,
            row["scenario_title"],
            fontsize=9,
            fontweight="bold",
            transform=ax.transAxes,
            wrap=True
        )

        ax.text(
            0.05, 0.62,
            f"Max Speed: {row['max_speed']:.2f} m/s",
            fontsize=9,
            color="#1f4e79",
            transform=ax.transAxes
        )

        ax.text(
            0.05, 0.45,
            f"Avg Speed: {row['avg_speed']:.2f} m/s",
            fontsize=9,
            color="#1565c0",
            transform=ax.transAxes
        )

        ax.text(
            0.05, 0.28,
            f"Final Speed: {row['final_speed']:.2f} m/s",
            fontsize=9,
            color="#2e7d32",
            transform=ax.transAxes
        )

        ax.text(
            0.05, 0.14,
            f"SOC Drop: {row['soc_drop']:.2f} %",
            fontsize=9,
            color="#b22222",
            transform=ax.transAxes
        )
    else:
        ax.axis("off")

#plt.tight_layout(rect=[0, 0, 1, 0.96])
fig3.subplots_adjust(top=0.93, left=0.03, right=0.97, bottom=0.03, hspace=0.30, wspace=0.18)
plt.savefig(os.path.join(results_folder, "EV_scenario_kpi_cards.png"), dpi=300)

#plt.show()
plt.show(block=False)
input("Press Enter to close plots...")