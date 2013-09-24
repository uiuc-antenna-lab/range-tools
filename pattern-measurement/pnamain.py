# -*- coding: utf-8 -*-
"""
Created on Fri Sep 06 14:30:23 2013

@author: Kurt
"""

import numpy, pyvisa, time, datetime, pylab
import scipy.io as sio
from visa import *

#LOAD IN TEST PARAMETERS FROM TEXT FILE
fid = open('rangeinit.txt','r')
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
position = getpos()         
temp = 361                  #out of bounds value for angle, used to intialize while loop below
if position >= 180:         #go via shortest path to the start position
    pos.write("MOVE,A,CWGO,"+start+";")    #<- add start pos. here
    while getpos() != temp:
        time.sleep(5)
        temp = getpos()
        print "Initializing turntable position"
else:
    pos.write("MOVE,A,CCWGO,"+start+";")    
    while getpos() != temp:  
        time.sleep(5)
        temp = getpos()
        print "Initializing turntable position"
        
#SET POLARIZATION ON SGH
print "Setting SGH polarization"
pos.write("SCALE,B,360;")
pos.write("PRIMARY,B;")
temp = getpos()
position = getpos()
if pol == 'H':
    print "H-pol"
    if position >= 0 or position <= 180:         #go via shortest path to the start position
        pos.write("MOVE,B,CCWGO,000.00;")    #<- add start pos. here
        raw_input('wait for positioner to stop and then press enter')        
#        while getpos() != temp:
#            time.sleep(1)
#            temp = getpos()            
    else:
        pos.write("MOVE,B,CWGO,000.00")    
        raw_input('wait for positioner to stop and then press enter')
#        while getpos() != temp:  
#            time.sleep(1)
#            temp = getpos()
         
if pol == 'V':
    print "V-pol"
    if position >= 90 or position <= 270:         #go via shortest path to the start position
        pos.write("MOVE,B,CWGO,090.00;")    #<- add start pos. here
        raw_input('wait for positioner to stop and then press enter')        
#        while getpos() != temp:
#            time.sleep(1)
#            temp = getpos()            
    else:
        pos.write("MOVE,B,CCWGO,090.00") 
        raw_input('wait for positioner to stop and then press enter')
#        while getpos() != temp:  
#            time.sleep(1)
#            temp = getpos()

pos.write("PRIMARY,A;")
time.sleep(3)
pos.write("PRIMARY,A;")

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
    print ANG[ind]

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

#PLOT PATTERN
splot = 20*numpy.log10(abs(S21[:,0]))
#plot(ANG,splot)