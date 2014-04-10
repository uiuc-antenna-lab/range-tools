# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 15:47:32 2014

@author: Brian Gibbons
"""

import numpy as np
from HertzianDipoleFields import HertzianDipoleFF_Etheta, HertzianDipoleFF_Hphi
from CoorSysUtils import *
import mayavi.mlab as mlab

from numpy import pi, sqrt, zeros_like, ones_like
from scipy.constants import mu_0 as mu0
from scipy.constants import epsilon_0 as eps0

freq = 3e9 # [Hz]
w = 2 * pi * freq
k = w * sqrt(mu0 * eps0)
eta0 = sqrt(mu0 / eps0)
I = 1.0 # [A]
l = 1e-3 # [m]


#pattEt = HertzianDipoleFF_Etheta(200, theta, k, eta0, I, l)
#pattHp = HertzianDipoleFF_Hphi(200, theta, k, eta0, I, l)
#normEt = pattEt / np.max(np.abs(pattEt))
#normHp = pattHp / np.max(np.abs(pattHp))


#plt.polar((pi/2) - theta, np.abs(normEt), 'b.-') # Field plot
#plt.hold(True)
#plt.polar((pi/2) + theta, np.abs(normEt), 'b.-')
#plt.show()

r_scale = 1
theta = np.linspace(0, pi, 20)
phi = np.linspace(0, 2*pi, 1 + 2**5)

gtheta, gphi = np.meshgrid(theta, phi)
rPattern = ones_like(gtheta)
pattEt = HertzianDipoleFF_Etheta(200, gtheta, k, eta0, I, l)
normEt = pattEt / np.max(np.abs(pattEt))
realEt = np.real(pattEt) / np.max(np.real(pattEt))
imagEt = np.imag(pattEt) / np.max(np.imag(pattEt))
normAbsEt = np.abs(normEt)


## Plot E_theta vector on a sphere of constant radius
#x, y, z = sph2cart(rPattern, gtheta, gphi)
#vec_t_x, vec_t_y, vec_t_z = cartPtSphTheta(x, y, z) * normAbsEt
#mlab.quiver3d(x, y, z, vec_t_x, vec_t_y, vec_t_z, color=(0,1,0)) # t in green
#mlab.show()

## Plot theta-hat vector with radial position corresponding to pattern strength
#x, y, z = sph2cart(normAbsEt, gtheta, gphi)
#vec_t_x, vec_t_y, vec_t_z = cartPtSphTheta(x, y, z)
#mlab.quiver3d(x, y, z, vec_t_x, vec_t_y, vec_t_z, color=(0,1,0)) # t in green
#mlab.show()

# Plot pattern as a surface, with radial position corresponding to strength
x, y, z = sph2cart(normAbsEt, gtheta, gphi)
#x, y, z = sph2cart(realEt, gtheta, gphi)
mlab.mesh(x, y, z, scalars = normAbsEt, representation="surface")
mlab.show()

#vec_t_x, vec_t_y, vec_t_z = sph2cart(200*ones_like(pattEt), pattEt, zeros_like(pattEt))
#vec_r_x, vec_r_y, vec_r_z = cartPtSphR(x, y, z)

#vec_p_x, vec_p_y, vec_p_z = cartPtSphPhi(x, y, z)


#mlab.quiver3d(x, y, z, vec_r_x, vec_r_y, vec_r_z, color=(1,0,0)) # r in red

#mlab.quiver3d(x, y, z, vec_p_x, vec_p_y, vec_p_z, color=(0,0,1)) # p in blue


#mlab.points3d(x, y, z, mode = "sphere")#, scale_factor = 0.1)
#mlab.view(azimuth = 0, elevation = 0)
#mlab.show()



#s = np.ones(x.shape)
##obj = mlab.contour3d(x, y, z, s, contours=3)
##mlab.view(azimuth = 0, elevation = 0)
##mlab.show()
#
#x, y, z = np.mgrid[1:1:20j, 0:(pi):20j, -1:1:20j]
#r, theta, phi = cart2sph(x, y, z)
#
#
#
#mlab.view(azimuth = 0, elevation = 0)
#mlab.show()

#u =    np.sin(np.pi*x) * np.cos(np.pi*z)
#v = -2*np.sin(np.pi*y) * np.cos(2*np.pi*z)
#w = np.cos(np.pi*x)*np.sin(np.pi*z) + np.cos(np.pi*y)*np.sin(2*np.pi*z)


#fig = mlab.figure(1, size=(400, 400), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0)) # figure with white background
#mlab.quiver3d(u, v, w)
#mlab.outline()

# Code from http://blog.seljebu.no/2013/11/python-segfault-on-mayavi-masking/
# prevent segfault (malloc too large)
#vectors = fig.children[0].children[0].children[0]
#vectors.glyph.mask_points.maximum_number_of_points = 1000 # "Manually" set Maximum number of points
#vectors.glyph.mask_input_points = True # turn masking on

#src = mlab.pipeline.vector_field(u, v, w)
#mlab.pipeline.vectors(src, mask_points=20, scale_factor=3.)
#mlab.pipeline.vector_cut_plane(src, mask_points=2, scale_factor=3)

