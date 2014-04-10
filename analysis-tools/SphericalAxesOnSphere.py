# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 17:00:24 2014

@author: brian
"""
import numpy as np
from numpy import pi
from CoorSysUtils import *
import mayavi.mlab as mlab  # Note: importing Mayavi is slow, ~5-8 seconds

r_scale = 1
theta = np.linspace(0, pi, 20)
phi = np.linspace(0, 2*pi, 1 + 2**5)

gtheta, gphi = np.meshgrid(theta, phi)
rPattern = np.ones_like(gtheta)
#rPattern = HertzianDipoleFF_Etheta(200, gtheta, k, eta0, I, l)


x, y, z = sph2cart(np.abs(rPattern), gtheta, gphi)
vec_r_x, vec_r_y, vec_r_z = cartPtSphR(x, y, z)
vec_t_x, vec_t_y, vec_t_z = cartPtSphTheta(x, y, z)
vec_p_x, vec_p_y, vec_p_z = cartPtSphPhi(x, y, z)


mlab.quiver3d(x, y, z, vec_r_x, vec_r_y, vec_r_z, color=(1,0,0)) # r in red
mlab.quiver3d(x, y, z, vec_t_x, vec_t_y, vec_t_z, color=(0,1,0)) # t in green
mlab.quiver3d(x, y, z, vec_p_x, vec_p_y, vec_p_z, color=(0,0,1)) # p in blue
mlab.show()