import ckt24_buses
import matplotlib.patches as mpatches
import matplotlib.patches as mmarkers
import pylab
from functions import bus_name_lists
import sqlite3

def plot_zones():

    ckt24_buses.ckt24_plot()

    bus1p, bus2p, bus3p = bus_name_lists()

    # Take bus coordinates max and min
    xmax = 11746421.02
    xmin = 11746421.02
    ymax = 3714090.755
    ymin = 3714090.755


    for bus in [bus1p, bus2p, bus3p]:
        for row in bus:
            if ymax < float(row[2]):
                ymax = float(row[2])
            if ymin > float(row[2]):
                ymin = float(row[2])
            if xmax < float(row[1]):
                xmax = float(row[1])
            if xmin > float(row[1]):
                xmin = float(row[1])

    x_step = (xmax - xmin)/5
    y_step = (ymax - ymin)/5

    def lineplot(p1,p2):
        x = [p1[0],p2[0]]
        y = [p1[1],p2[1]]
        pylab.plot(x,y,color='k',linewidth=2)

    # zone 1 x axis
    lineplot([xmin,ymin+1.3*y_step],[xmin+x_step,ymin+1.3*y_step])
    lineplot([xmin+x_step,ymin+1.43*y_step],[xmin+2*x_step,ymin+1.43*y_step])

    # zone 2 x axis
    lineplot([xmin+2*x_step,ymin+2*y_step],[xmin+3.72*x_step,ymin+2*y_step])

    # zone 2 y axis
    lineplot([xmin+2*x_step,ymin],[xmin+2*x_step,ymin+2*y_step])

    # zone 3 y axis
    lineplot([xmin+3.72*x_step,ymin],[xmin+3.72*x_step,ymin+5*y_step])

    # zone 5 x axias
    lineplot([xmin+1.6*x_step,ymin+2.85*y_step],
    [xmin+3.72*x_step,ymin+2.85*y_step])

    # zones 1 and 6 y axis
    lineplot([xmin+x_step,ymin+1.3*y_step],[xmin+x_step,ymin+2.1*y_step])

    # zone 6 inclined line
    lineplot([xmin+x_step,ymin+2.1*y_step],[xmin+1.6*x_step,ymin+2.85*y_step])
    m = ((ymin+2.85*y_step) - (ymin+2.1*y_step)) / \
    ((xmin+1.6*x_step) - (xmin+x_step))
    b = (ymin+2.1*y_step) - (m*(xmin+x_step))

    # zone 6 "knee"
    lineplot([xmin+1.6*x_step,ymin+2.85*y_step],
    [xmin+1.6*x_step,ymin+3.2*y_step])
    lineplot([xmin+1.6*x_step,ymin+3.2*y_step],
    [xmin+1.25*x_step,ymin+3.2*y_step])
    lineplot([xmin+1.25*x_step,ymin+3.2*y_step],
    [xmin+1.25*x_step,ymin+5*y_step])

    # borders
    lineplot([xmin,ymin],[xmax,ymin])
    lineplot([xmin,ymin],[xmin,ymax])
    lineplot([xmax,ymin],[xmax,ymax])
    lineplot([xmin,ymax],[xmax,ymax])

    substation, = pylab.plot([11735514.42],[3709460.816],'k^',
    markersize=10, label='Substation')
    blue_patch = mpatches.Patch(color='blue', label='Three-phase lines')
    green_patch = mpatches.Patch(color='green', label='Two-phase lines')
    red_patch = mpatches.Patch(color='red', label='One-phase lines')
    # pylab.legend(handles=[substation, blue_patch, green_patch, red_patch])
    pylab.title("ckt24 separated in zones for machine learning fault location")
    pylab.show()

def zones2database():

    # Insert zones number label for each bus
    def bus_insert_zone(buslist,xmax,xmin,x_step,ymax,ymin,y_step):
        for i in range(len(buslist)):

            buslist[i][1] = float(buslist[i][1])
            buslist[i][2] = float(buslist[i][2])

            # Zone 1
            if xmin<=buslist[i][1]<xmin+x_step:
                if ymin<=buslist[i][2]<=ymin+1.3*y_step:
                    buslist[i].insert(3,'z1')
            if xmin+x_step<=buslist[i][1]<=xmin+2*x_step:
                if ymin<=buslist[i][2]<=ymin+1.43*y_step:
                    buslist[i].insert(3,'z1')
            # Zone 2
            if xmin+2*x_step<buslist[i][1]<xmin+3.72*x_step:
                if ymin<=buslist[i][2]<=ymin+2*y_step:
                    buslist[i].insert(3,'z2')
            # Zone 3
            if xmin+3.72*x_step<=buslist[i][1]<=xmax:
                buslist[i].insert(3,'z3')
            # Zone 4
            if xmin+x_step<=buslist[i][1]<=xmin+1.6*x_step:
                if ymin+1.43*y_step<=buslist[i][2]<=m*buslist[i][1]+b:
                    buslist[i].insert(3,'z4')
            if xmin+1.6*x_step<buslist[i][1]<=xmin+2*x_step:
                if ymin+1.43*y_step<=buslist[i][2]<=ymin+2.85*y_step:
                    buslist[i].insert(3,'z4')
            if xmin+2*x_step<buslist[i][1]<=xmin+3.72*x_step:
                if ymin+2*y_step<buslist[i][2]<=ymin+2.85*y_step:
                    buslist[i].insert(3,'z4')
            # Zone 5
            if xmin+1.25*x_step<=buslist[i][1]<xmin+1.6*x_step:
                if ymin+3.2*y_step<=buslist[i][2]<=ymax:
                    buslist[i].insert(3,'z5')
            if xmin+1.6*x_step<=buslist[i][1]<xmin+3.72*x_step:
                if ymin+2.85*y_step<=buslist[i][2]<=ymax:
                    buslist[i].insert(3,'z5')
            # Zone 6
            if xmin<=buslist[i][1]<xmin+x_step:
                if ymin+1.3*y_step<buslist[i][2]<=ymax:
                    buslist[i].insert(3,'z6')
            if xmin+x_step<=buslist[i][1]<xmin+1.25*x_step:
                if m*buslist[i][1]+b<buslist[i][2]<=ymax:
                    buslist[i].insert(3,'z6')
            if xmin+1.25*x_step<=buslist[i][1]<xmin+1.6*x_step:
                if m*buslist[i][1]+b<buslist[i][2]<=ymin+3.2*y_step:
                    buslist[i].insert(3,'z6')
        return buslist

    bus1p = bus_insert_zone(bus1p,xmax,xmin,x_step,ymax,ymin,y_step)
    bus2p = bus_insert_zone(bus2p,xmax,xmin,x_step,ymax,ymin,y_step)
    bus3p = bus_insert_zone(bus3p,xmax,xmin,x_step,ymax,ymin,y_step)


    conn = sqlite3.connect('database_faultlocation_1PV.db')
    c = conn.cursor()
    c.execute('ALTER TABLE PV1_faultloc_db ADD zone TEXT')
    for buslist in [bus1p,bus2p,bus3p]:
        for i in range(len(buslist)):
            c.execute('UPDATE PV1_faultloc_db SET zone=? WHERE bus=?',
            (buslist[i][3], buslist[i][0]))
    conn.commit()

if __name__ == "__main__":

    print(
    """
This code plots ckt24 division in 6 different geographic regions and adds their
label to a fault in the databases.
    """
    )
    plot_zones()
    zones2database()
