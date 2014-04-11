# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 15:47:32 2014

@author: Brian Gibbons
"""
import numpy as np


def DemoPlot(case, thetaScale = 1.0, phiScale = 1.0j):
    from HertzianDipoleFields import HertzianDipoleFF_Etheta
    import CoorSysUtils as cs
    import mayavi.mlab as mlab
    
    from numpy import pi, sqrt, exp, ones_like, real, cos
    from scipy.constants import mu_0 as mu0
    from scipy.constants import epsilon_0 as eps0
    
    # Some setup
    freq = 3e9 # [Hz]
    w = 2 * pi * freq
    k = w * sqrt(mu0 * eps0)
    eta0 = sqrt(mu0 / eps0)
    I = 1.0 # [A]
    l = 1e-3 # [m]
    
    if (case == 1):
        print("Animated Polarization Demo")
        print("")
        print("You can configure the the type of polarization with")
        print("the values for thetaScale and phiScale. Complex numbers")
        print("may be used for circular or elliptical polarization.")
        print("")
        print("  thetaScale = {}, phiScale = {}".format(thetaScale, phiScale))

        theta = np.linspace(0, pi, 15)
        phi = np.linspace(0, 2*pi, 1 + 2**5)
        
        gtheta, gphi = np.meshgrid(theta, phi)
        rPattern = ones_like(gtheta)
        pattEt = HertzianDipoleFF_Etheta(200, gtheta, k, eta0, I, l)
            # 200 is just an arbitrary radial distance away from the dipole
        normEt = pattEt / np.max(np.abs(pattEt))
        
        # Animate a vector on a sphere of constant radius
        x, y, z = cs.sph2cart(rPattern, gtheta, gphi)
        vec_t_x = normEt * (thetaScale * cs.cartPtSphThetax(x, y, z) \
                            + phiScale * cs.cartPtSphPhix(x, y, z))
        vec_t_y = normEt * (thetaScale * cs.cartPtSphThetay(x, y, z) \
                            + phiScale * cs.cartPtSphPhiy(x, y, z))
        vec_t_z = normEt * (thetaScale * cs.cartPtSphThetaz(x, y, z) \
                            + phiScale * cs.cartPtSphPhiz(x, y, z))
        
        # Note that these fields are purely arbitrary: we're just using
        # the E-theta value of a dipole for convenience, putting its value
        # in both the vectors' phi and theta components.
        
        s = mlab.quiver3d(x, y, z, real(vec_t_x), real(vec_t_y),    \
            real(vec_t_z), color=(0,1,0), scale_mode = "vector",    \
            scale_factor = 0.2)
        # Animate the data.
#        fig = mlab.gcf()
#        ms = s.mlab_source
        
        @mlab.animate(delay=50)
        def anim():
            f = mlab.gcf()
            angle = 0.0
            while True:
                s.mlab_source.set(u = real(vec_t_x * exp(1j*angle)), \
                                  v = real(vec_t_y * exp(1j*angle)), \
                                  w = real(vec_t_z * exp(1j*angle)))
                angle += pi/50
                if (angle >= 2*pi):
                    angle = 0
                yield
        anim()
        mlab.show()
    
    elif (case == 2):
        print("Animation of dipole's far-field E-field theta component")
        # Animate dipole E_theta vector on a sphere of constant radius
        
        theta = np.linspace(0, pi, 15)
        phi = np.linspace(0, 2*pi, 1 + 2**5)
        
        gtheta, gphi = np.meshgrid(theta, phi)
        rPattern = ones_like(gtheta)
        pattEt = HertzianDipoleFF_Etheta(200, gtheta, k, eta0, I, l)
            # 200 is just an arbitrary radial distance away from the dipole
        normEt = np.abs(pattEt / np.max(np.abs(pattEt)))
        
        x, y, z = cs.sph2cart(rPattern, gtheta, gphi)
        vec_t_x, vec_t_y, vec_t_z = cs.cartPtSphTheta(x, y, z) * normEt
        s = mlab.quiver3d(x, y, z, vec_t_x, vec_t_y, vec_t_z, color=(0,1,0), \
                            scale_mode = "vector", scale_factor = 0.2)
        # Animate the data.
#        fig = mlab.gcf()
#        ms = s.mlab_source
        
        @mlab.animate(delay=50)
        def anim():
            f = mlab.gcf()
            angle = 0.0
            while True:
                s.mlab_source.set(u = vec_t_x*cos(angle), \
                                  v = vec_t_y*cos(angle), \
                                  w = vec_t_z*cos(angle))
                angle += pi/50
                if (angle >= 2*pi):
                    angle = 0
                yield
        anim()
        mlab.show()
    
    elif (case == 3):
        print("Dipole's far-field E-field theta component")
        print("")
        print("Vector length corresponds to field magnitude")
        # Plot E_theta vector on a sphere of constant radius
        theta = np.linspace(0, pi, 15)
        phi = np.linspace(0, 2*pi, 1 + 2**5)
        
        gtheta, gphi = np.meshgrid(theta, phi)
        rPattern = ones_like(gtheta)
        pattEt = HertzianDipoleFF_Etheta(200, gtheta, k, eta0, I, l)
            # 200 is just an arbitrary radial distance away from the dipole
        normEt = np.abs(pattEt / np.max(np.abs(pattEt)))
        
        x, y, z = cs.sph2cart(rPattern, gtheta, gphi)
        vec_t_x, vec_t_y, vec_t_z = cs.cartPtSphTheta(x, y, z) * normEt
        mlab.quiver3d(x, y, z, vec_t_x, vec_t_y, vec_t_z, color=(0,1,0))
        mlab.show()
        
    elif (case == 4):
        print("Dipole's far-field E-field theta component")
        print("")
        print("Radial distance and color correspond to field magnitude.")
        
        # Plot pattern as a surface with radial position corresponding to
        # field magnitude
        theta = np.linspace(0, pi, 15)
        phi = np.linspace(0, 2*pi, 1 + 2**5)
        
        gtheta, gphi = np.meshgrid(theta, phi)
        rPattern = ones_like(gtheta)
        pattEt = HertzianDipoleFF_Etheta(200, gtheta, k, eta0, I, l)
            # 200 is just an arbitrary radial distance away from the dipole
        normEt = np.abs(pattEt / np.max(np.abs(pattEt)))
                
        x, y, z = cs.sph2cart(normEt, gtheta, gphi)
        mlab.mesh(x, y, z, scalars = normEt, representation="surface")
        mlab.show()
        
    else:        
        print("Help goes here.")
    
    return

def PlotCutPlane2d(data, cutPlane, plotdB = False, elPlanePhi = "0 deg",
                   angleMax = "auto", dBminr = -80, plotStr = 'b.-'):
    import matplotlib.pyplot as plt
    from numpy import pi
    
    cutPlane = str.lower(cutPlane)
    if ((cutPlane != "az") and (cutPlane != "el")):
        print("Undefined cutplane type. Must be either 'az' or 'el'.")
        return
    
    if (angleMax == "auto"):
        if (cutPlane == "az"):
            angleMax = 2*pi
        else: # (cutPlane == "el"):
            angleMax = pi

    angle = np.linspace(0, angleMax, len(data))

    sp = plt.subplot(111, projection='polar')
    
    if (plotdB):
        if (np.min(data) < 0):
            print("WARNING: negative data value(s) given. Replacing with +1e-20")
        data = np.where(data <= 0, 1e-20, data)
        data = 20*np.log10(data)
        a = plt.gca()
        ymin = np.max((dBminr, np.min(data)))
        ymax = np.max(data)
        a.set_ylim(ymin, ymax)
        a.set_yticks(np.linspace(ymin, ymax, 5))
    
    plt.polar(angle, data, plotStr)
    
    if (cutPlane == "az"):
        plt.title("Azimuth Cutplane (theta = 90 deg)")
    else: #(cutPlane == "el"):
        plt.title("Elevation Cutplane (phi = {})".format(elPlanePhi))
        # Now set angle to start at top and increase clockwise
        sp.set_theta_zero_location("N")
        sp.set_theta_direction(-1) # Clockwise
    
    plt.show()
    
    return


def PlotCutPlane3d():
    import CoorSysUtils as cs
    import mayavi.mlab as mlab
    
    return

# TODO: Draw polarization ellipse at each point?


## Plot theta-hat vector with radial position corresponding to pattern strength
#x, y, z = sph2cart(normAbsEt, gtheta, gphi)
#vec_t_x, vec_t_y, vec_t_z = cartPtSphTheta(x, y, z)
#mlab.quiver3d(x, y, z, vec_t_x, vec_t_y, vec_t_z, color=(0,1,0)) # t in green
#mlab.show()


#mlab.view(azimuth = 0, elevation = 0)
#fig = mlab.figure(1, size=(400, 400), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0)) # figure with white background
