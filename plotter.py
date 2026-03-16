import matplotlib.pyplot as plt


def plot_single_dashboard(data):

    t = data["time"]

    plt.figure(figsize=(10,8))

    plt.subplot(2,2,1)
    plt.plot(t, data["speed"])
    plt.title("Speed vs Time")
    plt.grid(True)

    plt.subplot(2,2,2)
    plt.plot(t, data["soc"])
    plt.title("SOC vs Time")
    plt.grid(True)

    plt.subplot(2,2,3)
    plt.plot(t, data["power"])
    plt.title("Power vs Time")
    plt.grid(True)

    plt.subplot(2,2,4)
    plt.plot(t, data["position"])
    plt.title("Position vs Time")
    plt.grid(True)

    plt.tight_layout()


def plot_comparison(data1, data2):

    t = data1["time"]

    plt.figure(figsize=(10,6))

    plt.subplot(2,1,1)
    plt.plot(t, data1["speed"], label="Healthy Battery")
    plt.plot(t, data2["speed"], label="Aged Battery")
    plt.title("Speed Comparison")
    plt.legend()
    plt.grid(True)

    plt.subplot(2,1,2)
    plt.plot(t, data1["soc"], label="Healthy Battery")
    plt.plot(t, data2["soc"], label="Aged Battery")
    plt.title("SOC Comparison")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()