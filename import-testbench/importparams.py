# -*- coding: utf-8 -*-
"""
Created on Sat Sep 07 14:39:28 2013

@author: Kurt
"""


import time, datetime

#Open init file
fid = open('rangeinit.txt','r')
fid.readline()
fid.readline()
fid.readline()
project = fid.readline().split()[2]
datafile = fid.readline().split()[2]
log = fid.readline().split()[2]
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
stop = fid.readline().split()[2]
fid.readline()
fid.readline()
comments = fid.read()
fid.close()

#Append project file
print 'Logging measurement'
fid = open(project + '.txt',"a")
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
fid.write(st+"\n")
fid.write("\tDatafile: " + datafile+"\n")
fid.write("\tFrequency: "+fstart+" - "+fstop+", "+npts+" points\n")
fid.write("\tRotation: 0-"+stop+" degrees, approx "+ares+" degree resolution\n")
fid.write('\tPolarization: ' + pol+"\n")
fid.write(comments+'\n\n')
fid.close()    
