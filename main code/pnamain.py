# -*- coding: utf-8 -*-
"""
Created on Fri Sep 06 14:30:23 2013

@author: Kurt
"""

import pyvisa, time, pylab
from visa import *

#PARAMETERS THAT MIGHT CHANGE
fmin = "1GHz"
fmax = "2GHz"
nf = "100"
ares = 1.0
stopflag = 0

start = 0
stop = 360
#freq = linspace(fmin,fmax,nf)

#VISA reference locations
PNAref = 'GPIB0::16'
POSref = 'GPIB0::17'

#create instrument objects
pna = instrument(PNAref)
pos = instrument(POSref)

def getpos():
    line = pos.ask("DISPLAY,A,POSITION;").split(',')
    position = line[2].split(';')
    position = float(position[0])
    return position

#initialization of PNA
print pna.ask("*IDN?")                                  #get the PNA info for reference
pna.write("SYST:FPReset")                         #factory preset
pna.write("DISPlay:WINDow:STATE ON")              #turn on a window for disp
#Setup S21 measurement aliased as MyMeas
pna.write("CALCulate:PARameter:DEFine:EXT 'MyMeas', S12")
pna.write("DISPlay:WINDow1:TRACe1:FEED 'MyMeas'")         #FEED MyMeas to Trace 1 for display
#Set frequency params
pna.write("SENS1:FREQ:STAR "+fmin)
pna.write("SENS1:FREQ:STOP "+fmax)
pna.write("SENS1:SWE:POIN "+nf)
#select measurement
pna.write("CALC:PAR:SEL 'MyMeas'")

#initialization of positioner
pos.write("ASYNCHRONOUS;")
pos.write("SCALE,A,360;")
position = getpos()
temp = 361
if position >= 180:
    pos.write("MOVE,A,CWGO,000.00;")
    while getpos() != temp:
        time.sleep(5)
        temp = getpos()
        print "Initializing turntable position"
else:
    pos.write("MOVE,A,CCWGO,000.00;")    
    while getpos() != temp:  
        time.sleep(5)
        temp = getpos()
        print "Initializing turntable position"

ind = 0     #intializing angle and data indeces
ANG = []    #take initial angle meas
ANG.append(getpos()) 

s21 = []    #take intial S meas
junk = pna.ask("CALCulate:DATA? SDATA").split(',')   #have the analyzer write the measurement to the buffer
s21.append(pna.ask("CALCulate:DATA? SDATA").split(','))   #why do we have to do this twice???

#Set travel velocity and start motion 
pos.write("VELOCITY,A,001.00;")
pos.write("MOVE,A,CWGO,090.00;")
time.sleep(2)
while getpos() != ANG[ind]:    
    while getpos() <= ANG[ind]+ares:
        fun = 'hi!'
        if abs(getpos()-90)<=1:
            stopflag = 1
            break        
    ind =ind+1    
    if stopflag:
        break
    
    s21.append(pna.ask("CALCulate:DATA? SDATA").split(','))
    ANG.append(getpos())
    print(ANG[ind])

S21 = numpy.empty([len(s21),float(nf)],dtype = complex)
for ind in range(len(s21)):
    line = s21[ind]
    for i in range(int(len(line)/2)):
        S21[ind,i] =complex(float(line[2*i]),float(line[2*i+1]))
    



#
##collect data
#junk = pna.ask("CALCulate:DATA? SDATA").split(',')   #have the analyzer write the measurement to the buffer
#s21 = pna.ask("CALCulate:DATA? SDATA").split(',')   #why do we have to do this twice???
#
#
#    
#"""
#set up asynch on pos
#
#
#S21 = []
#for i in range(int(len(s21)/2)):
#    S21.append(complex(float(s21[2*i]),float(s21[2*i+1])))
