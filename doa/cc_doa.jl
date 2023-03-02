using LinearAlgebra

"""
    finddelay(x, y)

Estimate the delay of x with respect to y by locating the peak of their
cross-correlation.

The output delay will be positive when x is delayed with respect y, negative if
advanced, 0 otherwise.

# Example
```jldoctest
julia> finddelay([0, 0, 1, 2, 3], [1, 2, 3])
2

julia> finddelay([1, 2, 3], [0, 0, 1, 2, 3])
-2
```
"""
function finddelay(x::AbstractVector, y::AbstractVector)
    s = xcorr(y, x, padmode=:none);
    max_corr = maximum(abs, s);
    max_idxs = findall(x -> abs(x) == max_corr, s);

    center_idx = length(x);
    # Delay is position of peak cross-correlation relative to center.
    # If the maximum cross-correlation is not unique, use the position
    # closest to the center.
    d_ind = argmin(abs.(center_idx .- max_idxs));
    d = center_idx - max_idxs[d_ind];
    return d;
end

using Combinatorics
using DSP
# https://www.mathworks.com/help/phased/ref/gccphat.html
# TDOA Method

# signal = (num of channels * num of samples)
function cc_tdoa(signal, sensor, fs=32000)
    num_channels = size(signal, 2);
    sensor_idx = 1:num_channels ;
    sensor_idx_pairs = combinations(sensor_idx,2);
    m_vectors = [];
    delays = [];
    for sensor_idx_pair in sensor_idx_pairs
        idx1 = sensor_idx_pair[1];
        idx2 = sensor_idx_pair[2];
        
        push!(m_vectors, sensor[idx1] - sensor[idx2]);
        delay = finddelay(signal[:, idx1], signal[:, idx2]);
        push!(delays, delay);
    end

    # Solve TDoA using Least Squares
    m_vectors = mapreduce(permutedims, vcat, m_vectors);
    r = m_vectors \ (-1 .* c0 .* delays ./ fs);
    az = atand(r[2], r[1]);
    el = acosd(r[3]);

    return az, el, delays;
end


include("../sensor.jl") # To retrieve Sensor Positions
#=
Step 0: Open recording or generate signal
=#
# To Generate Signal:
include("../signal_generator/generate_sig.jl")
az_gt = 0.0;      # Ground Truth Azimuth Angle (in degrees)
c0 = 343.0;       # Speed of Medium (in m/s)
filename = "./signal_generator/1kHz_tone_sr32kHz.wav";
new_sig, sample_rate = simulate_sensor_signal(filename, sensors, az_gt, c0);

# Open Multichannel Recording:
# using WAV
# new_sig, sample_rate = wavread("./test_signal.wav");

#= 
Step 1: Pre-process Signal by selecting 
      Frequency of Interest at each channel
=#
include("../utils/preprocess.jl")
@time az, el, delays = cc_tdoa(new_sig, sensors, 32000);
println("Azimuth Angle from Cross-Correlation: $(az)°")
# push!(pair_corr, xcorr(signal_pair[1, :], signal_pair[2,:]));
# plot(abs.(pair_corr[1]))