# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 15:17:30 2014

@author: Brian Gibbons

Hertzian dipole field expressions from Jin's "Theory and Computation of Electromagnetic Fields"
"""

from numpy import exp, sin, cos, pi

def HertzianDipole_Er(r, theta, k, eta, I, l):
    """
    Return radial component of the electric field of a Hertzian (or
    infinitesimal, or ideal) dipole. The dipole length l should be small and
    theta should be in radians.
    """
    return ((eta*I*l*cos(theta))/(2*pi*r**2)) * (1 + 1.0/(1j*k*r)) * exp(-1j*k*r)


def HertzianDipole_Etheta(r, theta, k, eta, I, l):
    """
    Return theta component of the electric field of a Hertzian (or
    infinitesimal, or ideal) dipole. The dipole length l should be small and
    theta should be in radians.
    """
    return ((1j*k*eta*I*l*sin(theta))/(4*pi*r)) * (1 + 1.0/(1j*k*r) - 1.0/((k*r)**2)) * exp(-1j*k*r)


def HertzianDipole_Hphi(r, theta, k, eta, I, l):
    """
    Return phi component of the magnetic field of a Hertzian (or
    infinitesimal, or ideal) dipole. The dipole length l should be small and
    theta should be in radians.
    """
    return ((1j*k*I*l*sin(theta))/(4*pi*r)) * (1 + 1.0/(1j*k*r)) * exp(-1j*k*r)


def HertzianDipoleFF_Etheta(r, theta, k, eta, I, l):
    """
    Return far-field theta component of the electric field of a Hertzian (or
    infinitesimal, or ideal) dipole. The dipole length l should be small,
    theta should be in radians, and k*r >> 1 (far-field approximation).
    """
    return ((1j*k*eta*I*l*sin(theta))/(4*pi*r)) * exp(-1j*k*r)


def HertzianDipoleFF_Hphi(r, theta, k, eta, I, l):
    """
    Return far-field phi component of the magnetic field of a Hertzian (or
    infinitesimal, or ideal) dipole. The dipole length l should be small,
    theta should be in radians, and k*r >> 1 (far-field approximation).
    """
    return ((1j*k*I*l*sin(theta))/(4*pi*r)) * exp(-1j*k*r)
