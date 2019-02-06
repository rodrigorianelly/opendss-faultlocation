import matplotlib.pyplot as plt
import matplotlib.collections as mcoll
import linepack
import numpy as np

def V(bus, dssCircuit):
    dssCircuit.SetActiveBus(bus)
    voltages = dssCircuit.ActiveBus.puVmagAngle
    return voltages

def N(bus, dssCircuit):
    dssCircuit.SetActiveBus(bus)
    nodes = dssCircuit.ActiveBus.Nodes
    return nodes

def ckt24_plot(l1,l2,l3,phase,norm,dssCircuit):

    flag = 0
    if phase == 1:
        vflag = 0
    elif phase == 2:
        vflag = 2
    elif phase == 3:
        vflag = 4

    # Plot Substation
    substation, = plt.plot([11735514.42],[3709460.816], color="sienna",
    marker="^", markersize=10, linestyle="None", label='Substation')
    plt.legend(handles=[substation])

    # Print 1p lines with color according to pu voltage in a specific phase
    for i in range(len(l1)):
        if len(l1[i])==8:
            if l1[i][3] != phase:
                linepack.plotline([float(l1[i][4]),float(l1[i][5])],
                [float(l1[i][6]),float(l1[i][7])],'k')
            else:
                if flag == 1:
                    if len(N(l1[i][1],dssCircuit)) == 3:
                        v1 = vflag
                    else:
                        v1 = 0
                    if len(N(l1[i][2],dssCircuit)) == 3:
                        v2 = vflag
                    else:
                        v2 = 0

                    if len(N(l1[i][1],dssCircuit)) == 2:
                        if N(l1[i][1],dssCircuit)[0] == phase:
                            v1 = 0
                        if N(l1[i][1],dssCircuit)[1] == phase:
                            v1 = 2

                    if len(N(l1[i][2],dssCircuit)) == 2:
                        if N(l1[i][2],dssCircuit)[0] == phase:
                            v2 = 0
                        if N(l1[i][2],dssCircuit)[1] == phase:
                            v2 = 2

                    linepack.multicolored_lines([float(l1[i][4]),
                    float(l1[i][5])],[float(l1[i][6]),float(l1[i][7])],
                    V(l1[i][1],dssCircuit)[v1],V(l1[i][2],dssCircuit)[v2],norm)


                elif flag == 0:

                    flag = 1

                    if len(N(l1[i][1],dssCircuit)) == 3:
                        v1 = vflag
                    else:
                        v1 = 0
                    if len(N(l1[i][2],dssCircuit)) == 3:
                        v2 = vflag
                    else:
                        v2 = 0
                    if len(N(l1[i][1],dssCircuit)) == 2:
                        if N(l1[i][1],dssCircuit)[0] == phase:
                            v1 = 0
                        if N(l1[i][1],dssCircuit)[1] == phase:
                            v1 = 2
                    if len(N(l1[i][2],dssCircuit)) == 2:
                        if N(l1[i][2],dssCircuit)[0] == phase:
                            v2 = 0
                        if N(l1[i][2],dssCircuit)[1] == phase:
                            v2 = 2

                    linepack.multicolored_lines([float(l1[i][4]),
                    float(l1[i][5])],[float(l1[i][6]),float(l1[i][7])],
                    V(l1[i][1],dssCircuit)[v1],V(l1[i][2],dssCircuit)[v2],norm,
                    colorbar_flag=1)


    # Print 2p lines with color according to pu voltage in a specific phase
    for i in range(len(l2)):
        if len(l2[i])==8:
            if (l2[i][3][0] != phase) and (l2[i][3][1] != phase):
                linepack.plotline([float(l2[i][4]),float(l2[i][5])],
                [float(l2[i][6]),float(l2[i][7])],'k')
            elif l2[i][3][0] == phase:
                if len(N(l2[i][1],dssCircuit)) == 3:
                    v1 = vflag
                else:
                    v1 = 0
                if len(N(l2[i][2],dssCircuit)) == 3:
                    v2 = vflag
                else:
                    v2 = 0
                linepack.multicolored_lines([float(l2[i][4]),
                float(l2[i][5])],[float(l2[i][6]),float(l2[i][7])],
                V(l2[i][1],dssCircuit)[v1],V(l2[i][2],dssCircuit)[v2],norm)


            elif l2[i][3][1] == phase:
                if len(N(l2[i][1],dssCircuit)) == 3:
                    v1 = vflag
                else:
                    v1 = 2
                if len(N(l2[i][2],dssCircuit)) == 3:
                    v2 = vflag
                else:
                    v2 = 2
                linepack.multicolored_lines([float(l2[i][4]),
                float(l2[i][5])],[float(l2[i][6]),float(l2[i][7])],
                V(l2[i][1],dssCircuit)[v1],V(l2[i][2],dssCircuit)[v2],norm)


    # Print 3p lines with color according to pu voltage in a specific phase
    for i in range(len(l3)):
        if len(l3[i])==7:
            linepack.multicolored_lines([float(l3[i][3]),float(l3[i][4])],
            [float(l3[i][5]),float(l3[i][6])],V(l3[i][1],dssCircuit)[vflag],
            V(l3[i][2],dssCircuit)[vflag],norm)

    plt.axis("off")
