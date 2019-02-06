from functions import bus_name_lists, line_name_lists, V, C, P
import os
import time
import win32com.client

def main():

    # Get directory of .py file
    dir = os.path.dirname(os.path.abspath(__file__))

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

    transformer_kva_nominal = []
    all_elements = dssCircuit.AllElementNames
    transformer_list = [s for s in all_elements if "Transformer" in s]
    for i in range(len(transformer_list)):
        dssCircuit.SetActiveElement(transformer_list[i])
        dssCircuit.Transformers.Name = \
        transformer_list[i].replace("Transformer.","")
        transformer_kva_nominal.append(dssCircuit.Transformers.kva)

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

    transformer_kva_ckt = []
    for transformer in transformer_list:
        transformer_kva_ckt.append(P(transformer, dssCircuit))

    transformer_compare = []
    for i in range(len(transformer_list)):
        t = []
        t.append(transformer_list[i])
        t.append(transformer_kva_nominal[i])
        if len(transformer_kva_ckt[i]) == 8:
            t.append(transformer_kva_ckt[i][0])
        elif len(transformer_kva_ckt[i]) == 16:
            t.append(transformer_kva_ckt[i][0]+
            transformer_kva_ckt[i][2]+transformer_kva_ckt[i][4])
        transformer_compare.append(t)
    # print(transformer_compare)
    # print()
    print("Transformers over nominal kva:")
    print()
    for i in range(len(transformer_compare)):
        if transformer_compare[i][2] > transformer_compare[i][1]:
            print(transformer_compare[i][0])
    print()
    kva_sum = []
    for i in range(len(transformer_compare)):
        if i > 25:
            kva_sum.append(transformer_compare[i][1])
    kva_sum = sum(kva_sum)
    print("Service xfmr connected kva: %.1f" % kva_sum)

if __name__ == "__main__":

    print(
    """
This code runs a simulation for ckt24 at 15h of summer and returns which
transformers are working over nominal power and the sum of the service
transformers nominal power.
    """
    )

    main()
