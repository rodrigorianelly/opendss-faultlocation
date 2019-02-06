from functions import bus_name_lists, transformer_list, V, C
import json
import os
import time
import win32com.client

def main():

    t_start = time.time()

    # Get directory of .py file
    dir = os.path.dirname(os.path.abspath(__file__))

    # Bus_1p_list
    bus1p_list = bus_name_lists()[0]

    # Bus_2p_list
    bus2p_list = bus_name_lists()[1]

    # Bus_3p_list
    bus3p_list = bus_name_lists()[2]

    # List with transformers info
    xfmr_list = transformer_list()

    print("Running circuit solution\n")
    t_start = time.time()

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

    new_edit = "New "

    # Solve circuit in different loadshapes, according to seasons
    dssText.Command = "Redirect "+dir+"\\ckt24\\339PV_new.dss"
    
    for season in ["Spring","Summer","Autumn","Winter"]:

        if season == "Spring":
            irrad = "0.981"
        if season == "Summer":
            irrad = "0.944"
        if season == "Autumn":
            irrad = "0.923"
        if season == "Winter":
            irrad = "0.950"

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

        dssText.Command = "Redirect "+dir+"\\ckt24\\339PV_"+season+".dss"
        for i in range(len(xfmr_list)):
            bus_pv = xfmr_list[i][6]
            kv_pv = xfmr_list[i][7]
            phase = str(xfmr_list[i][1])
            dssText.Command = new_edit+"PVSystem.PV"+str(i)\
+" phases=1 bus1="+bus_pv+"."+phase+" kv="+kv_pv+" kVA=15"\
+" irrad="+irrad+" pmpp=15 temperature=25 pf=1"\
+" %cutin=5 %cutout=5 effcurve=MyEff P-tCurve=MyPvst"\
+" Daily=MyIrrad Tdaily=Mytemp"

        if new_edit == "New ":
            new_edit = "Edit "

        for hour in [9,10,11,12,13,14,15,16,17]:

            # Set and calculate voltage bases
            dssText.Command = "Redirect "+dir+"\\ckt24\\ckt24_vbases.dss"

            dssText.Command = "Solve mode=daily number=1 hour="+str(hour)

            # Results list
            results_list = [[season, hour],
            V("SourceBus", dssCircuit), V("SubXfmr_LSB", dssCircuit),
            C("Vsource.source", dssCircuit),
            C("Transformer.SUBXFMR", dssCircuit)]

            with open(dir+"\\ckt24_solve.txt","a") \
            as filehandler:
                json.dump(results_list, filehandler)
                filehandler.write("\n")


    t_end = time.time()
    print("Total simulation time: %f" % (t_end - t_start))


if __name__ == "__main__":
    main()
