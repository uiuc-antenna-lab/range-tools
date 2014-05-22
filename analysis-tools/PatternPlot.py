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


def NiceScale(datamin, datamax, stepsize):
    mintick = np.trunc(datamin / float(stepsize)) * stepsize
    if (mintick < datamin):
        mintick += stepsize
    maxtick = np.trunc(datamax / float(stepsize)) * stepsize
    if (maxtick > datamax):
        maxtick -= stepsize

    ticks = np.hstack((datamin,
                       np.arange(mintick, maxtick, stepsize),
                       maxtick, # Since arange excludes the end point
                       datamax))    
    return ticks


def PlotCutPlane(angle, data, cutPlane, normalize = False, plotdB = False,
                 dataIndB = False, dBmin = -60, dBpower = False,
                 plotStr = 'b.-'):
    import matplotlib.pyplot as plt
    
    if ((data.dtype != 'float32') and (data.dtype != 'float64')):
        print("ERROR: data must be of type 'float32' or 'float64'.")
        print("       Actual data type: dtype = {}".format(data.dtype))
        return
    
    cutPlane = str.lower(cutPlane)
    if (len(cutPlane) > 2):
        cutPlane = cutPlane[0:2]
    if ((cutPlane != "az") and (cutPlane != "el")):
        print("Undefined cutplane type. Must be either 'az' or 'el'.")
        return

    d = np.copy(data)
    if (normalize):
        if (dataIndB):
            d -= np.max(d)
        else:
            d /= np.max(np.abs(d))
    
    plt.figure()
    sp = plt.subplot(111, projection='polar')
    
    if (plotdB):
        if (not dataIndB):
            if (dBpower):
                dBbase = 10.0
            else:
                dBbase = 20.0
            d = np.abs(d)
            d = dBbase*np.log10(d)
        d = np.where(d < dBmin, dBmin, d)
        
        a = plt.gca()
#        ymin = np.max((dBmin, np.min(d)))
        ymin = dBmin
        ymax = np.max(d)
        a.set_ylim(ymin, ymax)
        a.set_yticks(NiceScale(ymin, ymax, 10))
    
    if ((not plotdB) and (dataIndB)): # Convert to linear
        if (dBpower):
            dBbase = 10.0
        else:
            dBbase = 20.0
        d = 10**(d / dBbase)
    
    plt.polar(np.deg2rad(angle), d, plotStr)
    
    if (cutPlane == "az"):
        plt.title("Azimuth Cutplane")
    else: #(cutPlane == "el"):
        plt.title("Elevation Cutplane")
        # Now set angle to start at top and increase clockwise
        sp.set_theta_zero_location("N")
        sp.set_theta_direction(-1) # Clockwise
    
    plt.show(block = False)
    
    return


def PlotCutPlane3d():
    import CoorSysUtils as cs
    import mayavi.mlab as mlab
    
    return


def PlotCutPlaneFreqSweep2D(angle, freq, data, normalize = False,
                            plotdB = False, dataIndB = False, dBmin = -60,
                            dBpower = False, plotStr = 'b.-'):
    import matplotlib.pyplot as plt
    
    if ((data.dtype != 'float32') and (data.dtype != 'float64')):
        print("ERROR: data must be of type 'float32' or 'float64'.")
        print("       Actual data type: dtype = {}".format(data.dtype))
        return
    
    d = np.copy(data)
    if (normalize):
        labelVal = "Relative"
        if (dataIndB):
            d -= np.max(d)
        else:
            d /= np.max(np.abs(d))
    else:
        labelVal = "Absolute"
    
    if (plotdB):
        labelType = "Decibels"
        if (not dataIndB):
            if (dBpower):
                dBbase = 10.0
            else:
                dBbase = 20.0
            d = np.abs(d)
            d = dBbase*np.log10(d)
        d = np.where(d < dBmin, dBmin, d)
    else:
        labelType = "Linear"
        if (dataIndB):  # Convert to linear
            if (dBpower):
                dBbase = 10.0
            else:
                dBbase = 20.0
            d = 10**(d / dBbase)
    
    # Good-looking colormaps:
    "gist_rainbow"
    "gist_rainbow_r"
    "jet"
    "jet_r"
    "hot"
    
    angI = np.argsort(angle)
    a = angle[angI]
    d = d[angI, :]
    
    plt.figure()
    plt.pcolormesh(a, freq, d.T, cmap = "gist_rainbow_r")
    plt.axis('tight')
    plt.xlabel('Angle [deg]')
    plt.xticks(NiceScale(np.min(a), np.max(a), 45))
    plt.ylabel('Freq [Hz]')
    cb = plt.colorbar()
    cb.set_label(labelType + " " + labelVal)
    if (plotdB):
        cb.set_ticks(NiceScale(np.min(d), np.max(d), 10))
    else:
        cb.set_ticks(NiceScale(np.min(d), np.max(d), 0.25))
    plt.grid()
    plt.show(block = False)
    
    return


