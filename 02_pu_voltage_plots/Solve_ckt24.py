from functions import bus_name_lists, line_name_lists, V, C
import win32com.client
import os
import ckt24_colorV
import matplotlib.pyplot as plt

def main():

    # Get directory of .py file
    dir = os.path.dirname(os.path.abspath(__file__))

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

    season = "Spring"
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

    hour=3

    # Set and calculate voltage bases
    dssText.Command = "Redirect "+dir+"\\ckt24\\ckt24_vbases.dss"

    # Solve circuit
    dssText.Command = "Solve mode=daily number=1 hour="+str(hour)

    # Circuit plot
    norm = [1,1.05]

    ckt24_colorV.ckt24_plot(l1,l2,l3,1,norm,dssCircuit)
    plt.ylim(3707500,3727500)
    plt.xlim(11730000,11747500)
    plt.axis("off")
    plt.title("Phase A, Spring 3h")
    plt.show()

    ckt24_colorV.ckt24_plot(l1,l2,l3,2,norm,dssCircuit)
    plt.ylim(3707500,3727500)
    plt.xlim(11730000,11747500)
    plt.axis("off")
    plt.title("Phase B, Spring 3h")
    plt.show()

    ckt24_colorV.ckt24_plot(l1,l2,l3,3,norm,dssCircuit)
    plt.ylim(3707500,3727500)
    plt.xlim(11730000,11747500)
    plt.axis("off")
    plt.title("Phase C, Spring 3h")
    plt.show()







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

    # Set and calculate voltage bases
    dssText.Command = "Redirect "+dir+"\\ckt24\\ckt24_vbases.dss"

    dssText.Command = "Solve mode=daily number=1 hour="+str(hour)

    # Results list
    ckt24_colorV.ckt24_plot(l1,l2,l3,1,norm,dssCircuit)
    plt.ylim(3707500,3727500)
    plt.xlim(11730000,11747500)
    plt.axis("off")
    plt.title("Phase A, Summer 15h")
    plt.show()

    ckt24_colorV.ckt24_plot(l1,l2,l3,2,norm,dssCircuit)
    plt.ylim(3707500,3727500)
    plt.xlim(11730000,11747500)
    plt.axis("off")
    plt.title("Phase B, Summer 15h")
    plt.show()

    ckt24_colorV.ckt24_plot(l1,l2,l3,3,norm,dssCircuit)
    plt.ylim(3707500,3727500)
    plt.xlim(11730000,11747500)
    plt.axis("off")
    plt.title("Phase C, Summer 15h")
    plt.show()



if __name__ == "__main__":

    print(
    """
This code plots ckt24 pu voltage profile for situations where there is
high load and low load.
    """
    )

    main()
