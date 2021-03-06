# -*- coding: utf-8 -*-
"""
Created on Fri Oct 04 13:31:28 2013

setpositioner.py 
        -a program to move the positioner to a given angular location

@author: Kurt
"""

import sys
import numpy, pyvisa, time, datetime
from pylab import *
import scipy.io as sio
from visa import *
import warnings
warnings.filterwarnings("ignore")
from positionerutils import *

POSref = 'GPIB0::17'
pos = instrument(POSref)

#setting the appropriate parameters on the positioner
pos.clear()
pos.write("WINDOW,A,001.00;")
pos.write("WINDOW,B,001.00;")    
pos.write("ASYNCHRONOUS;")  #allow for commands on the pos. while turning
pos.write("PRIMARY,A;")     #setting A as the primary axis
pos.write("SCALE,A,360;")   #set scale to 360, might let this be a free param
pos.write("VELOCITY,A,010.00;")

position = getpos('A')    
dest = sys.argv[1]
    
pos.write("MOVE,A,CWCHECK,"+dest+";")    #<- add start pos. here
time.sleep(2)        
print "Moving", 
while getvel() != 0:
    time.sleep(2)
    print ".",
print "Complete"

