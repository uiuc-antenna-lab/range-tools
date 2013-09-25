# -*- coding: utf-8 -*-
"""
Created on Fri Sep 06 14:30:23 2013

@author: Kurt
"""

import sys
import numpy, pyvisa, time, datetime
from pylab import *
import scipy.io as sio
from visa import *

print sys.argv[1]
#LOAD IN TEST PARAMETERS FROM TEXT FILE
fid = open(sys.argv[1],'r')
fid.readline()
fid.readline()
fid.readline()
project = fid.readline().split()[2]
datafile = fid.readline().split()[2]
option = fid.readline().split()[2]
fid.readline()
fid.readline()
fstart = fid.readline().split()[2]
fstop = fid.readline().split()[2]
npts = fid.readline().split()[2]
fid.readline()
fid.readline()
pol = fid.readline().split()[2]
fid.readline()
fid.readline()
ares = fid.readline().split()[2]
start = fid.readline().split()[2]
stop = fid.readline().split()[2]
fid.readline()
fid.readline()
comments = fid.read()
fid.close()

#VISA reference locations -- store these to a file?
PNAref = 'GPIB0::16'
POSref = 'GPIB0::17'

#create instrument objects
pna = instrument(PNAref)
pos = instrument(POSref)

#function to grab current turntable location from positioner
def getpos():
    line = pos.ask("DISPLAY,A,POSITION;").split(',')
    position = line[2].split(';')
    position = float(position[0])
    return position
def getposb():
    lineb = pos.ask("DISPLAY,B,POSITION;").split(',')
    positionb = lineb[2].split(';')
    positionb = float(positionb[0])
    return positionb
def getvel():
    movement_str = pos.ask("DISPLAY,ACTIVE;").split(',')
    velocity = movement_str[2].split(';')
    velocity = abs(float(velocity[0]))
    return velocity

#initialization of PNA
print pna.ask("*IDN?")                            #get the PNA info for reference
pna.write("SYST:FPReset")                         #factory preset
pna.write("DISPlay:WINDow:STATE ON")              #turn on a window for disp
#Setup S21 measurement aliased as MyMeas
pna.write("CALCulate:PARameter:DEFine:EXT 'MyMeas', S12")
pna.write("DISPlay:WINDow1:TRACe1:FEED 'MyMeas'") #FEED MyMeas to Trace 1 for display
#Set frequency params
pna.write("SENS1:FREQ:STAR "+fstart)
pna.write("SENS1:FREQ:STOP "+fstop)
pna.write("SENS1:SWE:POIN "+npts)
#select measurement
pna.write("CALC:PAR:SEL 'MyMeas'")

#initialization of positioner
pos.write("ASYNCHRONOUS;")  #allow for commands on the pos. while turning
pos.write("PRIMARY,A;")
pos.write("SCALE,A,360;")   #set scale to 360, might let this be a free param
pos.write("WINDOW,A,001.50;")
pos.write("WINDOW,B,001.50;")

position = getpos()   
if position < 5 or position > 355 :
    pos.write("MOVE,A,CWGO,010.00;")
    time.sleep(5)      
temp = 361                  #out of bounds value for angle, used to intialize while loop below
if position >= 180:         #go via shortest path to the start position
    print "position greater than 180"
    pos.write("MOVE,A,CWCHECK,"+start+";")    #<- add start pos. here
    while getvel() == 0:
        niente = 0
    while getvel() != 0:
        time.sleep(5)
        print "Initializing turntable position"
#    while getpos() != temp:
#        time.sleep(5)
#        temp = getpos()
#        print "Initializing turntable position"
else:
    print "position less than 180"
    pos.write("MOVE,A,CCWCHECK,"+start+";")  
    while getvel() == 0:
        niente = 0
        print "Vel = 0"
    while getvel() != 0:
        time.sleep(5)
        print "Initializing turntable position"
#    while getpos() != temp:  
#        time.sleep(5)
#        temp = getpos()
#        print "Initializing turntable position"
        
