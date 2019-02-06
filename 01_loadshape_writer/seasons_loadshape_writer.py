import pylab
import numpy
import os

def plot2year(y,label_):
    x = []
    xticks_ = []
    for i in range(8760):
        x.append(i)
        if i == 1872:
            xticks_.append("mar 20")
        elif i == 4104:
            xticks_.append("jun 21")
        elif i == 6360:
            xticks_.append("sep 22")
        elif i == 8520:
            xticks_.append("dec 22")
        else:
            xticks_.append("")
    pylab.xticks(x, xticks_, rotation=30)
    pylab.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False)         # labels along the bottom edge are off
    pylab.plot(x,y,label=label_)
    return

def loadshape_reader(file):
    with open(file,"r") as filehandler:
        loadshape = filehandler.readlines()
    for i in range(len(loadshape)):
        loadshape[i] = loadshape[i].replace("\n","")
        loadshape[i] = float(loadshape[i])
    return loadshape

def getmean(array):
    array = numpy.asarray(array)
    array = numpy.reshape(array,(-1,24))
    array = numpy.mean(array,axis=0)
    return array

def getstddev(array):
    array = numpy.asarray(array)
    array = numpy.reshape(array,(-1,24))
    array = numpy.std(array,axis=0)
    return array

def loadshape_writer(filename,numbers):
    if os.path.isfile(filename):
        os.remove(filename)

    with open(filename,"a") as filehandler:
        for i in range(len(numbers)):
            filehandler.write(str(round(numbers[i],9))+"\n")

def plot_loadshape_years(LS_PhaseA, LS_PhaseB, LS_PhaseC, LS_ThreePhase,
Other_Bus_Load):

    plot2year(LS_PhaseA,"Phase A")
    pylab.legend(loc=1)
    pylab.show()

    plot2year(LS_PhaseB,"Phase B")
    pylab.legend(loc=1)
    pylab.show()

    plot2year(LS_PhaseC,"Phase C")
    pylab.legend(loc=1)
    pylab.show()

    plot2year(LS_ThreePhase,"Three-phase")
    pylab.legend(loc=1)
    pylab.show()

    plot2year(Other_Bus_Load,"Special")
    pylab.legend(loc=1)
    pylab.show()

