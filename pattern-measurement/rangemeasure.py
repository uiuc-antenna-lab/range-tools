# -*- coding: utf-8 -*-
"""
Created on Fri Sep 06 14:30:23 2013
Updated on: Tue Dec 10 2013
@author: Kurt
@author: Robert A. Scott
@author: Brian Gibbons
"""
#python initialization files
import sys
import numpy, pyvisa, time, datetime
from pylab import *
import scipy.io as sio
from visa import *
import warnings
warnings.filterwarnings("ignore")
from cmdfileparser import CmdfileParser

print '\n'
print "pattern-measurement  v. 0.8"
print('Reading "{0}"'.format(sys.argv[1]))

"""
Reading in measurement file data
"""
# Initialize variables; use 'UNSET' for ones that MUST be set, and whatever
# default value is desired for ones that MAY be set
project = 'UNSET'
datafile = 'UNSET'
option = 'UNSET'
power = 'default'
fstart = 'UNSET'
fstop = 'UNSET'
fcenter = 'UNSET'
fbandwidth = 'UNSET'
npts = 'UNSET'
pol = 'UNSET'
ares = 'UNSET'
start = 'UNSET'
stop = 'UNSET'
comments = ''

#LOAD IN TEST PARAMETERS FROM TEXT FILE
parser = CmdfileParser()
finput = open(sys.argv[1],'r')
ftext = finput.read()   # Read in entire file to string
finput.close()
results = parser.parse(ftext)
locals().update(results) # Use returned dictionary of parsed values to update the local variables

print('\nParameters')
print('----------')
print('project = "{0}"'.format(project))
print('datafile = "{0}"'.format(datafile))
print('option = "{0}"'.format(option))
if not isinstance(power, str): # Assume number, print it nicely
    print('power = {0:+} dBm'.format(power))    # Explicitly include signs
else:
    if power == "default":
        print('power = default (-17 dBm)')
    else:
        print('ERROR: unknown power setting "{0}"'.format(power))
        # TODO: throw exception here
if not isinstance(fstart, str): # Assume number, print it nicely 
    print('fstart = {0:g} Hz'.format(fstart))
else:
    print('fstart = ' + fstart) # Presumably fstart is the string 'UNSET'
    
if not isinstance(fstop, str):
    print('fstop = {0:g} Hz'.format(fstop))
else:
    print('fstop = ' + fstop)
    
if not isinstance(fcenter, str):
    print('fcenter = {0:g} Hz'.format(fcenter))
else:
    print('fcenter = ' + fcenter)
    
if not isinstance(fbandwidth, str):
    print('fbandwidth = {0:g} Hz'.format(fbandwidth))
else:
    print('fbandwidth = ' + fbandwidth)
    
print('npts = ' + str(npts))
print('pol = "' + pol + '"')
print('ares = {0} deg'.format(ares))
print('start = {0} deg'.format(start))
print('stop = {0} deg'.format(stop))
print('comments = "' + comments + '"')

errorMsg = ""
if project == 'UNSET':
    errorMsg = errorMsg + '"project" variable unset.\n'
if datafile == 'UNSET':
    errorMsg = errorMsg + '"datafile" variable unset.\n'
if option == 'UNSET':
    errorMsg = errorMsg + '"option" variable unset.\n'
if ((fstart == 'UNSET') or (fstop == 'UNSET'))          \
    and ((fcenter == 'UNSET') or (fbandwidth == 'UNSET')):
    errorMsg = errorMsg + 'Frequency variables unset (fstart and fstop, or fcenter and fbandwidth).\n'
if npts == 'UNSET':
    errorMsg = errorMsg + '"npts" variable unset.\n'
if pol == 'UNSET':
    errorMsg = errorMsg + '"pol" variable unset.\n'
if ares == 'UNSET':
    errorMsg = errorMsg + '"ares" variable unset.\n'
if start == 'UNSET':
    errorMsg = errorMsg + '"start" variable unset.\n'
if stop == 'UNSET':
    errorMsg = errorMsg + '"stop" variable unset.\n'
if comments == "":
    print("Comments are not set. This is not recommended.\n")

if errorMsg != "":
    print("ERROR(S):\n" + errorMsg)
    # TODO: Throw excepction here
#    sys.exit("ERROR(S):\n" + errorMsg)

# Compute start and stop frequencies if fcenter and fbandwidth given
if ((fstart == 'UNSET') or (fstop == 'UNSET')):
    if (not (fstart == 'UNSET')) or (not (fstop == 'UNSET')):
        print("\nWARNING: fstart or fstop have been specified but won't be used.")
    fstart = fcenter - fbandwidth/2.0
    fstop  = fcenter + fbandwidth/2.0
    print("\nComputing fstart and fstop based on fcenter and fbandwidth:")
    print("fstart = {0:g} Hz\nfstop = {1:g} Hz\n".format(fstart, fstop))
