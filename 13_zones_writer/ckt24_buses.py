import pylab
from functions import line_name_lists

def plotline(p1,p2,color_):
    x = [p1[0],p2[0]]
    y = [p1[1],p2[1]]
    pylab.plot(x,y,color=color_,linewidth=2)

def ckt24_plot():
    l1 = line_name_lists()[0]
    l2 = line_name_lists()[1]
    l3 = line_name_lists()[2]

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
