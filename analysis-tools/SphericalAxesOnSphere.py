# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 17:00:24 2014

@author: Brian Gibbons
"""
import numpy as np
from numpy import pi
import CoorSysUtils as cs
import mayavi.mlab as mlab  # Note: importing Mayavi is slow, ~5-8 seconds

theta = np.linspace(0, pi, 20)
phi = np.linspace(0, 2*pi, 1 + 2**5)

gtheta, gphi = np.meshgrid(theta, phi)
rPattern = np.ones_like(gtheta)

x, y, z = cs.sph2cart(rPattern, gtheta, gphi)
vec_r_x, vec_r_y, vec_r_z = cs.cartPtSphR(x, y, z)
vec_t_x, vec_t_y, vec_t_z = cs.cartPtSphTheta(x, y, z)
vec_p_x, vec_p_y, vec_p_z = cs.cartPtSphPhi(x, y, z)

mlab.quiver3d(x, y, z, vec_r_x, vec_r_y, vec_r_z, \
                color=(1,0,0), scale_factor = 0.1) # r-hat in red
mlab.quiver3d(x, y, z, vec_t_x, vec_t_y, vec_t_z, \
                color=(0,1,0), scale_factor = 0.1) # theta-hat in green
mlab.quiver3d(x, y, z, vec_p_x, vec_p_y, vec_p_z, \
                color=(0,0,1), scale_factor = 0.1) # phi-hat in blue
mlab.show()
