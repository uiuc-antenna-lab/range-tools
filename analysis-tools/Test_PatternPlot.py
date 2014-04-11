# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 15:25:01 2014

@author: Brian Gibbons
"""

from PatternPlot import PlotCutPlane2d
from HertzianDipoleFields import HertzianDipoleFF_Etheta as Etheta
import numpy as np
from numpy import pi, sqrt
from scipy.constants import epsilon_0 as eps0
from scipy.constants import mu_0 as mu0

freq = 3e9 # [Hz]
w = 2 * pi * freq
k = w * sqrt(mu0 * eps0)
eta0 = sqrt(mu0 / eps0)
I = 1.0 # [A]
l = 1e-3 # [m]

theta = np.linspace(0, pi, 200)
pattEt = Etheta(200, theta, k, eta0, I, l)
data = np.abs(pattEt / np.max(np.abs(pattEt)))

PlotCutPlane2d(data, "el", plotdB = True, dBminr = -40)
