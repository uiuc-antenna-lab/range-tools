function plotPoincare(MagX, MagY, DeltaPhase, OpaqueSphere, ShowLabels)
%plotPoincare Plot points on a Poincare sphere
%   Plots a point or vector of points on a Poincare sphere for
%   easy visualization of the points' polarization.
%   
%   X and Y must be two perpendicular measurements of the field, with MagX
%   and MagY being the fields' magnitudes and DeltaPhase being the
%   difference in their phases in degrees (PhaseY - PhaseX).
%
%   OpaqueSphere is an optional argument which determines if the sphere is
%   opaque (points on the back are hidden) or transparent (see-through wire
%   frame) If not specified, it defaults to false (transparent).
%   
%   ShowLabels is an optional argument which sets whether or not to include
%   text labels on the sphere denoting six special case polarizations:
%   left- and right-handed circular; vertical, horizontal, and +/-45
%   degree (slant) linear. If not specified, it defaults to true.
%
%   Written by Brian Gibbons
%
%   Version 0.3 - October 8, 2013
%   	-Tidies up code
%   	-Cleans up labeling code (single phase term now)
%   Version 0.2 - October 1, 2013
%       -Combines X_phase and Y_phase into a single DeltaPhase argument
%       -Adds option to show or hide polarization labels
%       -Places polarization labels' texts slightly above the sphere
%         surface, with their marks still on the surface


% Determine number of input arguments and set defaults accordingly
switch(nargin)
    case 5
        % All arguments specified, no need to do anything
    case 4
        % Default to showing polarization labels
        ShowLabels = true;
    case 3
        % Default to showing polarization labels
        ShowLabels = true;
        % Default to a transparent (wireframe) sphere
        OpaqueSphere = false;
    otherwise
        error('Insufficient number of input arguments.');
end


sxm = size(MagX);
sym = size(MagY);
sph = size(DeltaPhase);

if (sum((sxm ~= sym) | (sxm ~= sph)) ~= 0)
    % Vectors aren't the same size, exit function
    error('Input vector size mismatch');
end

SphereGrid = 30; % Sphere size: SphereGrid+1 units per side
[xs, ys, zs] = sphere(SphereGrid);  % Background unit sphere

gamma = atan(MagY(:) ./ MagX(:));  % compute gamma
delta = (pi/180) * DeltaPhase(:);  % compute delta in radians

% Convert from spherical coordinates (r = 1, phi = 2*gamma, theta = delta)
% to rotated rectangular coordinates (spherical's z-axis becomes the
% x-axis, x becomes y, and y becomes z)
y = sin(2*gamma) .* cos(delta); % normally x
z = sin(2*gamma) .* sin(delta); % normally y
x = cos(2*gamma); % normally z

% cmap = Color map for sphere. Use uniform light gray (nearing white).
cmap = 0.85*ones(SphereGrid+1, SphereGrid+1, 3); 
mesh(xs, ys, zs, cmap);  % Plot background unit sphere using cmap coloring
view([0.7 1 0.5]); % Set viewing angle
if (OpaqueSphere)
    hidden on;
else
    hidden off;
end
hold on;
axis equal; % Could also use 'axis square', since all the axes are the same
rotate3d on; % Allow user to click and drag view
scatter3(x, y, z, 100, 'k.'); % Plot given point(s) with a black point

xlabel('x');
ylabel('y');
zlabel('z');

if (ShowLabels)	% Add special case polarization labels
    % #1: Horiz linear
    labelMagX(1)   = 1; % horiz mag
    labelMagY(1)   = 0; % vert mag
    labelDeltaPhase(1) = 0; % phase (PhaseY - PhaseX)

    % #2: Vert linear
    labelMagX(2)   = 0; % horiz mag
    labelMagY(2)   = 1; % vert mag
    labelDeltaPhase(2) = 0; % phase (PhaseY - PhaseX)

    % #3: +45 deg slant linear
    labelMagX(3)   = 1; % horiz mag
    labelMagY(3)   = 1; % vert mag
    labelDeltaPhase(3) = 0; % phase (PhaseY - PhaseX)

    % #4: -45 deg slant linear
    labelMagX(4)   = 1; % horiz mag
    labelMagY(4)   = 1; % vert mag
    labelDeltaPhase(4) = 180; % phase (PhaseY - PhaseX)

    % #5: LHCP
    labelMagX(5)   = 1; % horiz mag
    labelMagY(5)   = 1; % vert mag
    labelDeltaPhase(5) = 90; % phase (PhaseY - PhaseX)

    % #6: RHCP
    labelMagX(6)   = 1; % horiz mag
    labelMagY(6)   = 1; % vert mag
    labelDeltaPhase(6) = -90; % phase (PhaseY - PhaseX)

    gamma_labels = atan(labelMagY(:) ./ labelMagX(:));
    delta_labels = (pi/180) * labelDeltaPhase(:);

    y_labels = sin(2*gamma_labels) .* cos(delta_labels); % normally x
    z_labels = sin(2*gamma_labels) .* sin(delta_labels); % normally y
    x_labels = cos(2*gamma_labels); % normally z

    % Plot labels' points with a red 'o'
    scatter3(x_labels, y_labels, z_labels, 'ro');
    
	% Factor to scale radial position of text labels.
	% >1 : The labels' origins float about the sphere
	% =1 : The labels' origins are on the surface of the sphere
	% <1 : The labels' origins are in the sphere
    textPosScaling = 1.05;  
    x_labels = textPosScaling*x_labels;
    y_labels = textPosScaling*y_labels;
    z_labels = textPosScaling*z_labels;

    % Add text labels
    text(x_labels(1), y_labels(1), z_labels(1), 'Horiz Linear');
    text(x_labels(2), y_labels(2), z_labels(2), 'Vert Linear');
    text(x_labels(3), y_labels(3), z_labels(3), '+45\circ Slant Linear');
    text(x_labels(4), y_labels(4), z_labels(4), '-45\circ Slant Linear');
    text(x_labels(5), y_labels(5), z_labels(5), 'LHCP');
    text(x_labels(6), y_labels(6), z_labels(6), 'RHCP');
end

hold off;

end