def PlotCutPlaneFreqSweep3D(angle, freq, data, normalize = False,
                            plotdB = False, dataIndB = False, dBmin = -60, 
                            dBpower = False):
#    import mayavi
    import mayavi.mlab as mlab
    
    if ((data.dtype != 'float32') and (data.dtype != 'float64')):
        print("ERROR: data must be of type 'float32' or 'float64'.")
        print("       Actual data type: dtype = {}".format(data.dtype))
        return
    
    d = np.copy(data)
    if (normalize):
        labelVal = "Relative"
        if (dataIndB):
            d -= np.max(d)
        else:
            d /= np.max(np.abs(d))
    else:
        labelVal = "Absolute"
    
    if (plotdB):
        labelType = "Decibels"
        if (not dataIndB):
            if (dBpower):
                dBbase = 10.0
            else:
                dBbase = 20.0
            d = np.abs(d)
            d = dBbase*np.log10(d)
        d = np.where(d < dBmin, dBmin, d)
    else:
        labelType = "Linear"
        if (dataIndB):  # Convert to linear
            if (dBpower):
                dBbase = 10.0
            else:
                dBbase = 20.0
            d = 10**(d / dBbase)
    
    # Code from http://stackoverflow.com/questions/13456845/how-to-change-the-font-type-and-size-in-mayavi-with-code#13464738
    # and from http://stackoverflow.com/questions/19825520/enthought-canopy-mayavi-font-size-bug
    # and from auto-generated code using "record" function of mayavi dialog box

#    from numpy import array
#    mlab.figure()
    try:
        engine = mayavi.engine
    except NameError:
        from mayavi.api import Engine
        engine = Engine()
        engine.start()
    if len(engine.scenes) == 0:
        engine.new_scene()

    mlab.surf(angle, freq, d, 
              extent=[0, len(angle),
                      0, len(freq), 0,
                      np.min((len(angle), len(freq)))])
    
    ax = mlab.axes(ranges = [np.min(angle), np.max(angle), 
                             np.min(freq), np.max(freq), 
                             np.min(d), np.max(d)],
                    nb_labels = 3, xlabel = "Angle [deg]", 
                    ylabel = "Freq [Hz]", zlabel = "Magnitude")
    axes = engine.scenes[0].children[0].children[0].children[0].children[0].children[1]
    
    ax.axes.font_factor = 1.0   # Make font smaller; value in range [1, 2]
    axes.title_text_property.bold = False
    axes.title_text_property.shadow = True
    axes.label_text_property.font_family = 'times'
    axes.label_text_property.bold = False
    axes.label_text_property.shadow = True
    
    module_manager = engine.scenes[0].children[0].children[0].children[0].children[0]
    module_manager.scalar_lut_manager.title_text_property.shadow = True
    module_manager.scalar_lut_manager.label_text_property.shadow = True
    module_manager.scalar_lut_manager.shadow = True
    module_manager.scalar_lut_manager.title_text_property.font_family = 'times'
    
    mlab.scalarbar(orientation = "vertical", nb_labels = 5,
                   title = labelType + " " + labelVal)
    
    mlab.view(azimuth = 225, elevation = 45)
    
    return


def PlotCutPlaneFreqSweep3DPolar(angle, freq, data, normalize = False, 
                                 plotdB = False, dataIndB = False, dBmin = -60, 
                                 linmin = 0, dBpower = False):
    import mayavi.mlab as mlab
