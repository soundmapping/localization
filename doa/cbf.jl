using LinearAlgebra
using DSP.Util
include("../utils/delay.jl")

#=
Input:
sensor_pos  : Sensor Position [x, y, z] in meters
az          : Azimuth Angle (in degrees)
el          : Elevation Angle (in degrees)
f           : Frequency (in Hz)
c0          : Speed of Medium (in m/S)

Output:
weight      : Delay coefficient
=#
function vandermonde_weight(sensor_pos, az, el, f=1000, c0=343)
    w0 = 2 * π * f;
    τ = generate_time_delay(sensor_pos, az, el, c0)
    weight = exp.(-1im * w0 * τ)
    # println("Weights size: ", size(weights))

    return weight 
end

#=
Input:
Rx          : Covariance Matrix of Signal
sensors     : Sensor Positions corresponding to Rx
f           : Frequency (in Hz)
c0          : Speed of Medium (in m/S)

Output:
p           : Power of Beampattern
az_list     : List Containing Azimuth Angles
=#
function cbf(Rx, sensors, f=1000, c0=343)
    az_list = LinRange(-180,180,361);
    P = Vector{}(undef, size(az_list,1));
    for (idx, az) in enumerate(az_list)
        weights = vandermonde_weight.(sensors, az, 90, f, c0);
        P[idx] = weights' * Rx * weights;
    end
    return abs.(P), az_list;
end

# Return Normalized Power and Azimuth Angle with max Power
function predict_az(P, az_list)
    P_db = map(pow2db, P);
    (P_db_max, max_idx) = findmax(P_db);
    P_db .-= P_db_max;
    az_with_max_P = az_list[max_idx];

    return P_db, az_with_max_P
end

function beamform(Rx, sensors, method::Function, n_signals=1)
    return method(Rx, sensors)
end

if abspath(PROGRAM_FILE) == @__FILE__ 
    include("../sensor.jl") # To retrieve Sensor Positions
    #=
    Step 0: Open recording or generate signal
    =#
    # To Generate Signal:
    include("./signal_generator/generate_sig.jl")
    az_gt = 0;      # Ground Truth Azimuth Angle (in degrees)
    c0 = 343;       # Speed of Medium (in m/s)
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
    freq_interest = 1000; # (Hz)
    new_S = []
    for signal in eachcol(new_sig)
        S_interest = choose_freq(signal, freq_interest, sample_rate);
        push!(new_S, S_interest);
    end
    # test_sig = Matrix{}(undef, size(new_sig, 2)) 
    new_S = mapreduce(permutedims, vcat, new_S);

    #=
    Step 2: Generate Beamformer Pattern based on Different 
    =#
    using Statistics
    Rx = cov(new_S, dims=2);
    P, az_list = cbf(Rx, sensors);

    #= 
    Step 3: Predict the Direction of Arrival based on Maximum Power
    =#
    P_cbf_db, az_cbf_max = predict_az(P, az_list);

    #= 
    Step 4: Plot Beamformer Power Spectras
    =#
    ymin = minimum([P_cbf_db;]);
    using Plots
    plot(az_list, P_cbf_db, label="DoA = $(az_cbf_max)°");
    xlabel!("Azimuth Angle (°)");
    ylabel!("Power (dB)");
    plot!([az_gt, az_gt], [ymin, 0],
        label="True Azimuth Angle = $(az_gt)°",
        marker=:x)
    plot!([az_cbf_max, az_cbf_max], [ymin, 0],
        label="Predicted Azimuth Angle = $(az_cbf_max)°",
        marker=:x)
    savefig("../plots/Power_Spectra.png")

    #= 
    Step 5: Plot Polar Plots of Beampattern
    =#
    plot(deg2rad.(az_list), P_cbf_db, proj=:polar, 
            label="CBF: $(az_cbf_max)°");
    plot!(deg2rad.([az_gt, az_gt]),
        [ymin, 0],
        label="True Azimuth Angle = $(az_gt)°",
        marker=:x);
    plot!(deg2rad.([az_cbf_max, az_cbf_max]),
        [ymin, 0],
        label="Predicted Azimuth Angle = $(az_cbf_max)°",
        marker=:x)

    ylims!((ymin, maximum(P_cbf_db)));
    savefig("../plots/Beamformer.png")
end