# -*- coding: utf-8 -*-

import pylab
import numpy
import os
from math import acos,cos,sin,pi
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

def deg2rad(angle_deg):
    return angle_deg*pi/180.0

def irradshape_reader(file):
    with open(file,"r") as filehandler:
        irrad_data = filehandler.readlines()
    dhi = []
    dni = []
    ghi = []
    zenith = []
    for i in range(len(irrad_data)):
        if i>2 and i%2!=0:
            dhi.append(float(irrad_data[i].split(",")[8]))
            dni.append(float(irrad_data[i].split(",")[9]))
            ghi.append(float(irrad_data[i].split(",")[10]))
            zenith.append(float(irrad_data[i].split(",")[11]))

    return [dhi,dni,ghi,zenith]

def azimuth_reader(file):
    with open(file,"r") as filehandler:
        azimuth_data = filehandler.readlines()
    az = []
    for i in range(365):
        for j in range(3,8468,368):
            az.append(float(azimuth_data[j+i]))
    return az

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

def irradshape_writer(filename,numbers):
    file = Path(filename)
    if file.is_file():
        os.remove(filename)
    with open(filename,"a") as filehandler:
        for i in range(len(numbers)):
            filehandler.write(str(round(numbers[i],9))+"\n")

def main():

    dhi = irradshape_reader("Topeka_solar_2015.csv")[0]
    dni = irradshape_reader("Topeka_solar_2015.csv")[1]
    ghi = irradshape_reader("Topeka_solar_2015.csv")[2]
    zenith = irradshape_reader("Topeka_solar_2015.csv")[3]

    azimuth = azimuth_reader("topeka_azimuth.txt")
    beta = deg2rad(39.05)
    az_PV = deg2rad(180)
    albedo = 0.3

    irrad = []
    aoi = []

    for i in range(len(dhi)):
        z = deg2rad(zenith[i])
        az = deg2rad(azimuth[i])
        aoi.append(acos(cos(z)*cos(beta)+sin(z)*sin(beta)*cos(az-az_PV)))

        term1 = dni[i]*cos(aoi[i])
        if term1<0:
            term1 = 0

        term2 = ghi[i]*albedo*(1-cos(beta))/2

        term3 = dhi[i]*(1+cos(beta))/2

        irrad.append(term1+term2+term3)

    plot2year(irrad)
    pylab.title("Yearly Irradiance")
    pylab.show()

    std_dev = []

    Summer = irrad[4104:6360]
    std_dev.append(numpy.amax(getstddev(Summer)))
    Summer = getmean(Summer)
    irradshape_writer("irrad_SummerDay.txt",Summer)
    pylab.plot(Summer, label='Summer')
    pylab.gca().set_ylim([0,1000])
    pylab.xticks(range(24))

    Spring = irrad[1872:4104]
    std_dev.append(numpy.amax(getstddev(Spring)))
    Spring = getmean(Spring)
    irradshape_writer("irrad_SpringDay.txt",Spring)
    pylab.plot(Spring, label='Spring')
    pylab.gca().set_ylim([0,1000])
    pylab.xticks(range(24))

    Autumn = irrad[6360:8520]
    std_dev.append(numpy.amax(getstddev(Autumn)))
    Autumn = getmean(Autumn)
    irradshape_writer("irrad_AutumnDay.txt",Autumn)
    pylab.plot(Autumn, label='Autumn')
    pylab.gca().set_ylim([0,1000])
    pylab.xticks(range(24))

    Winter = irrad[8520:]+irrad[:1872]
    std_dev.append(numpy.amax(getstddev(Winter)))
    Winter = getmean(Winter)
    irradshape_writer("irrad_WinterDay.txt",Winter)
    pylab.plot(Winter, label='Winter')
    pylab.gca().set_ylim([0,1000])
    pylab.xticks(range(24))
    pylab.legend(loc=1)
    pylab.title("Daily Typical Irradiance")
    pylab.show()
    print("The biggest standard deviation for the irradiances (W/m^2) is: ",
    round(numpy.amax(std_dev),2))

if __name__ == "__main__":

    print(
    """
This code takes the anual irradiance shape from Topeka, Kansas, US and uses
it for ckt24. It works getting the mean for a typical day of one season in an
inclined photovoltaic solar panel inclined by an angle beta. Try changing the
beta value to see how it affects the yearly irradiance in the panel!
    """
    )

    main()
