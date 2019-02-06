from functions import bus_name_lists, line_name_lists, transformer_list, V, C, P
import os
import time
import win32com.client

def main():

    print(
    """
This code checks if it is possible to install small photovoltaic generation
systems of 15 kW in half of the 1p transformers (339 PVSystems) according to pu
voltage variation in all buses, current in lines and power in transformers.
    """
    )

    buses_criteria_pu_var()
    # lines_criteria()
    # transformers_criteria()

def buses_criteria_pu_var():

    # Get directory of .py file
    dir = os.path.dirname(os.path.abspath(__file__))

    flag_noPV = 0
    flag_PV = 1

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

    # List with transformers info
    xfmr_list = transformer_list()

    hours = ["9","10","11","12","13","14","15","16","17"]

    PV_powers_Vlimit = [] # Bus voltage variation criteria

    print("Running circuit comparisons for Voltages pu variations\n")
    t_start = time.time()

    for season in ["Spring","Summer","Autumn","Winter"]:

        if season == "Spring":
            irrad = "0.981"
        if season == "Summer":
            irrad = "0.944"
        if season == "Autumn":
            irrad = "0.923"
        if season == "Winter":
            irrad = "0.950"

        for hour in hours:

            PV_power = 5
            power_iteration = "run again"
            while power_iteration == "run again":

                for flag in [flag_noPV, flag_PV]:

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

                    # Set and calculate voltage bases
                    dssText.Command = "Redirect "+dir+"\\ckt24\\ckt24_vbases.dss"

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

                    # Change PVSystem parameters to get max power
                    if flag == flag_PV:
                        dssText.Command = \
                        "Redirect "+dir+"\\ckt24\\339PV_new.dss"
                        dssText.Command = \
                        "Redirect "+dir+"\\ckt24\\339PV_"+season+".dss"
                        for i in range(len(xfmr_list)):
                            bus_pv = xfmr_list[i][6]
                            kv_pv = xfmr_list[i][7]
                            phase = str(xfmr_list[i][1])
                            dssText.Command = "New PVSystem.PV"+str(i)\
+" phases=1 bus1="+bus_pv+"."+phase+" kv="+kv_pv+" kVA="+str(PV_power)\
+" irrad="+irrad+" pmpp="+str(PV_power)+" temperature=25 pf=1"\
+" %cutin=5 %cutout=5 effcurve=MyEff P-tCurve=MyPvst"\
+" Daily=MyIrrad Tdaily=Mytemp"

                    # Set and calculate voltage bases
                    dssText.Command = "Redirect "+dir+"\\ckt24\\ckt24_vbases.dss"
                    # Solve circuit
                    dssText.Command = "Solve mode=daily number=1 hour="+hour

                    # Results list
                    if flag == flag_PV:

                        voltages_list1p_PV = []
                        voltages_list2p_PV = []
                        voltages_list3p_PV = []

                        for buses1p in bus1p_listn:
                            voltages_list1p_PV.append(V(buses1p,
                            dssCircuit))
                        for buses2p in bus2p_listn:
                            voltages_list2p_PV.append(V(buses2p,
                            dssCircuit))
                        for buses3p in bus3p_listn:
                            voltages_list3p_PV.append(V(buses3p,
                            dssCircuit))

                    if flag == flag_noPV:

                        voltages_list1p_noPV = []
                        voltages_list2p_noPV = []
                        voltages_list3p_noPV = []

                        for buses1p in bus1p_listn:
                            voltages_list1p_noPV.append(V(buses1p,
                            dssCircuit))
                        for buses2p in bus2p_listn:
                            voltages_list2p_noPV.append(V(buses2p,
                            dssCircuit))
                        for buses3p in bus3p_listn:
                            voltages_list3p_noPV.append(V(buses3p,
                            dssCircuit))

                pu_limit = 0.015

                V_flag = 0
                for i in range(len(voltages_list1p_noPV)):
                    if abs(voltages_list1p_PV[i][0] -
                    voltages_list1p_noPV[i][0]) > pu_limit:
                        V_flag=1
                for i in range(len(voltages_list2p_noPV)):
                    if abs(voltages_list2p_PV[i][0] -
                    voltages_list2p_noPV[i][0]) > pu_limit:
                        V_flag=1
                    elif abs(voltages_list2p_PV[i][2] -
                    voltages_list2p_noPV[i][2]) > pu_limit:
                        V_flag=1
                for i in range(len(voltages_list3p_noPV)):
                    if abs(voltages_list3p_PV[i][0] -
                    voltages_list3p_noPV[i][0]) > pu_limit:
                        V_flag=1
                    elif abs(voltages_list3p_PV[i][2] -
                    voltages_list3p_noPV[i][2]) > pu_limit:
                        V_flag=1
                    elif abs(voltages_list3p_PV[i][0] -
                    voltages_list3p_noPV[i][0]) > pu_limit:
                        V_flag=1

                if V_flag==1:
                    PV_powers_Vlimit.append([season,hour,PV_power-5])
                    power_iteration = "stop running"

                if PV_power == 200:
                    PV_powers_Vlimit.append([season,hour,"max_iter_200"])
                    power_iteration = "stop running"

                PV_power = PV_power+5

            print("Running simulation of season %s, hour %s..." % (season,hour))
    print()
    print("List with season, hour and maximum power for PVSystem:")
    print(PV_powers_Vlimit)
    print()
    PV_powers_Vlimit = [int(e[-1]) for e in PV_powers_Vlimit]
    print("Minimum value: %d kW" % min(PV_powers_Vlimit))
    print()
    t_end = time.time()
    print("Total simulation time \
    (Voltage pu variation comparisons): %f" % (t_end - t_start))



