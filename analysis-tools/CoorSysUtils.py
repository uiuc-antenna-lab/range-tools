# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 17:01:29 2014

@author: Brian Gibbons
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
    """ Return all three Cartesian components of the spherical vector r-hat at
        the point (x,y,z).
    """
    from numpy import sqrt
    mag = sqrt(x**2 + y**2 + z**2)
    return [x/mag, y/mag, z/mag]

def cartPtSphTheta(x, y, z):
    """ Return all three Cartesian components of the spherical vector
        theta-hat at the point (x,y,z).
    """
    from numpy import sin, cos, sqrt
    mag = sqrt(x**2 + y**2 + z**2)
    r, t, p = cart2sph(x/mag, y/mag, z/mag)
    return [cos(t)*cos(p), cos(t)*sin(p), -sin(t)]

def cartPtSphPhi(x, y, z):
    """ Return all three Cartesian components of the spherical vector
        phi-hat at the point (x,y,z).
    """
    from numpy import sin, cos, sqrt, zeros_like
    mag = sqrt(x**2 + y**2 + z**2)
    r, t, p = cart2sph(x/mag, y/mag, z/mag)
    return [-sin(p), cos(p), zeros_like(p)]

# TODO: Update function strings
def cartPtSphRx(x, y, z):
    """ Return Cartesian x component of the spherical vector r-hat at
        the point (x,y,z).
    """
    from numpy import sqrt
    mag = sqrt(x**2 + y**2 + z**2)
    return x/mag

def cartPtSphRy(x, y, z):
    """ Return Cartesian y component of the spherical vector r-hat at
        the point (x,y,z).
    """
    from numpy import sqrt
    mag = sqrt(x**2 + y**2 + z**2)
    return y/mag

def cartPtSphRz(x, y, z):
    """ Return Cartesian z component of the spherical vector r-hat at
        the point (x,y,z).
    """
    from numpy import sqrt
    mag = sqrt(x**2 + y**2 + z**2)
    return z/mag

def cartPtSphThetax(x, y, z):
    """ Return Cartesian x component of the spherical vector theta-hat at
        the point (x,y,z).
    """
    from numpy import cos, sqrt
    mag = sqrt(x**2 + y**2 + z**2)
    r, t, p = cart2sph(x/mag, y/mag, z/mag)
    return cos(t)*cos(p)

def cartPtSphThetay(x, y, z):
    """ Return Cartesian y component of the spherical vector theta-hat at
        the point (x,y,z).
    """
    from numpy import sin, cos, sqrt
    mag = sqrt(x**2 + y**2 + z**2)
    r, t, p = cart2sph(x/mag, y/mag, z/mag)
    return cos(t)*sin(p)

def cartPtSphThetaz(x, y, z):
    """ Return Cartesian z component of the spherical vector theta-hat at
        the point (x,y,z).
    """
    from numpy import sin, sqrt
    mag = sqrt(x**2 + y**2 + z**2)
    r, t, p = cart2sph(x/mag, y/mag, z/mag)
    return -sin(t)

def cartPtSphPhix(x, y, z):
    """ Return Cartesian x component of the spherical vector phi-hat at
        the point (x,y,z).
    """
    from numpy import sin, sqrt
    mag = sqrt(x**2 + y**2 + z**2)
    r, t, p = cart2sph(x/mag, y/mag, z/mag)
    return -sin(p)

def cartPtSphPhiy(x, y, z):
    """ Return Cartesian y component of the spherical vector phi-hat at
        the point (x,y,z).
    """
    from numpy import cos, sqrt
    mag = sqrt(x**2 + y**2 + z**2)
    r, t, p = cart2sph(x/mag, y/mag, z/mag)
    return cos(p)

def cartPtSphPhiz(x, y, z):
    """ Return Cartesian z component of the spherical vector phi-hat at
        the point (x,y,z).
    """
    from numpy import zeros_like
    return zeros_like(x)
