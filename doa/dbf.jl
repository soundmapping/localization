include("./cbf.jl")

#=
Based on this paper:
https://ieeexplore.ieee.org/document/9037110
=#

#=
Creates c vector to build Delta Matrix
p   : Order of Differnetial
=#
function create_c_vector(p)
    idx = 0:p;
    c = zeros(p+1);
    c .= (-1).^(p .- idx) .* binomial.(p, idx)
    return c
end

#=
Create the Finite Difference Operator in Matrix from

Input:
M       : Number of Sensors
p       : Order of Differential
=#
function create_delta_matrix(M, p)
    delta = zeros((M - p, M));
    for (idx, row) in enumerate(eachrow(delta))
        c = create_c_vector(p);
        # println("c has size $(size(c)) at $idx")
        delta[idx, idx:idx+p] = create_c_vector(p);
    end
    return delta
end

using LinearAlgebra
#=
new_S   : Sensor Signal
sensors : Sensor coordinates Matrix (num_sensors * 3-coordinates)
order   : Differential Beamformer Order
=#
function dbf(new_S, sensors, order=3)
    az_list = LinRange(-180,180,361);
    weights = [];
    for (idx, az) in enumerate(az_list)
        weight = vandermonde_weight.(sensors, az, 90);
        push!(weights, weight)
    end

    M = size(sensors,1);
    delta = create_delta_matrix(size(sensors,1), order);
    P = Vector{}(undef, size(az_list,1));
    for (idx, weight) in enumerate(weights)
        # Conjugating weight will give correct answer
        data_delayed = weight .* new_S[:,1]; 
        diff = delta * data_delayed;
        P[idx] = diff' * diff;
    end
    return P, az_list
end

if abspath(PROGRAM_FILE) == @__FILE__ 
    using WAV
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
    new_S = mapreduce(permutedims, vcat, new_S);

    #=
    Step 2: Generate Differential Beamformer
    =#
    order = 2; # Order of DBF
    P_dbf, az_list = dbf(new_S, sensors, order)
    P_dbf_db = pow2db.(abs.(P_dbf));
    P_dbf_db .-= maximum(P_dbf_db);
    P_dbf_max, az_dbf_max = findmax(P_dbf_db);
    println("Min: $(P_dbf_max)")
    println("P_dbf_db $(P_dbf_db)")
    #=
    Step 3: Plot Differential Beamformer Power Spectra
    =#
    using Plots
    plot(az_list, P_dbf_db,
        label="DBF order $order = $(az_list[az_dbf_max])°");
    xlabel!("Azimuth Angle (°)")
    ylabel!("Power (dB)")
    savefig("./plots/dbf_spectra.png")

    #=
    Step 4: Plot Differential Beamformer Polar Plot
    =#
    using DSP.Util
    plot(deg2rad.(az_list), P_dbf_db,
        label="DBF = $(az_list[az_dbf_max])°",
        proj =:polar);
    ylims!(P_dbf_max, 0)
    savefig("./plots/dbf_beamformer.png")
end