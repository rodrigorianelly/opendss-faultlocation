import functions
import matplotlib.patches as mpatches
import matplotlib.patches as mmarkers
import pylab

def ckt24_plot():

    def plotline(p1,p2,color_):
        x = [p1[0],p2[0]]
        y = [p1[1],p2[1]]
        pylab.plot(x,y,color=color_,linewidth=2)

    l1 = functions.line_name_lists()[0]
    l2 = functions.line_name_lists()[1]
    l3 = functions.line_name_lists()[2]

    for i in range(len(l1)):
        if len(l1[i])==7:
            plotline([float(l1[i][3]),float(l1[i][4])],
            [float(l1[i][5]),float(l1[i][6])],"red")
    for i in range(len(l2)):
        if len(l2[i])==7:
            plotline([float(l2[i][3]),float(l2[i][4])],
            [float(l2[i][5]),float(l2[i][6])],"green")
    for i in range(len(l3)):
        if len(l3[i])==7:
            plotline([float(l3[i][3]),float(l3[i][4])],
            [float(l3[i][5]),float(l3[i][6])],"blue")
    pylab.axis("off")

def plot_no_pv():

    ckt24_plot()
    substation, = pylab.plot([11735514.42],[3709460.816],'k^',
    markersize=10, label='Substation')
    blue_patch = mpatches.Patch(color='blue', label='Three-phase lines')
    green_patch = mpatches.Patch(color='green', label='Two-phase lines')
    red_patch = mpatches.Patch(color='red', label='One-phase lines')
    pylab.legend(handles=[substation, blue_patch, green_patch, red_patch])
    pylab.title("No PV system")
    pylab.show()

def plot_1_pv():

    ckt24_plot()
    substation, = pylab.plot([11735514.42],[3709460.816],'k^',
    markersize=10, label='Substation')
    pvsyst, = pylab.plot([11740622.95],[3714771.12],
    color='orange', marker='s', markersize=10, linestyle='None',
    label='PV System')
    blue_patch = mpatches.Patch(color='blue', label='Three-phase lines')
    green_patch = mpatches.Patch(color='green', label='Two-phase lines')
    red_patch = mpatches.Patch(color='red', label='One-phase lines')
    pylab.legend(handles=[substation, pvsyst, blue_patch, green_patch,
    red_patch])
    pylab.title("1 PV system")
    pylab.show()

def plot_5_pv():

    ckt24_plot()
    substation, = pylab.plot([11735514.42],[3709460.816],'k^',
    markersize=10, label='Substation')
    pvsyst, = pylab.plot(
    [11740361.09,11745683.27,11740622.95,11740594.66,11735219.81],
    [3709237.782,3712746.259,3714771.12,3718243.191,3718067.52],
    color='orange', marker='s', markersize=10, linestyle='None',
    label='PV System')
    blue_patch = mpatches.Patch(color='blue', label='Three-phase lines')
    green_patch = mpatches.Patch(color='green', label='Two-phase lines')
    red_patch = mpatches.Patch(color='red', label='One-phase lines')
    pylab.legend(handles=[substation, pvsyst, blue_patch, green_patch,
    red_patch])
    pylab.title("5 PV systems")
    pylab.show()

def plot_many_pv():

    ckt24_plot()
    substation, = pylab.plot([11735514.42],[3709460.816],'k^',
    markersize=10, label='Substation')
    transformer_list = functions.transformer_list()
    x = []
    y = []
    for i in range(len(transformer_list)):
        x.append(float(transformer_list[i][3]))
        y.append(float(transformer_list[i][4]))
    pvsyst, = pylab.plot(x, y, color='orange', marker='s', markersize=3,
    linestyle='None', label='PV System')
    blue_patch = mpatches.Patch(color='blue', label='Three-phase lines')
    green_patch = mpatches.Patch(color='green', label='Two-phase lines')
    red_patch = mpatches.Patch(color='red', label='One-phase lines')
    pylab.legend(handles=[substation, pvsyst, blue_patch, green_patch,
    red_patch])
    pylab.title("339 PV systems")
    pylab.show()

if __name__ == "__main__":

    print(
    """
This code plots ckt24 showing the phases of the lines and where the
PV systems will be installed
    """
    )

    plot_no_pv()
    plot_1_pv()
    plot_5_pv()
    plot_many_pv()
