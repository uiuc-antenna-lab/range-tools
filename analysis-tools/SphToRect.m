function [x, y, z] = SphToRect(r, theta, phi)
%SphToRect Convert spherical coordinates (r, theta, phi) into rectangular (x, y, z)
%   r = radius from origin
%
%   theta = angle in radians from +z axis
%
%   phi = angle in radians from +x axis, in the XY plane
%
%   This function was written for easier conversion from spherical to
%   rectangular coordinates, since Matlab's built-in function sph2cart
%   uses an elevation angle instead of a zenith angle. Although this can be
%   handled with a simple conversion, i.e.
%       [x, y, z] = sph2cart(theta, (pi/2) - phi, r);
%   this function can allow for somewhat cleaner code (shorter arguments,
%   and in the order typically used for spherical coordinates).
%
%   Written by Brian Gibbons
%   Version 0.1

x = r .* sin(theta) .* cos(phi);
y = r .* sin(theta) .* sin(phi);
z = r .* cos(theta);

end