def seasons_mean_stddev_plot(LS_PhaseA, LS_PhaseB, LS_PhaseC, LS_ThreePhase,
Other_Bus_Load):
    std_dev = []

    Spring_A = LS_PhaseA[1872:4104]
    Spring_B = LS_PhaseB[1872:4104]
    Spring_C = LS_PhaseC[1872:4104]
    Spring_3 = LS_ThreePhase[1872:4104]
    Spring_Other = Other_Bus_Load[1872:4104]

    std_dev.append(numpy.amax(getstddev(Spring_A)))
    std_dev.append(numpy.amax(getstddev(Spring_B)))
    std_dev.append(numpy.amax(getstddev(Spring_C)))
    std_dev.append(numpy.amax(getstddev(Spring_3)))
    std_dev.append(numpy.amax(getstddev(Spring_Other)))

    Spring_A = getmean(Spring_A)
    Spring_B = getmean(Spring_B)
    Spring_C = getmean(Spring_C)
    Spring_3 = getmean(Spring_3)
    Spring_Other = getmean(Spring_Other)

    loadshape_writer("LS_PhaseA_SpringDay.txt",Spring_A)
    loadshape_writer("LS_PhaseB_SpringDay.txt",Spring_B)
    loadshape_writer("LS_PhaseC_SpringDay.txt",Spring_C)
    loadshape_writer("LS_ThreePhase_SpringDay.txt",Spring_3)
    loadshape_writer("Other_Bus_Load_SpringDay.txt",Spring_Other)
    pylab.plot(Spring_A, label="Phase A")
    pylab.plot(Spring_B, label="Phase B")
    pylab.plot(Spring_C, label="Phase C")
    pylab.plot(Spring_3, label="Three Phase")
    pylab.plot(Spring_Other, label="Special")
    pylab.gca().set_ylim([0.25,0.8])
    pylab.xticks(range(24))
    pylab.legend(loc=2)
    pylab.title("Spring")
    pylab.show()

    Summer_A = LS_PhaseA[4104:6360]
    Summer_B = LS_PhaseB[4104:6360]
    Summer_C = LS_PhaseC[4104:6360]
    Summer_3 = LS_ThreePhase[4104:6360]
    Summer_Other = Other_Bus_Load[4104:6360]

    std_dev.append(numpy.amax(getstddev(Summer_A)))
    std_dev.append(numpy.amax(getstddev(Summer_B)))
    std_dev.append(numpy.amax(getstddev(Summer_C)))
    std_dev.append(numpy.amax(getstddev(Summer_3)))
    std_dev.append(numpy.amax(getstddev(Summer_Other)))

    Summer_A = getmean(Summer_A)
    Summer_B = getmean(Summer_B)
    Summer_C = getmean(Summer_C)
    Summer_3 = getmean(Summer_3)
    Summer_Other = getmean(Summer_Other)
    loadshape_writer("LS_PhaseA_SummerDay.txt",Summer_A)
    loadshape_writer("LS_PhaseB_SummerDay.txt",Summer_B)
    loadshape_writer("LS_PhaseC_SummerDay.txt",Summer_C)
    loadshape_writer("LS_ThreePhase_SummerDay.txt",Summer_3)
    loadshape_writer("Other_Bus_Load_SummerDay.txt",Summer_Other)
    pylab.plot(Summer_A, label="Phase A")
    pylab.plot(Summer_B, label="Phase B")
    pylab.plot(Summer_C, label="Phase C")
    pylab.plot(Summer_3, label="Three-phase")
    pylab.plot(Summer_Other, label="Special")
    pylab.gca().set_ylim([0.25,0.8])
    pylab.xticks(range(24))
    pylab.legend(loc=2)
    pylab.title("Summer")
    pylab.show()

    Autumn_A = LS_PhaseA[6360:8520]
    Autumn_B = LS_PhaseB[6360:8520]
    Autumn_C = LS_PhaseC[6360:8520]
    Autumn_3 = LS_ThreePhase[6360:8520]
    Autumn_Other = Other_Bus_Load[6360:8520]

    std_dev.append(numpy.amax(getstddev(Autumn_A)))
    std_dev.append(numpy.amax(getstddev(Autumn_B)))
    std_dev.append(numpy.amax(getstddev(Autumn_C)))
    std_dev.append(numpy.amax(getstddev(Autumn_3)))
    std_dev.append(numpy.amax(getstddev(Autumn_Other)))

    Autumn_A = getmean(Autumn_A)
    Autumn_B = getmean(Autumn_B)
    Autumn_C = getmean(Autumn_C)
    Autumn_3 = getmean(Autumn_3)
    Autumn_Other = getmean(Autumn_Other)
    loadshape_writer("LS_PhaseA_AutumnDay.txt",Autumn_A)
    loadshape_writer("LS_PhaseB_AutumnDay.txt",Autumn_B)
    loadshape_writer("LS_PhaseC_AutumnDay.txt",Autumn_C)
    loadshape_writer("LS_ThreePhase_AutumnDay.txt",Autumn_3)
    loadshape_writer("Other_Bus_Load_AutumnDay.txt",Autumn_Other)
    pylab.plot(Autumn_A, label="Phase A")
    pylab.plot(Autumn_B, label="Phase B")
    pylab.plot(Autumn_C, label="Phase C")
    pylab.plot(Autumn_3, label="Three-phase")
    pylab.plot(Autumn_Other, label="Special")
    pylab.gca().set_ylim([0.25,0.8])
    pylab.xticks(range(24))
    pylab.legend(loc=8)
    pylab.legend(loc=2)
    pylab.title("Autumn")
    pylab.show()

    Winter_A = LS_PhaseA[8520:]+LS_PhaseA[:1872]
    Winter_B = LS_PhaseB[8520:]+LS_PhaseB[:1872]
    Winter_C = LS_PhaseC[8520:]+LS_PhaseC[:1872]
    Winter_3 = LS_ThreePhase[8520:]+LS_ThreePhase[:1872]
    Winter_Other = Other_Bus_Load[8520:]+Other_Bus_Load[:1872]

    std_dev.append(numpy.amax(getstddev(Winter_A)))
    std_dev.append(numpy.amax(getstddev(Winter_B)))
    std_dev.append(numpy.amax(getstddev(Winter_C)))
    std_dev.append(numpy.amax(getstddev(Winter_3)))
    std_dev.append(numpy.amax(getstddev(Winter_Other)))

    Winter_A = getmean(Winter_A)
    Winter_B = getmean(Winter_B)
    Winter_C = getmean(Winter_C)
    Winter_3 = getmean(Winter_3)
    Winter_Other = getmean(Winter_Other)
    loadshape_writer("LS_PhaseA_WinterDay.txt",Winter_A)
    loadshape_writer("LS_PhaseB_WinterDay.txt",Winter_B)
    loadshape_writer("LS_PhaseC_WinterDay.txt",Winter_C)
    loadshape_writer("LS_ThreePhase_WinterDay.txt",Winter_3)
    loadshape_writer("Other_Bus_Load_WinterDay.txt",Winter_Other)
    pylab.plot(Winter_A, label="Phase A")
    pylab.plot(Winter_B, label="Phase B")
    pylab.plot(Winter_C, label="Phase C")
    pylab.plot(Winter_3, label="Three-phase")
    pylab.plot(Winter_Other, label="Special")
    pylab.gca().set_ylim([0.25,0.8])
    pylab.xticks(range(24))
    #pylab.legend(loc=8, bbox_to_anchor=(0.4,0))
    pylab.legend(loc=3)
    pylab.title("Winter")
    pylab.show()

    print("The biggest standard deviation for the loadshapes(pu) is: ",
    round(numpy.amax(std_dev),2))


if __name__ == "__main__":

    print(
    """
This code takes the anual loadshape from ckt24 and gets the mean for a
typical day of one season
    """
    )

    LS_PhaseA = loadshape_reader("LS_PhaseA.txt")
    LS_PhaseB = loadshape_reader("LS_PhaseB.txt")
    LS_PhaseC = loadshape_reader("LS_PhaseC.txt")
    LS_ThreePhase = loadshape_reader("LS_ThreePhase.txt")
    Other_Bus_Load = loadshape_reader("Other_Bus_Load.txt")

    plot_loadshape_years(LS_PhaseA, LS_PhaseB, LS_PhaseC, LS_ThreePhase,
    Other_Bus_Load)

    seasons_mean_stddev_plot(LS_PhaseA, LS_PhaseB, LS_PhaseC, LS_ThreePhase,
    Other_Bus_Load)
