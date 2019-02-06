from functions import bus_name_lists, line_name_lists, V, C, P
import os
import time
import win32com.client

def main():

    # Get directory of .py file
    dir = os.path.dirname(os.path.abspath(__file__))

    # Make lists with bus names

    # Bus_1p_list
    bus1p_list = bus_name_lists()[0]
    for i in range(len(bus1p_list)):
        if i == 0:
            bus1p_listn = [bus1p_list[0][0]]
        else:
            bus1p_listn.append(bus1p_list[i][0])

    # Bus_2p_list
    bus2p_list = bus_name_lists()[1]
    for i in range(len(bus2p_list)):
        if i == 0:
            bus2p_listn = [bus2p_list[0][0]]
        else:
            bus2p_listn.append(bus2p_list[i][0])

    # Bus_3p_list
    bus3p_list = bus_name_lists()[2]
    for i in range(len(bus3p_list)):
        if i == 0:
            bus3p_listn = [bus3p_list[0][0]]
        else:
            bus3p_listn.append(bus3p_list[i][0])

    # Start the DSS
    dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")
    if dssObj.Start(0) == False:
        sys.exit("DSS failed to start")
    else:
        #Assign a variable to each of the interfaces
        dssText = dssObj.Text
        dssCircuit = dssObj.ActiveCircuit
        dssSolution = dssCircuit.Solution

    # Clear the DSS
    dssObj.ClearAll()

    # Load circuit
    dssText.Command = "Compile "+dir+"\\ckt24\\ckt24.dss"

    # Min and max pu voltage in bus of the circuit in hours and seasons
    min_pu_list = []
    max_pu_list = []

    for season in ["Spring","Summer","Autumn","Winter"]:

        # Solve circuit in different loadshapes, season based
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

        # Set and calculate voltage bases
        dssText.Command = "Redirect "+dir+"\\ckt24\\ckt24_vbases.dss"

        hours = ["9","10","11","12","13","14","15","16","17"]

        for hour in hours:

            min_pu = 1.05
            max_pu = 0

            # Solve circuit
            dssText.Command = "Solve mode=daily number=1 hour="+hour

            for bus in bus1p_listn:
                # print(V(bus,dssCircuit))
                # print(bus)
                if min_pu > V(bus,dssCircuit)[0]:
                    min_pu = V(bus,dssCircuit)[0]
                if max_pu < V(bus,dssCircuit)[0]:
                    max_pu = V(bus,dssCircuit)[0]

            for bus in bus2p_listn:
                # print(V(bus,dssCircuit))
                # print(bus)
                for i in [0,2]:
                    if min_pu > V(bus,dssCircuit)[i]:
                        min_pu = V(bus,dssCircuit)[i]
                    if max_pu < V(bus,dssCircuit)[i]:
                        max_pu = V(bus,dssCircuit)[i]

            for bus in bus3p_listn:
                # print(V(bus,dssCircuit))
                # print(bus)
                for i in [0,2,4]:
                    if min_pu > V(bus,dssCircuit)[i]:
                        min_pu = V(bus,dssCircuit)[i]
                    if max_pu < V(bus,dssCircuit)[i]:
                        max_pu = V(bus,dssCircuit)[i]

            min_pu_list.append(min_pu)
            max_pu_list.append(max_pu)

    print("min pu voltage:")
    print(min(min_pu_list))
    print()
    print("max pu voltage:")
    print(max(max_pu_list))

if __name__ == "__main__":

    print(
    """
This code runs simulations for ckt24 throughout the day and returns
the highest and lowest pu voltage value registered in a bus.
    """
    )

    main()