def lines_criteria():

    # Get directory of .py file
    dir = os.path.dirname(os.path.abspath(__file__))

    flag_noPV = 0
    flag_PV = 1

    # Make lists with line names

    # Line_1p_list
    line1p_list = line_name_lists()[0]
    for i in range(len(line1p_list)):
        if i == 0:
            line1p_listn = [line1p_list[0][0]]
        else:
            line1p_listn.append(line1p_list[i][0])

    # Line_2p_list
    line2p_list = line_name_lists()[1]
    for i in range(len(line2p_list)):
        if i == 0:
            line2p_listn = [line2p_list[0][0]]
        else:
            line2p_listn.append(line2p_list[i][0])

    # Line_3p_list
    line3p_list = line_name_lists()[2]
    for i in range(len(line3p_list)):
        if i == 0:
            line3p_listn = [line3p_list[0][0]]
        else:
            line3p_listn.append(line3p_list[i][0])

    # List with transformers info
    xfmr_list = transformer_list()

    # Hours of interest when solving the circuit
    hours = ["9","10","11","12","13","14","15","16","17"]

    PV_powers_Climit = [] # Line currents criteria

    print("Running circuit comparisons for Currents - Lines Criteria\n")
    t_start = time.time()

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

    # Solve circuit in different loadshapes, season based
    dssText.Command = "Edit Loadshape.LS_PhaseA" \
    +" mult=(file=LS_PhaseA_SummerDay.txt)"
    dssText.Command = "Edit Loadshape.LS_PhaseB" \
    +" mult=(file=LS_PhaseB_SummerDay.txt)"
    dssText.Command = "Edit Loadshape.LS_PhaseC" \
    +" mult=(file=LS_PhaseC_SummerDay.txt)"
    dssText.Command = "Edit Loadshape.LS_ThreePhase" \
    +" mult=(file=LS_ThreePhase_SummerDay.txt)"
    dssText.Command = "Edit Loadshape.Other_Bus_Load" \
    +" mult=(file=Other_Bus_Load_SummerDay.txt)"

    # Set and calculate voltage bases
    dssText.Command = "Redirect "+dir+"\\ckt24\\ckt24_vbases.dss"
    # Solve circuit
    dssText.Command = "Solve mode=daily number=1 hour=15"

    currents_list1p_noPV = []
    currents_list2p_noPV = []
    currents_list3p_noPV = []

    for line1p in line1p_listn:
        dssCircuit.SetActiveElement("Line."+line1p)
        currents_list1p_noPV.append(dssCircuit.ActiveElement.NormalAmps)

    for line2p in line2p_listn:
        dssCircuit.SetActiveElement("Line."+line2p)
        currents_list2p_noPV.append(dssCircuit.ActiveElement.NormalAmps)

    for line3p in line3p_listn:
        dssCircuit.SetActiveElement("Line."+line3p)
        currents_list3p_noPV.append(dssCircuit.ActiveElement.NormalAmps)

    hours = ["9","10","11","12","13","14","15","16","17"]

    PV_powers_Climit = []

    for season in ["Spring","Summer","Autumn","Winter"]:

        if season == "Spring":
            irrad = "0.981"
        if season == "Summer":
            irrad = "0.944"
        if season == "Autumn":
            irrad = "0.923"
        if season == "Winter":
            irrad = "0.950"

        for hour in hours:

            PV_power = 5
            power_iteration = "run again"
            while power_iteration == "run again":

                # Clear the DSS
                dssObj.ClearAll()

                # Load circuit
                dssText.Command = "Compile "+dir+"\\ckt24\\ckt24.dss"

                # Set and calculate voltage bases
                dssText.Command = "Redirect "+dir+"\\ckt24\\ckt24_vbases.dss"

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

                # Change PVSystem parameters to get max power
                dssText.Command = \
                "Redirect "+dir+"\\ckt24\\339PV_new.dss"
                dssText.Command = \
                "Redirect "+dir+"\\ckt24\\339PV_"+season+".dss"
                for i in range(len(xfmr_list)):
                    bus_pv = xfmr_list[i][6]
                    kv_pv = xfmr_list[i][7]
                    phase = str(xfmr_list[i][1])
                    dssText.Command = "New PVSystem.PV"+str(i)\
