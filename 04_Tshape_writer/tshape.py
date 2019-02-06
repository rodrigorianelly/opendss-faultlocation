# -*- coding: utf-8 -*-

import pylab
import numpy
import os
from pathlib import Path

def plot2year(y):
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
    pylab.plot(x,y)
    return

def tshape_reader(file):
    with open(file,"r") as filehandler:
        tshape = filehandler.readlines()
    for i in range(len(tshape)):
        if i>2 and i%2!=0:
            tshape[i] = tshape[i].split(",")
            tshape[i] = tshape[i][13]
            tshape[i] = float(tshape[i])
    return tshape[3::2]

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


def tshape_writer(filename,numbers):
    file = Path(filename)
    if file.is_file():
        os.remove(filename)
    with open(filename,"a") as filehandler:
        for i in range(len(numbers)):
            filehandler.write(str(round(numbers[i],9))+"\n")
def main():

    temps = tshape_reader("Topeka_solar_2015.csv")

    plot2year(temps)
    pylab.title("Yearly Temperature (°C)")
    pylab.show()

    std_dev = []

    Summer = temps[4104:6360]
    std_dev.append(numpy.amax(getstddev(Summer)))
    Summer = getmean(Summer)
    tshape_writer("temps_SummerDay.txt",Summer)
    pylab.plot(Summer, label='Summer')

    Spring = temps[1872:4104]
    std_dev.append(numpy.amax(getstddev(Spring)))
    Spring = getmean(Spring)
    tshape_writer("temps_SpringDay.txt",Spring)
    pylab.plot(Spring, label='Spring')

    Autumn = temps[6360:8520]
    std_dev.append(numpy.amax(getstddev(Autumn)))
    Autumn = getmean(Autumn)
    tshape_writer("temps_AutumnDay.txt",Autumn)
    pylab.plot(Autumn, label='Autumn')

    Winter = temps[8520:]+temps[:1872]
    std_dev.append(numpy.amax(getstddev(Winter)))
    Winter = getmean(Winter)
    tshape_writer("temps_WinterDay.txt",Winter)
    pylab.plot(Winter, label='Winter')
    pylab.gca().set_ylim([-10,30])
    pylab.xticks(range(24))
    pylab.legend(loc=2)
    pylab.title("Daily Temperature")
    pylab.xlabel("Hour")
    pylab.ylabel("Temperature (°C)")
    pylab.show()

    print("The biggest standard deviation for the temperatures (°C) is: ",
    round(numpy.amax(std_dev),2))

if __name__ == "__main__":

    print(
    """
This code takes the anual temperature shape from Topeka, Kansas, US and uses
it for ckt24. It works getting the mean for a typical day of one season.
    """
    )

    main()
