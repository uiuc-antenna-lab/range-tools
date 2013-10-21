# Collection of functions and utilities related to the positioner
#
# KS
#
# Version 0.1 - October 20, 2013
#   -simply moved over positioner functions from rangemeasure


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