+" phases=1 bus1="+bus_pv+"."+phase+" kv="+kv_pv+" kVA="+str(PV_power)\
+" irrad="+irrad+" pmpp="+str(PV_power)+" temperature=25 pf=1"\
+" %cutin=5 %cutout=5 effcurve=MyEff P-tCurve=MyPvst"\
+" Daily=MyIrrad Tdaily=Mytemp"

                # Set and calculate voltage bases
                dssText.Command = "Redirect "+dir+"\\ckt24\\ckt24_vbases.dss"
                # Solve circuit
                dssText.Command = "Solve mode=daily number=1 hour="+hour

                # Results list

                currents_list1p_PV = []
                currents_list2p_PV = []
                currents_list3p_PV = []


                for lines1p in line1p_listn:
                    currents_list1p_PV.append(C("Line."+lines1p, dssCircuit))

                for lines2p in line2p_listn:
                    currents_list2p_PV.append(C("Line."+lines2p, dssCircuit))

                for lines3p in line3p_listn:
                    currents_list3p_PV.append(C("Line."+lines3p, dssCircuit))

                C_flag = 0
                safe_factor = 0.8

                for i in range(len(currents_list1p_noPV)):
                    if abs(currents_list1p_PV[i][0]) > \
                    safe_factor*abs(currents_list1p_noPV[i]):
                        C_flag = 1
                for i in range(len(currents_list2p_noPV)):
                    if abs(currents_list2p_PV[i][0]) > \
                    safe_factor*abs(currents_list2p_noPV[i]):
                        C_flag = 1
                    if abs(currents_list2p_PV[i][2]) > \
                    safe_factor*abs(currents_list2p_noPV[i]):
                        C_flag = 1
                for i in range(len(currents_list3p_noPV)):
                    if abs(currents_list3p_PV[i][0]) > \
                    safe_factor*abs(currents_list3p_noPV[i]):
                        C_flag = 1
                    if abs(currents_list3p_PV[i][2]) > \
                    safe_factor*abs(currents_list3p_noPV[i]):
                        C_flag = 1
                    if abs(currents_list3p_PV[i][4]) > \
                    safe_factor*abs(currents_list3p_noPV[i]):
                        C_flag = 1

                if C_flag==1:
                    PV_powers_Climit.append([season,hour,PV_power-5])
                    power_iteration = "stop running"

                if PV_power == 200:
                    PV_powers_Climit.append([season,hour,"max_iter_200"])
                    power_iteration = "stop running"

                PV_power = PV_power+5
            print("Running simulation of season %s, hour %s..." % (season,hour))
    print()
    print("List with season, hour and maximum power for PVSystem:")
    print(PV_powers_Climit)
    print()
    PV_powers_Climit = [int(e[-1]) for e in PV_powers_Climit]
    print("Minimum value: %d kW" % min(PV_powers_Climit))
    print()


    t_end = time.time()
    print("Total simulation time (Current comparisons - "
    "lines criteria): %f" % (t_end - t_start))