else: # fstart and fstop both given, use those
    if not ((fcenter == 'UNSET') and (fbandwidth == 'UNSET')):
        print("WARNING: fcenter and/or fbandwidth have been specified but won't be used.")
        # TODO: Put in a better warning here?

# TODO: Test file paths for missing directories; either create them or throw an exception now (not at the end of the program after data has been taken)

# TODO: Test to make sure we're not overwriting any files. If so, raise a warning (and prompt?)


"""
Setting up GPIB connection parameters
"""
#VISA reference locations -- store these to a file?
PNAref = 'GPIB0::16'
POSref = 'GPIB0::17'

#create instrument objects
pna = instrument(PNAref)
pos = instrument(POSref)

#setting the window on the positioner
pos.clear()
pos.write("WINDOW,A,001.00;")
pos.write("WINDOW,B,001.00;")

"""
Function definitions
"""

#function to grab window parameter of axis(sel) -used in needinit()
def getwindow(sel):
    window = pos.ask("DISPLAY,"+sel+",WINDOW;").split(',')
    window = window[2].split(';')
    window = float(window[0])
    return window
    
#function to grab current turntable location from positioner
def getpos(sel):
    line = pos.ask("DISPLAY,"+sel+",POSITION;").split(',')
    position = line[2].split(';')
    position = float(position[0])
    return position

#function used to grab the current velocity of the avtive axis
def getvel():
    movement_str = pos.ask("DISPLAY,ACTIVE;").split(',')
    velocity = movement_str[2].split(';')
    velocity = abs(float(velocity[0]))
    return velocity 

#function to determine whether or not a positioner element needs initialization
def needinit(sel):
    inita = 0
    initb = 0
    if sel == 'A':   # Element A (chamber table) 
        positiona = getpos(sel)
        windowa = getwindow(sel)
        if abs(positiona - float(start)) > windowa:
            inita=1
        return inita
    else:            # Element B (Signal Antenna)
        positionb = getpos(sel)
        windowb = getwindow(sel)
        if pol == 'V': #if the polarization is V or H
            bstart = "270.00"
        else:
            bstart = "000.00"
        if abs(positionb - float(bstart)) > windowb:
            initb=1
        return initb

#functin to show the user the progress of the measurement
def drawProgressBar(percent, barLen = 20):
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()
  
  
"""
Positioner position initialization
PNA initialization
"""
  
#initialization of PNA
print "Intializing communication with network analyzer",
pna.ask("*IDN?")                            #get the PNA info for reference
print ". . . Complete"

pna.write("SYST:FPReset")                   #factory preset
pna.write("DISPlay:WINDow:STATE ON")        #turn on a window for disp

#Setup S12 measurement aliased as MyMeas
pna.write("CALCulate:PARameter:DEFine:EXT 'MyMeas', S12")
pna.write("DISPlay:WINDow1:TRACe1:FEED 'MyMeas'")  #FEED MyMeas to Trace 1 for display

#Set frequency params
pna.write("SENS1:FREQ:STAR "+str(fstart))
pna.write("SENS1:FREQ:STOP "+str(fstop))
pna.write("SENS1:SWE:POIN "+str(npts))
pna.write("SENS1:SWE:TIME .05")

#Set power level
if power != 'default':
    pna.write("SOUR:POW2 "+str(power))

#select measurement
pna.write("CALC:PAR:SEL 'MyMeas'")
  
#initialization of positioner, bypass if sgh option used
if option != 'sgh':
    pos.write("ASYNCHRONOUS;")  #allow for commands on the pos. while turning
    pos.write("PRIMARY,A;")     #setting A as the primary axis
    pos.write("SCALE,A,360;")   #set scale to 360, might let this be a free param
    pos.write("VELOCITY,A,003.00;")
    
    position = getpos('A')
    if needinit('A'):
        if position >= 180:         #go via shortest path to the start position
            pos.write("MOVE,A,CWCHECK,"+str(start)+";")    #<- add start pos. here
            time.sleep(2)        
            print "Moving to initial turntable position", 
            while getvel() != 0:
                time.sleep(2)
                print ".",
            print "Complete"

        else:
            pos.write("MOVE,A,CCWCHECK,"+str(start)+";") 
            time.sleep(2) 
            print "Moving to intial turntable position", 
            while getvel() != 0:
                time.sleep(2)
                print ".", 
            print "Complete"

        
#SET POLARIZATION ON SGH -- do regardless of sgh or real measurement?  issues w/ movement?
print "Setting Rx SGH polarization to",
pos.write("PRIMARY,B;")                     #selecting 'B' axis to be primary
pos.write("SCALE,B,360;")                   #changing the scale of the 'B' axis to 360
pos.write("VELOCITY,B,007.50;")
position = getpos('B')

