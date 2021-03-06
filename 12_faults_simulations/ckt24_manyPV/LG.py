from functions import bus_name_lists, transformer_list, V, C, float3
import json
import os
import sqlite3
import time
import win32com.client

def fault_LG(faultbus,faultphase,phases,r,buscoords,xfmr_list,dssObj,conn,c):
    """LG fault simulation in bus and results
    """

    # Get directory of .py file
    dir = os.path.dirname(os.path.abspath(__file__))

    dssText = dssObj.Text
    dssCircuit = dssObj.ActiveCircuit
    dssBus = dssCircuit.ActiveBus


    dssText.Command = "Edit Fault.fault phases=1 bus1="+faultbus \
    +faultphase+" r="+r

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

        dssText.Command = "Redirect "+dir+"\\339PV_"+season+".dss"
        for i in range(len(xfmr_list)):
            bus_pv = xfmr_list[i][6]
            kv_pv = xfmr_list[i][7]
            phase = str(xfmr_list[i][1])
            dssText.Command = "Edit PVSystem.PV"+str(i)\
+" phases=1 bus1="+bus_pv+"."+phase+" kv="+kv_pv+" kVA=15"\
+" irrad="+irrad+" pmpp=15 temperature=25 pf=1"\
+" %cutin=5 %cutout=5 effcurve=MyEff P-tCurve=MyPvst"\
+" Daily=MyIrrad Tdaily=Mytemp"

        for hour in [9,10,11,12,13,14,15,16,17]:

            dssText.Command = "Redirect "+dir+"\\ckt24_vbases.dss"
            dssText.Command = "Solve mode=daily number=1 hour="+str(hour)

            Vsub = V("SubXfmr_LSB", dssCircuit)
            Csub = C("Transformer.SUBXFMR", dssCircuit)

            c.execute("""INSERT INTO PV339_faultloc_db (fault_type,
            season, hour, bus, buscoordX, buscoordY, fault_resistance,
            busphases, faultphases, Vsub_mag1, Vsub_ang1, Vsub_mag2,
            Vsub_ang2, Vsub_mag3, Vsub_ang3, Isub_mag1, Isub_ang1,
            Isub_mag2, Isub_ang2, Isub_mag3, Isub_ang3) VALUES (
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            "LG",season, int(hour), faultbus, float(buscoords[0]),
            float(buscoords[1]), int(r), phases, faultphase,
            float3(Vsub[0]), float3(Vsub[1]), float3(Vsub[2]),
            float3(Vsub[3]), float3(Vsub[4]), float3(Vsub[5]),
            float3(Csub[8]), float3(Csub[9]), float3(Csub[10]),
            float3(Csub[11]), float3(Csub[12]), float3(Csub[13])))
            conn.commit()

    return

def main():

    t_start = time.time()

    # Get directory of .py file
    dir = os.path.dirname(os.path.abspath(__file__))

    # Create database for faults
    conn = sqlite3.connect('database_faultlocation_339PV.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS PV339_faultloc_db (
    fault_type TEXT, season TEXT, hour INT, bus TEXT,
    buscoordX REAL, buscoordY REAL, fault_resistance INT,
    busphases TEXT, faultphases TEXT, Vsub_mag1 REAL, Vsub_ang1 REAL,
    Vsub_mag2 REAL, Vsub_ang2 REAL, Vsub_mag3 REAL, Vsub_ang3 REAL,
    Isub_mag1 REAL, Isub_ang1 REAL, Isub_mag2 REAL, Isub_ang2 REAL,
    Isub_mag3 REAL, Isub_ang3 REAL)""")

    # Bus_1p_list
    bus1p_list = bus_name_lists()[0]

    # Bus_2p_list
    bus2p_list = bus_name_lists()[1]

    # Bus_3p_list
    bus3p_list = bus_name_lists()[2]

    # List with transformers info
    xfmr_list = transformer_list()

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

    # Initialize PV elements
    dssText.Command = "Redirect "+dir+"\\ckt24\\339PV_new.dss"
    for i in range(len(xfmr_list)):
        bus_pv = xfmr_list[i][6]
        kv_pv = xfmr_list[i][7]
        phase = str(xfmr_list[i][1])
        dssText.Command = "New PVSystem.PV"+str(i)\
+" phases=1 bus1="+bus_pv+"."+phase+" kv="+kv_pv+" kVA=15"\
+" irrad=0.981 pmpp=15 temperature=25 pf=1"\
+" %cutin=5 %cutout=5 effcurve=MyEff P-tCurve=MyPvst"\
+" Daily=MyIrrad Tdaily=Mytemp"

    # Initialize fault elements
    dssText.Command = "New Fault.fault"

    # Fault resistances
    fault_resistances = ["05","10","15","20","25","30","35","40","45","50"]

    print("\nAll LG faults for 1p buses\n")
    for bus1p in bus1p_list:
        print("Bus: %s" % bus1p)
        t1 = time.time()
        bus1p[3] = "."+str(bus1p[3])
        for r in fault_resistances:
            fault_LG(bus1p[0],bus1p[3],bus1p[3],r,[bus1p[1],bus1p[2]],
            xfmr_list,dssObj,conn,c)
        t2 = time.time()
        print("Time to simulate this bus: %fs\n" % (t2 - t1))

    print("\nAll LG faults for 2p buses\n")
    for bus2p in bus2p_list:
        print("Bus: %s" % bus2p)
        t1 = time.time()
        phases = ".%d.%d" % (bus2p[3],bus2p[4])
        for faultphase in ["."+str(bus2p[3]),"."+str(bus2p[4])]:
            for r in fault_resistances:
                fault_LG(bus2p[0],faultphase,phases,r,[bus2p[1],bus2p[2]],
                xfmr_list,dssObj,conn,c)
        t2 = time.time()
        print("Time to simulate this bus: %fs\n" % (t2 - t1))

    print("\nAll LG faults for 3p buses\n")
    for bus3p in bus3p_list:
        print("Bus: %s" % bus3p)
        t1 = time.time()
        for faultphase in [".1",".2",".3"]:
            for r in fault_resistances:
                fault_LG(bus3p[0],faultphase,".1.2.3",r,[bus3p[1],bus3p[2]],
                xfmr_list,dssObj,conn,c)
        t2 = time.time()
        print("Time to simulate this bus: %fs\n" % (t2 - t1))

    t_end = time.time()
    print("\n\n\nTotal simulation time: %f\n\n\n" % (t_end - t_start))


if __name__ == "__main__":
    main()