def transformers_criteria():

    # Get directory of .py file
    dir = os.path.dirname(os.path.abspath(__file__))

    flag_noPV = 0
    flag_PV = 1

    # List with transformers info
    xfmr_list = transformer_list()

    # Hours of interest when solving the circuit
    hours = ["9","10","11","12","13","14","15","16","17"]

    PV_powers_Plimit = [] # Transformers kva criteria

    print("Running circuit comparisons for Powers - Transformers Criteria\n")
    t_start = time.time()

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

    # Transformers nominal kva list
    transformer_kva_nominal = []
    all_elements = dssCircuit.AllElementNames
    t_list = [s for s in all_elements if "Transformer" in s]

    # Remove transformers that work over nominal kva in circuit without PV
    # from t_list and put them into another list
    t_list.remove("Transformer.05410_g2100dl9800")
    t_list.remove("Transformer.05410_g2100en2200")
    t_list.remove("Transformer.05410_g2100gi2700")
    t_list.remove("Transformer.05410_g2100nj7400")
    t_list.remove("Transformer.05410_g2101bc7200")
    t_list.remove("Transformer.05410_g2102cc0600")



    t_list_exceptions = []
    t_list_exceptions.append("Transformer.05410_g2100dl9800")
    t_list_exceptions.append("Transformer.05410_g2100en2200")
    t_list_exceptions.append("Transformer.05410_g2100gi2700")
    t_list_exceptions.append("Transformer.05410_g2100nj7400")
    t_list_exceptions.append("Transformer.05410_g2101bc7200")
    t_list_exceptions.append("Transformer.05410_g2102cc0600")



    for i in range(len(t_list)):
        dssCircuit.SetActiveElement(t_list[i])
        dssCircuit.Transformers.Name = \
        t_list[i].replace("Transformer.","")
        transformer_kva_nominal.append(dssCircuit.Transformers.kva)


    hours = ["9","10","11","12","13","14","15","16","17"]

    for season in ["Spring","Summer","Autumn","Winter"]:

        if season == "Spring":
            irrad = "0.981"
        if season == "Summer":
            irrad = "0.944"
        if season == "Autumn":
            irrad = "0.923"
        if season == "Winter":
            irrad = "0.950"

        for hour in hours:

            PV_power = 5
            power_iteration = "run again"
            while power_iteration == "run again":

                # Clear the DSS
                dssObj.ClearAll()

                # Load circuit
                dssText.Command = "Compile "+dir+"\\ckt24\\ckt24.dss"

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

                # Change PVSystem parameters to get max power
                dssText.Command = "Redirect "+dir+"\\ckt24\\339PV_"+season+".dss"
                for i in range(len(xfmr_list)):
                    bus_pv = xfmr_list[i][6]
                    kv_pv = xfmr_list[i][7]
                    phase = str(xfmr_list[i][1])
                    dssText.Command = "New PVSystem.PV"+str(i)\
+" phases=1 bus1="+bus_pv+"."+phase+" kv="+kv_pv+" kVA="+str(PV_power)\
+" irrad="+irrad+" pmpp="+str(PV_power)+" temperature=25 pf=1"\
+" %cutin=5 %cutout=5 effcurve=MyEff P-tCurve=MyPvst"\
+" Daily=MyIrrad Tdaily=Mytemp"

                # Set and calculate voltage bases
                dssText.Command = "Redirect "+dir+"\\ckt24\\ckt24_vbases.dss"
                # Solve circuit
                dssText.Command = "Solve mode=daily number=1 hour="+hour

                # Results list
                transformer_kva_PV = []

                for transformer in t_list:
                    transformer_kva_PV.append(P(transformer, dssCircuit))

                safe_factor = 1
                P_flag = 0
                for i in range(len(t_list)):
                    if len(transformer_kva_PV[i]) == 8:
                        if  (abs(transformer_kva_PV[i][0]))> \
                        safe_factor*abs(transformer_kva_nominal[i]):
                            P_flag = 1

                    elif len(transformer_kva_PV[i]) == 16:
                        if  (abs(transformer_kva_PV[i][0])+ \
                        abs(transformer_kva_PV[i][2])+ \
                        abs(transformer_kva_PV[i][4]))> \
                        safe_factor*abs(transformer_kva_nominal[i]):
                            P_flag = 1


                if P_flag==1:
                    PV_powers_Plimit.append([season,hour,PV_power-5])
                    power_iteration = "stop running"

                if PV_power == 200:
                    PV_powers_Plimit.append([season,hour,"max_iter_200"])
                    power_iteration = "stop running"

                PV_power = PV_power+5

            print()
            print(season,hour)
            print(PV_powers_Plimit)
            print()


    t_end = time.time()
    print("Total simulation time (power comparisons - "
    "transformers criteria): %f" % (t_end - t_start))



if __name__ == "__main__":
    main()
