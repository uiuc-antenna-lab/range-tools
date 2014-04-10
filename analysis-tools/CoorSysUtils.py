# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 17:01:29 2014

@author: brian
"""

def sph2cart(r, theta, phi):
    from numpy import sin, cos
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)
    return [x, y, z]

def cart2sph(x, y, z):
    from numpy import sqrt, arccos, arctan2
    r = sqrt(x**2 + y**2 + z**2)
    theta = arccos(z / r)
    phi = arctan2(y, x)
    return [r, theta, phi]

def cartPtSphR(x, y, z):
    """ Return (in Cartesian coordinates) the direction of the radial
        outward vector (r-hat in spherical coordinates) for the point (x,y,z)
    """
    from numpy import sqrt
    mag = sqrt(x**2 + y**2 + z**2)
    return [x/mag, y/mag, z/mag]

def cartPtSphTheta(x, y, z):
    """ Return (in Cartesian coordinates) the direction of the spherical
        coordinate theta-hat vector for the point (x,y,z)
    """
    from numpy import sin, cos, sqrt
    mag = sqrt(x**2 + y**2 + z**2)
    r, t, p = cart2sph(x/mag, y/mag, z/mag)
    return [cos(t)*cos(p), cos(t)*sin(p), -sin(t)]

def cartPtSphPhi(x, y, z):
    """ Return (in Cartesian coordinates) the direction of the spherical
        coordinate phi-hat vector for the point (x,y,z)
    """
    from numpy import sin, cos, sqrt, zeros_like
    mag = sqrt(x**2 + y**2 + z**2)
    r, t, p = cart2sph(x/mag, y/mag, z/mag)
    return [-sin(p), cos(p), zeros_like(p)]