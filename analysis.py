import pandas as pd

# ---------- Load Data ----------

file_path = "results/scenario_sweep_all.csv"

df = pd.read_csv(file_path)

print("\nLoaded Data:")
print(df.head())


# ---------- Compute Metrics ----------

summary = df.groupby(
    ["battery", "driver", "road", "traffic"]
).agg(

    max_speed=("speed", "max"),
    avg_speed=("speed", "mean"),
    final_speed=("speed", "last"),
    min_soc=("soc", "min")

).reset_index()

summary["soc_drop"] = 100 - summary["min_soc"]


# ---------- Print Results ----------

print("\nSummary Table:")
print(summary)


# ---------- Save Summary ----------

summary.to_csv("results/scenario_summary.csv", index=False)

print("\nSaved: results/scenario_summary.csv")