#SET POLARIZATION ON SGH
print "Setting SGH polarization"
pos.write("SCALE,B,360;")
pos.write("PRIMARY,B;")
position = getposb()
if pol == 'H':
    print "H-pol"
    if position >= 0 or position <= 180:         #go via shortest path to the start position
        pos.write("MOVE,B,CCWCHECK,000.00;")    #<- add start pos. here
        while getvel() == 0:
            niente = 0
        while getvel() != 0:
            time.sleep(5)
            print "Initializing gainhorn position"       
    else:
        pos.write("MOVE,B,CWCHECK,000.00")    
        while getvel() == 0:
            niente = 0
        while getvel() != 0:
            time.sleep(5)
            print "Initializing gainhorn position"
         
if pol == 'V':
    print "V-pol"
    if position >= 90 or position <= 270:         #go via shortest path to the start position
        pos.write("MOVE,B,CCWCHECK,090.00;")    #<- add start pos. here
        while getvel() == 0:
            niente = 0
        while getvel() != 0:
            time.sleep(5)
            print "Initializing gainhorn position"     
    else:
        pos.write("MOVE,B,CWCHECK,090.00") 
        while getvel() == 0:
            niente = 0
        while getvel() != 0:
            time.sleep(5)
            print "Initializing gainhorn position"

pos.write("PRIMARY,A;")
print "STARTING MEASUREMENT: SEE FIGURE 1"
#time.sleep(3)
#pos.write("PRIMARY,A;")

#PREPARE FOR ACQUISITION
ind = 0     #intializing angle and data indeces
ANG = []    #take initial angle meas
ANG.append(getpos()) 
s21 = []    #take intial S meas
junk = pna.ask("CALCulate:DATA? SDATA").split(',')   #have the analyzer write the measurement to the buffer
s21.append(pna.ask("CALCulate:DATA? SDATA").split(','))   #why do we have to do this twice???

#SET TRAVEL VELOCITY
stopflag = 0
pos.write("VELOCITY,A,003.00;")

#INITIALIZE QUICKPLOT FIGURE
ion()
figure(figsize = (8,5))
xlim([0,360])
ylim([-100,0])
qpobj, = plot(0,0)
QPx = []
QPy = []
title('Uncalibrated Pattern Data')
ylabel('Thru power, dB')
xlabel('Rotation, deg')


#START MOTION
pos.write("MOVE,A,CWGO,"+stop+";")        #format this for stop angle
while getpos() == ANG[ind]:
     dummy = 1                         #pause for positioner to start
while getpos() != ANG[ind]:             #motion check loop
    while getpos() <= ANG[ind]+float(ares):        #between measurements loop
        if abs(getpos()-float(stop))<=1:             #escape procedure for end <- add stop here
            stopflag = 1
            break        
    ind =ind+1    
    if stopflag:
        break
                                        #get net measurement set from analyzer
    s21.append(pna.ask("CALCulate:DATA? SDATA").split(','))
    ANG.append(getpos())
    
                                        #take off one data point for quickplot
    line = s21[ind]
    qp = 20*numpy.log10(abs(complex(float(line[0]),float(line[0]))))
    QPx.append(ANG[ind])
    QPy.append(qp)
    qpobj.set_ydata(QPy)
    qpobj.set_xdata(QPx)          # update the data on quickplot
    draw()                        # redraw the canvas
    pause(0.01)                   #locks up w/o pause

#CONVERT COLLECTED DATA INTO R+jI form
print "Acquisition complete\n Converting output data"
S21 = numpy.empty([len(s21),float(npts)],dtype = complex)
for ind in range(len(s21)):
    line = s21[ind]
    for i in range(int(len(line)/2)):
        S21[ind,i] =complex(float(line[2*i]),float(line[2*i+1]))

#APPEND PROJECT FILE
print 'Logging measurement in project file'
fid = open(project + '.txt',"a")
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
fid.write(st+"\n")
fid.write("\tDatafile: " + datafile+"\n")
fid.write("\tFrequency: "+fstart+" - "+fstop+", "+npts+" points\n")
fid.write("\tRotation: "+start+"-"+stop+" degrees, approx "+ares+" degree resolution\n")
fid.write('\tPolarization: ' + pol+"\n")
fid.write(comments+'\n\n')
fid.close()    

#SAVE DATA IN MAT FORMAT
freq = numpy.linspace(float(fstart),float(fstop),npts)
filename = datafile+".mat"
sio.savemat(filename,{'S21':S21, 'f':freq, 'angle':ANG})



#CLEAN UP
ioff()
show()      # redraw the canvas