#    import mayavi.tools as tools
    
    if ((data.dtype != 'float32') and (data.dtype != 'float64')):
        print("ERROR: data must be of type 'float32' or 'float64'.")
        print("       Actual data type: dtype = {}".format(data.dtype))
        return
    
    d = np.copy(data)
    if (normalize):
        labelVal = "Relative"
        if (dataIndB):
            d -= np.max(d)
        else:
            d /= np.max(np.abs(d))
    else:
        labelVal = "Absolute"
    
    if (plotdB):
        labelType = "Decibels"
        if (not dataIndB):
            if (dBpower):
                dBbase = 10.0
            else:
                dBbase = 20.0
            d = np.abs(d)
            d = dBbase*np.log10(d)
        d = np.where(d < dBmin, dBmin, d)
        dMin = np.max((np.min(d), dBmin))

    else:
        labelType = "Linear"
        if (dataIndB):  # Convert to linear
            if (dBpower):
                dBbase = 10.0
            else:
                dBbase = 20.0
            d = 10**(d / dBbase)
        d = np.where(d < linmin, linmin, d)
        dMin = np.max((np.min(d), linmin))
    
    dMax = np.max(d)
    dRange = np.max(d) - dMin
    radius = (d - dMin) / dRange  # Scale d to range [0, 1]
    
    xd = np.tile(np.cos(np.deg2rad(angle)), (len(freq), 1)).T * radius
    yd = np.tile(np.sin(np.deg2rad(angle)), (len(freq), 1)).T * radius
    zd = np.tile(freq, (len(angle), 1))
    
    xMax = np.max(xd)
    xMin = np.min(xd)
    yMax = np.max(yd)
    yMin = np.min(yd)
    
    # Code from http://stackoverflow.com/questions/13456845/how-to-change-the-font-type-and-size-in-mayavi-with-code#13464738
    # and from http://stackoverflow.com/questions/19825520/enthought-canopy-mayavi-font-size-bug
    # and from auto-generated code using "record" function of mayavi dialog box

#    from numpy import array
#    try:
#        engine = mayavi.engine
#    except NameError:
#        from mayavi.api import Engine
#        engine = Engine()
#        engine.start()
#    if len(engine.scenes) == 0:
#        engine.new_scene()

    mlab.figure()
    mlab.mesh(xd, yd, zd, scalars = d, scale_mode = "scalar",
              extent=[xMin, xMax, yMin, yMax, 0, 10])
    
#    ax = mlab.axes(ranges = [xMin, xMax, yMin, yMax, 
    ax = mlab.axes(ranges = [-dMax, dMax, -dMax, dMax, 
                             np.min(freq), np.max(freq)],
                   extent = [-1, 1, -1, 1, 0, 10],
                   nb_labels = 5, zlabel = "Freq [Hz]",
                   z_axis_visibility = True,
                   x_axis_visibility = True,
                   y_axis_visibility = True)
    
    mlab.scalarbar(orientation = "vertical", nb_labels = 5,
                   title = labelType + " " + labelVal)
    mlab.view(azimuth = 225, elevation = 45)
    
##    tools.pipeline.scalar_cut_plane()
#    
##    mlab.figure()
##    mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(xd, yd, zd, d),
##                                     extent = [-1, 1, -1, 1, 0, 10],
##                                     slice_index = 0,
##                                     plane_orientation = "z_axes")
#    
#    
#    from mayavi.modules.outline import Outline
#    from mayavi.modules.image_plane_widget import ImagePlaneWidget
#
#    mlab.figure()
#    src = mlab.pipeline.scalar_field(xd, yd, zd, d)
#    mlab.pipeline.add_dataset(src)
##    mayavi.add_source(src)
#    mlab.pipeline.ImagePlaneWidgetFactory(src)
##    mayavi.add_module(Outline())
##    mayavi.add_module(ImagePlaneWidget())
    
    
#    axes = engine.scenes[0].children[0].children[0].children[0].children[0].children[1]
#    
#    ax.axes.font_factor = 1.0   # Make font smaller; value in range [1, 2]
#    axes.title_text_property.bold = False
#    axes.title_text_property.shadow = True
#    axes.label_text_property.font_family = 'times'
#    axes.label_text_property.bold = False
#    axes.label_text_property.shadow = True
    
    
    
    return


# TODO: Draw polarization ellipse at each point?


## Plot theta-hat vector with radial position corresponding to pattern strength
#x, y, z = sph2cart(normAbsEt, gtheta, gphi)
#vec_t_x, vec_t_y, vec_t_z = cartPtSphTheta(x, y, z)
#mlab.quiver3d(x, y, z, vec_t_x, vec_t_y, vec_t_z, color=(0,1,0)) # t in green
#mlab.show()


#mlab.view(azimuth = 0, elevation = 0)
#fig = mlab.figure(1, size=(400, 400), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0)) # figure with white background
