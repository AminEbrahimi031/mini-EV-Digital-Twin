# Mini EV Twin 🚗⚡

Python-Based Digital Twin for Electric Vehicle Simulation

---

## Project Overview

Mini EV Twin is a Python-based simulation project that demonstrates a simplified **Digital Twin concept for Electric Vehicles (EVs)**.

The system models how an electric vehicle behaves under different conditions such as:

* Driver style
* Road slope
* Traffic resistance
* Battery health

The project performs multi-scenario simulations and produces engineering dashboards, KPI visualizations, scenario analysis, and animated vehicle behavior.

This project was built as a self-initiated **portfolio engineering project** combining:

* EV simulation
* data analysis
* visualization
* digital twin concepts

---

## Main Features

* EV longitudinal motion simulation
* Driver behavior modeling (**Eco / Normal / Aggressive**)
* Battery state-of-charge (SOC) simulation
* Traffic resistance modeling
* Road slope modeling
* Battery health modeling (**Healthy / Aged**)
* Scenario-based simulation analysis
* CSV data export for data analysis
* Advanced engineering visualization
* KPI dashboards
* Multi-scenario animated vehicle simulation

---

## Technologies Used

### Programming Language

* Python

### Python Libraries

* numpy
* pandas
* matplotlib
* csv
* os

### Development Tools

* VS Code
* GitHub

---

## Project Structure

```text
Mini EV Twin
│
├── results
│
├── assets
│
├── main.py
├── simulation_engine.py
├── vehicle_model.py
├── battery_model.py
├── driver_model.py
├── environment_model.py
│
├── analysis.py
├── advanced_visualization.py
├── summary_dashboard.py
├── multi_animation.py
│
├── plotter.py
├── config.py
│
└── README.md
```

---

## Project Visualization

The simulation generates multiple engineering dashboards and scenario analysis plots.

---

### Vehicle Behavior Simulation

Speed, battery SOC, power consumption and position evolution during a simulation run.

![Vehicle Behavior](results/figure1_vehicle_behavior.png)

---

### Battery Health Comparison

Comparison between **Healthy** and **Aged** battery performance.

![Battery Comparison](results/figure2_battery_comparison.png)

---

### Scenario Sweep – Healthy Battery

Simulation results across different driver styles, road slopes and traffic conditions.

![Healthy Scenarios](results/figure3_healthy_scenarios.png)

---

### Scenario Sweep – Aged Battery

Simulation results for an aged battery under the same scenario combinations.

![Aged Scenarios](results/figure4_aged_scenarios.png)

---

### Driver Style vs Maximum Speed

How driving behavior affects vehicle performance.

![Driver vs Speed](results/figure5_driver_vs_max_speed.png)

---

### Driver Style vs Battery Consumption

Impact of driving behavior on **battery SOC drop**.

![Driver vs SOC](results/figure6_driver_vs_soc_drop.png)

---

### Road Type Impact on Vehicle Speed

Effect of **flat vs uphill roads** on final vehicle speed.

![Road Impact](results/figure7_road_impact_final_speed.png)

---

### Traffic Impact on Battery Consumption

Impact of traffic resistance on battery usage.

![Traffic Impact](results/figure8_traffic_impact_soc_drop.png)

---

### Battery Health Impact on Maximum Speed

Healthy vs aged battery influence on vehicle performance.

![Battery Max Speed](results/figure9_battery_max_speed_bar.png)

---

### Top 10 Worst Scenarios by Battery Consumption

Ranking of the scenarios with the highest SOC drop.

![Top SOC Drop](results/figure10_top10_soc_drop.png)

---

### Summary Dashboard

Overview of all simulation results.

![Summary Dashboard](results/EV_summary_dashboard.png)

---

### KPI Dashboard

Engineering KPI summary of the simulation system.

![KPI Dashboard](results/EV_kpi_dashboard.png)

---

### Scenario KPI Cards

Detailed scenario-level metrics.

![Scenario KPI Cards](results/EV_scenario_kpi_cards.png)

---
## Simulation Animation

Click the preview image below to watch the animated EV digital twin simulation.

[![EV Simulation Demo](assets/animation_preview.png)](demo/ev_simulation_demo.mp4)
---

## Author

Amin Ebrahimi

Background:
Electrical Engineering (Control Systems)

Current field:
Digital Technologies

Areas of interest:

* Electric Vehicles
* Digital Twins
* Simulation
* Mobility Systems
* Data Analysis
