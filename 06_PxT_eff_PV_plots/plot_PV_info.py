import matplotlib.pyplot as plt

def main():
    plt.plot([0,25,75,100],[1.2,1,.8,.6])
    plt.title("Reduction of mpp in function of T")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("mpp (pu)")
    plt.show()

    plt.plot([0.1,0.2,0.4,1],[0.86,.9,.93,.97])
    plt.title("Inverter efficiency curve")
    plt.xlabel("Nominal Inverter Power (pu)")
    plt.ylabel("Efficiency (pu)")
    plt.show()


if __name__ == "__main__":
    main()
