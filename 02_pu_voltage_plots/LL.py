from functions import bus_name_lists, line_name_lists, min_pu_value, V, C
import os
import math
import win32com.client

import ckt24_colorV
import matplotlib.pyplot as plt

def fault_LL(faultbus,faultphases,phases,r,buscoords,l1,l2,l3,dssObj):
    """LL fault simulation in bus and results
    """

    # Get directory of .py file
    dir = os.path.dirname(os.path.abspath(__file__))

    dssText = dssObj.Text
    dssCircuit = dssObj.ActiveCircuit
    dssBus = dssCircuit.ActiveBus

    dssText.Command = "Edit Fault.fault phases=1 bus1="+faultbus \
    +faultphases[0]+" bus2="+faultbus+faultphases[1]+" r="+r

    season = "Summer"

    dssText.Command = "Edit Loadshape.LS_PhaseA" \
    +" mult=(file=LS_PhaseA_"+season+"Day.txt)"
    dssText.Command = "Edit Loadshape.LS_PhaseB" \
    +" mult=(file=LS_PhaseB_"+season+"Day.txt)"
    dssText.Command = "Edit Loadshape.LS_PhaseC" \
    +" mult=(file=LS_PhaseC_"+season+"Day.txt)"
    dssText.Command = "Edit Loadshape.LS_ThreePhase" \
    +" mult=(file=LS_ThreePhase_"+season+"Day.txt)"
    dssText.Command = "Edit Loadshape.Other_Bus_Load" \
    +" mult=(file=Other_Bus_Load_"+season+"Day.txt)"

    hour=15

    dssText.Command = "Redirect "+dir+"\\ckt24_vbases.dss"
    dssText.Command = "Solve mode=daily number=1 hour="+str(hour)

    # Colorbar limits
    norm = [math.floor(min_pu_value(l1,l2,l3,dssCircuit)*10)/10,1.05]

    # Circuit plot

    label = 'Fault at bus %s' % (faultbus)

    ckt24_colorV.ckt24_plot(l1,l2,l3,1,norm,dssCircuit)
    plt.plot(float(buscoords[0]),float(buscoords[1]),'go',markersize=7,
    label=label)
    plt.legend(loc='upper right')
    plt.ylim(3707500,3727500)
    plt.xlim(11730000,11747500)
    plt.axis("off")
    plt.title("Phase A, r=%s ohms" % (r))
    plt.show()

    ckt24_colorV.ckt24_plot(l1,l2,l3,2,norm,dssCircuit)
    plt.plot(float(buscoords[0]),float(buscoords[1]),'go',markersize=7,
    label=label)
    plt.legend(loc='upper right')
    plt.ylim(3707500,3727500)
    plt.xlim(11730000,11747500)
    plt.axis("off")
    plt.title("Phase B, r=%s ohms" % (r))
    plt.show()

    ckt24_colorV.ckt24_plot(l1,l2,l3,3,norm,dssCircuit)
    plt.plot(float(buscoords[0]),float(buscoords[1]),'go',markersize=7,
    label=label)
    plt.legend(loc='upper right')
    plt.ylim(3707500,3727500)
    plt.xlim(11730000,11747500)
    plt.axis("off")
    plt.title("Phase C, r=%s ohms" % (r))
    plt.show()

    return

def main():

    # Get directory of .py file
    dir = os.path.dirname(os.path.abspath(__file__))

    # Buses list
    bus1p_list = bus_name_lists()[0]
    bus2p_list = bus_name_lists()[1]
    bus3p_list = bus_name_lists()[2]

    # Lines list
    l1 = line_name_lists()[0]
    l2 = line_name_lists()[1]
    l3 = line_name_lists()[2]

    # Start the DSS
    dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")
    if dssObj.Start(0) == False:
        sys.exit("DSS failed to start")
    else:
        #Assign a variable to each of the interfaces for easier access
        dssText = dssObj.Text
        dssCircuit = dssObj.ActiveCircuit
        dssSolution = dssCircuit.Solution

    # Clear the DSS
    dssObj.ClearAll()

    # Load circuit
    dssText.Command = "Compile "+dir+"\\ckt24\\ckt24.dss"

    # Initialize fault elements
    dssText.Command = "New Fault.fault"

    # Fault resistance
    r = "05"

    # Print fault in a bus that has 2p
    bus2p = bus2p_list[20]
    phases = ".%d.%d" % (bus2p[3],bus2p[4])
    faultphases = ["."+str(bus2p[3]),"."+str(bus2p[4])]
    fault_LL(bus2p[0],faultphases,phases,r,[bus2p[1],bus2p[2]],
    l1,l2,l3,dssObj)

    # Print fault in a bus that has 3p
    # bus3p = bus3p_list[50]
    # faultphases = [".1",".3"]
    # fault_LL(bus3p[0],faultphases,".1.2.3",r,[bus3p[1],bus3p[2]],
    # l1,l2,l3,dssObj)

if __name__ == "__main__":

    print(
    """
This code plots a pu voltage profile for a LL fault between phases A and C with
a 5 ohms fault resistance.
    """
    )

    main()