if pol == 'H':
    print "horizontal",
    init=needinit('B')
    if init:
        if position >= 0 or position <= 180:         #go via shortest path to the start position
            pos.write("MOVE,B,CWCHECK,000.00;")    #<- add start pos. here
            time.sleep(2) 
            #print "Initializing gainhorn position", 
            while getvel() != 0:
                print ".",
                time.sleep(2)
            print "Complete"
        else:
            pos.write("MOVE,B,CCWCHECK,000.00")    
            time.sleep(2) 
            #print "Initializing gainhorn position",
            while getvel() != 0:
                print ".",
                time.sleep(2)
            print "Complete"
    else:
        print ". . Complete"
         
if pol == 'V':
    print "vertical",
    init = needinit('B')
    if init:
        if position >= 90 or position <= 270:         #go via shortest path to the start position
            pos.write("MOVE,B,CCWCHECK,270.00;")    #<- add start pos. here
            time.sleep(2)       
            #print "Initializing gainhorn position", 
            while getvel() != 0:
                print ".",  
                time.sleep(2)                
            print "Complete"   
        else:
            pos.write("MOVE,B,CWCHECK,270.00") 
            time.sleep(2) 
            #print"Initializing gainhorn position", 
            while getvel() != 0:
                print ".",  
                time.sleep(2) 
            print "Complete"
    else:
        print ". . Complete"


pos.write("PRIMARY,A;")               #moving primary back to 'A' axis
time.sleep(2)


"""
Measurement Magic
"""
#PREPARE FOR ACQUISITION
ind = 0     #intializing angle and data indeces
ANG = []    #take initial angle meas
ANG.append(getpos('A')) 
s12 = []    #take intial S meas
junk = pna.ask("CALCulate:DATA? SDATA").split(',')   #have the analyzer write the measurement to the buffer
s12.append(pna.ask("CALCulate:DATA? SDATA").split(','))   #why do we have to do this twice???

#SET TRAVEL VELOCITY
stopflag = 0
pos.write("VELOCITY,A,003.00;")

#MAIN ACQUISITION LOOP
if option != 'sgh':  #if not in sgh mode, do full measurement
    pos.write("MOVE,A,CWGO,"+str(stop)+";")        #format this for stop angle
    print "Running pattern measurement"
    time.sleep(2)

    #INITIALIZE QUICKPLOT FIGURE
    ion()
    figure(figsize = (8,5))
    xlim([0,360])
    ylim([-100,0])
    qpobj, = plot(0,0)
    QPx = []
    QPy = []
    title('Uncalibrated Pattern Data '+str(fstart)+' Hz')
    ylabel('Thru power, dB')
    xlabel('Rotation, deg')

                      #pause for positioner to start
    while getvel() != 0:             #motion check loop
        while getpos('A') <= ANG[ind]+float(ares):        #between measurements loop
            if abs(getpos('A')-float(stop))<=1 or abs(getpos('A')-float(stop))>=359:             #escape procedure for end <- add stop here
                stopflag = 1
                break        
        ind =ind+1    
        if stopflag:
            break
                                        #get net measurement set from analyzer
        s12.append(pna.ask("CALCulate:DATA? SDATA").split(','))
        ANG.append(getpos('A'))
        
                                        #take off one data point for quickplot
        line = s12[ind]
        qp = 20*numpy.log10(abs(complex(float(line[0]),float(line[1]))))
        QPx.append(ANG[ind])
        QPy.append(qp)
        qpobj.set_ydata(QPy)
        qpobj.set_xdata(QPx)            # update the data on quickplot
        draw()                          # redraw the canvas
        
        
        drawProgressBar(ANG[ind]/float(stop))
        pause(0.001)                   #locks up w/o pause

else:   #if sgh mode, take a single measurement with no movement
    print "Taking standard gain horn measurement"
    s12.append(pna.ask("CALCulate:DATA? SDATA").split(','))
    
drawProgressBar(1);print "\n"

#CONVERT COLLECTED DATA INTO R+jI form
print "Converting output data"
S12 = numpy.empty([len(s12),float(npts)],dtype = complex)
for ind in range(len(s12)):
    line = s12[ind]
    for i in range(int(len(line)/2)):
        S12[ind,i] =complex(float(line[2*i]),float(line[2*i+1]))

#APPEND PROJECT FILE
print 'Logging measurement in project file'
fid = open(project + '.txt',"a")
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
fid.write(st+"\n")
fid.write("\tDatafile: " + datafile+"\n")
fid.write("\tFrequency: "+str(fstart)+" - "+str(fstop)+", "+str(npts)+" points\n")
if option != 'sgh':
    fid.write("\tRotation: "+str(start)+"-"+str(stop)+" degrees, approx "+str(ares)+" degree resolution\n")
fid.write('\tPolarization: ' + str(pol)+"\n")
fid.write(comments+'\n\n')
fid.close()    

#SAVE DATA IN MAT FORMAT
freq = numpy.linspace(float(fstart),float(fstop),npts)
filename = datafile+".mat"
sio.savemat(filename,{'S12':S12, 'f':freq, 'angle':ANG})

#CLEAN UP
ioff()
show()      # redraw the canvas
