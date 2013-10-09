function [beamwidth, topIndex, botIndex] = findBeamwidth(beamwidthDepth_dB, data_dB)
%findBeamwidth Determine beamwidth of an antenna pattern
%   beamwidth = Width of beam, in number of indicies between the two bounds
%
%   topIndex = Index into data_dB of location of right-hand (larger angle)
%       bound of the beam
%
%   botIndex = Index into data_dB of location of left-hand (smaller angle)
%       bound of the beam

%   beamwidthDepth_dB = Decrease between pattern max and bounds of
%       beam, e.g. set this to +3 for the half-power (-3dB) beamwidth if
%       data_dB is a power pattern.
%
%   data_dB = Antenna pattern data in dB. Note that whether this is a power
%       or field pattern will influence what value you want to use with
%       beamwidthDepth_dB. Data points are assumed to be given in strictly 
%       increasing or strictly decreasing order by angle.
%   
%
%   Written by Brian Gibbons
%
%   TODO:
%   -Add support for calculating beamwidths of multiple (e.g. over freq.)
%       patterns simultaneously?
%   -Add support for two or more maxima in the pattern?
%
%   Version 0.2 - October 9, 2013
%       -Reworks code to be more generic from the specific case it was
%           orignally written for


% [data_dB_max, data_dB_maxIndex] = max(data_dB, [], 2); % Take max along 2nd (angles) dimension
[data_dB_max, data_dB_maxIndex] = max(data_dB); % Find pattern maximum
data_dB_cutoff = data_dB_max - beamwidthDepth_dB; % subtract off 3dB
angleCount = length(data_dB);

if (data_dB_cutoff < min(data_dB)) % Pattern doesn't go this low
    error('Desired depth of beam lower than data.');
end

topIndex = data_dB_maxIndex;
top_found = false;
botIndex = data_dB_maxIndex;
bot_found = false;

while (~top_found)
    % topIndex is continually incremented, and is "unwrapped"
    % wrappedTopIndex is "wrapped" so as to stay in the bounds of the
    % indices to the array data_dB
    topIndex = topIndex + 1;
    wrappedTopIndex = topIndex;
    if (wrappedTopIndex > angleCount)
        wrappedTopIndex = wrappedTopIndex - angleCount;
        % Only need to subtract angleCount off once, since we know there's
        % a value <= data_dB_cutoff somewhere in the data, so we won't make
        % it around more than once
    end
    if (data_dB(wrappedTopIndex) <= data_dB_cutoff)
        top_found = true;
    end
end
while (~bot_found)
    botIndex = botIndex - 1;
    wrappedBotIndex = botIndex;
    if (wrappedBotIndex <= 0)
        wrappedBotIndex = wrappedBotIndex + angleCount;
    end
    if (data_dB(wrappedBotIndex) <= data_dB_cutoff)
        bot_found = true;
    end
end

% Results
beamwidth = topIndex - botIndex;
if (topIndex > angleCount)
    topIndex = topIndex - angleCount;
end
if (botIndex <= 0)
    botIndex = botIndex + angleCount;
end

end