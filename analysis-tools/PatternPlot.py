# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 15:47:32 2014

@author: Brian Gibbons
"""
import numpy as np


def DemoPlot(case = 0, thetaVal = 1.0, phiVal = 1.0j):
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
        print("the values for thetaVal and phiVal. Complex numbers")
        print("may be used for circular or elliptical polarization.")
        print("")
        print("  thetaVal = {}, phiVal = {}".format(thetaVal, phiVal))

        theta = np.linspace(0, pi, 15)
        phi = np.linspace(0, 2*pi, 1 + 2**5)
        
        gtheta, gphi = np.meshgrid(theta, phi)
        rPattern = ones_like(gtheta)
        pattEt = HertzianDipoleFF_Etheta(200, gtheta, k, eta0, I, l)
            # 200 is just an arbitrary radial distance away from the dipole
        normEt = pattEt / np.max(np.abs(pattEt))
        
        # Animate a vector on a sphere of constant radius
        x, y, z = cs.sph2cart(rPattern, gtheta, gphi)
        vec_t_x = normEt * (thetaVal * cs.cartPtSphThetax(x, y, z) \
                            + phiVal * cs.cartPtSphPhix(x, y, z))
        vec_t_y = normEt * (thetaVal * cs.cartPtSphThetay(x, y, z) \
                            + phiVal * cs.cartPtSphPhiy(x, y, z))
        vec_t_z = normEt * (thetaVal * cs.cartPtSphThetaz(x, y, z) \
                            + phiVal * cs.cartPtSphPhiz(x, y, z))
        
        # Note that these fields are purely arbitrary: we're just using
        # the E-theta value of a dipole for convenience, putting its value
        # in both the vectors' phi and theta components.
        
        s = mlab.quiver3d(x, y, z, real(vec_t_x), real(vec_t_y),    \
            real(vec_t_z), color=(0,1,0), scale_mode = "vector",    \
            scale_factor = 0.2)
        mlab.orientation_axes()
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
        mlab.orientation_axes()
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
        mlab.orientation_axes()
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
        mlab.orientation_axes()
        mlab.show()
        
    else:
        print("Help for DemoPlot in the module PatternPlot:")
        print("DemoPlot(case = 0, thetaVal = 1.0, phiVal = 1.0j)")
        print("  Demonstration plots showing some of the capabilities of the")
        print("  Mayavi Python module for antenna radiation pattern display")
        print("  and analysis.")
        print("")
        print("  Four different 3D examples exist:")
        print("  1) Animated Polarization Demo")
        print("  2) Animated Dipole Far-Field E_theta Component")
        print("  3) Stationary Dipole Far-Field E_theta Component")
        print("  4) Surface Plot of Dipole Far-Field E_theta Component")
    
    return


def PlotCutPlane(data, cutPlane, plotdB = False, elPlanePhi = "0 deg",
                   angleMax = "auto", dBminr = -80, plotStr = 'b.-', 
                   dBpower = False):
    import matplotlib.pyplot as plt
    from numpy import pi
    
    cutPlane = str.lower(cutPlane)
    if (len(cutPlane) > 2):
        cutPlane = cutPlane[0:2]
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
            print("WARNING: data values <= 0 given. Replacing with +1e-20")
        data = np.where(data <= 0, 1e-20, data)
        if (not dBpower):
            data = 20*np.log10(data)
        else:
            data = 10*np.log10(data)
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


def PlotCutPlaneFreqSweep2D(angle, freq, data, plotdB = False, dBmin = -60,
                          normalize = False, plotStr = 'b.-', dBpower = False):
    import matplotlib.pyplot as plt
    
    if ((data.dtype != 'float32') and (data.dtype != 'float64')):
        print("ERROR: data must be of type 'float32' or 'float64'.")
        print("       Actual data type: dtype = {}".format(data.dtype))
        return
    
    if (normalize):
        data /= np.max(np.abs(data))
    
    if (plotdB):
        if (dBpower):
            dBbase = 10.0
        else:
            dBbase = 20.0
        data = np.abs(data)
        data = np.where(data < 10**(dBmin / dBbase), 10**(dBmin / dBbase), data)
        data = dBbase*np.log10(data)
    
    # Good-looking colormaps:
    "gist_rainbow"
    "gist_rainbow_r"
    "jet"
    "jet_r"
    "hot"
    
    angI = np.argsort(angle)
    a = angle[angI]
    data = data[angI, :]
    
    plt.pcolormesh(a, freq, data.T, cmap = "gist_rainbow_r")
    plt.axis('tight')
    plt.xlabel('Angle [deg]')
    plt.xticks(np.arange(0, 360 + 45, 45))
    plt.ylabel('Freq [Hz]')
    cb = plt.colorbar()
#    cb.set_label("Normalized |S12|")
    plt.grid()
    plt.show()
    
    return


def PlotCutPlaneFreqSweep3D(angle, freq, data, plotdB = False, dBmin = -60,
                          normalize = False, dBpower = False):
#    import mayavi
    import mayavi.mlab as mlab
    
    if ((data.dtype != 'float32') and (data.dtype != 'float64')):
        print("ERROR: data must be of type 'float32' or 'float64'.")
        print("       Actual data type: dtype = {}".format(data.dtype))
        return
    
    if (normalize):
        data /= np.max(np.abs(data))
    
    if (plotdB):
        if (dBpower):
            dBbase = 10.0
        else:
            dBbase = 20.0
        data = np.abs(data)
        data = np.where(data < 10**(dBmin / dBbase), 10**(dBmin / dBbase), data)
        data = dBbase*np.log10(data)
        
    # Code from http://stackoverflow.com/questions/13456845/how-to-change-the-font-type-and-size-in-mayavi-with-code#13464738
    # and from http://stackoverflow.com/questions/19825520/enthought-canopy-mayavi-font-size-bug
    # and from auto-generated code using "record" function of mayavi dialog box

#    from numpy import array
    try:
        engine = mayavi.engine
    except NameError:
        from mayavi.api import Engine
        engine = Engine()
        engine.start()
    if len(engine.scenes) == 0:
        engine.new_scene()

    mlab.surf(angle, freq, data, 
              extent=[0, len(angle),
                      0, len(freq), 0,
                      np.min((len(angle), len(freq)))])
    
    ax = mlab.axes(ranges = [np.min(angle), np.max(angle), 
                             np.min(freq), np.max(freq), 
                             np.min(data), np.max(data)],
                    nb_labels = 3, xlabel = "Angle [deg]", 
                    ylabel = "Freq [Hz]", zlabel = "Magnitude")
    axes = engine.scenes[0].children[0].children[0].children[0].children[0].children[1]
    
    ax.axes.font_factor = 1.0   # Make font smaller; value in range [1, 2]
    axes.title_text_property.bold = False
    axes.title_text_property.shadow = True
    axes.label_text_property.font_family = 'times'
    axes.label_text_property.bold = False
    axes.label_text_property.shadow = True
    
    mlab.view(azimuth = 225, elevation = 45)
    
    return


# TODO: Draw polarization ellipse at each point?


## Plot theta-hat vector with radial position corresponding to pattern strength
#x, y, z = sph2cart(normAbsEt, gtheta, gphi)
#vec_t_x, vec_t_y, vec_t_z = cartPtSphTheta(x, y, z)
#mlab.quiver3d(x, y, z, vec_t_x, vec_t_y, vec_t_z, color=(0,1,0)) # t in green
#mlab.show()


#mlab.view(azimuth = 0, elevation = 0)
#fig = mlab.figure(1, size=(400, 400), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0)) # figure with white background
