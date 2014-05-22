# -*- coding: utf-8 -*-
"""
Created on Thu May 22 13:36:13 2014

@author: Brian Gibbons
"""
import numpy as np

def GetSGHDataArray(CSVfilename, delimiter = ',', freqUnit = 1.0):
    import csv
    caldatafile = open(CSVfilename, mode = 'r')
    caldata = csv.reader(caldatafile, delimiter = delimiter)
    
    data = []
    for row in caldata:
        freq = freqUnit * np.float(row[0]) # Frequency point
        gain = np.float(row[1]) # Gain at this frequency, in dBi
        data.append((freq, gain))
    
    caldatafile.close()
    
    return np.array(data)


def GetGainAt(freq, SGHDataArray):
    freqData = SGHDataArray[:, 0]
    gainData = SGHDataArray[:, 1]
    if (not np.all(np.diff(freqData) > 0)): # freq not sorted in ascending order
        sortI = np.argsort(freqData)
        freqData = freqData[sortI]
        gainData = gainData[sortI]
    
    if ((np.min(freq) < np.min(freqData)) or (np.max(freq) > np.max(freqData))):
        print("WARNING: One or more requested frequency points lie outside")
        print("         the domain of the calibration data. Endpoint values")
        print("         for these frequencies will be returned (i.e. ")
        print("         extrapolation will NOT be done).")
        print("         Limits of calibration data = [{:.3g}, {:.3g}]".format(np.min(freqData), np.max(freqData)))
        print("         Limits of requested values = [{:.3g}, {:.3g}]".format(np.min(freq), np.max(freq)))
    
    return np.interp(freq, freqData, gainData)


def GetCalAdjust(freqData, calData, SGHDataArray, calDataAsPower = False):
    calDataMag = np.abs(calData)
    calDataPhase = np.angle(calData, deg = True)
    
    if (calDataAsPower):
        dBbase = 10.0
    else:
        dBbase = 20.0
    calDataMagdB = dBbase * np.log10(calDataMag)
    
    SGHGaindB = GetGainAt(freqData, SGHDataArray)
    
    calAdjustMag = calDataMagdB - SGHGaindB
    calAdjust = np.vstack((calAdjustMag, calDataPhase)).T
    
    return calAdjust


def GetAbsGain(data, calAdjust, dataAsPower = False, dBminVal = -120):
    if (dataAsPower):
        dBbase = 10.0
    else:
        dBbase = 20.0
    dataMag = dBbase * np.log10(np.abs(data))
    dataPhase = np.angle(data, deg = True)
    
    dataMag = np.where(dataMag < dBminVal, dBminVal, dataMag)
    
    dataMag -= calAdjust[:, 0]
    dataPhase -= calAdjust[:, 1]
    
#    d = np.vstack((dataMag, dataPhase)).T
#    
#    d -= calAdjust        
    
    return [dataMag, dataPhase]