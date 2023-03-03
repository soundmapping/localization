using LinearAlgebra
include("./cbf.jl")
#=
Input:
Rx          : Covariance Matrix of Signal (M x M Matrix)
n_signals   : Number of Signals in the Sensor Data

- Note: M represents number of sensors

Output:
Ex.values   : Eigenvalues of Covariance Matrix
Rs          : Signal Subspace (M x M Matrix)
Rn          : Noise Subspace  (M x M Matrix)
=#
function get_eigensubspace(Rx, n_signals=1)
    Ex = eigen(Rx);
    Rs = Ex.vectors[:, end-n_signals+1:end];
    Rs = Rs * Rs';
    Rn = Ex.vectors[:, 1:end-n_signals];
    Rn = Rn * Rn';

    return Ex.values, Rs, Rn
end

#=
Returns the MUSIC Pseudo Power Spectra with the associated Azimuth Angles
Input:
Rx          : Covariance Matrix of Signal
sensors      : Sensor Positions corresponding to Rx
f           : Frequency (in Hz)
c0          : Speed of Medium (in m/S)

Output:
P           : Power of MPDR Beampattern
az_list     : List Containing Azimuth Angles
=#
function music(Rx, sensors, n_signals, f=1000, c0=343);
    eig_vals, Rs, Rn = get_eigensubspace(Rx, n_signals);
    P_music, az_list = cbf(Rn, sensors, f, c0);
    return (1 ./ P_music), az_list
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
    Step 2: Generate Beamformer Pattern
    =#
    using Statistics
    Rx = cov(new_S, dims=2);
    P, az_list = cbf(Rx, sensors);
    P_music, az_list = music(Rx, sensors, 1); # MUSIC

    #= 
    Step 3: Predict the Direction of Arrival based on Maximum Power
    =#
    P_cbf_db, az_cbf_max = predict_az(P, az_list);
    P_music_db, az_music_max = predict_az(P_music, az_list);
    print("Predicted MUSIC azimuth angle: $(az_music_max)°");

    #= 
    Step 4: Plot Beamformer Power Spectras
    =#
    ymin = minimum([P_cbf_db; P_music_db;]);
    using Plots
    plot(az_list, P_cbf_db, label="DoA = $(az_cbf_max)°");
    plot!(az_list, P_music_db, label="MUSIC DoA = $(az_music_max)°")
    xlabel!("Azimuth Angle (°)");
    ylabel!("Power (dB)");
    plot!([az_gt, az_gt], [ymin, 0],
        label="True Azimuth Angle = $(az_gt)°",
        marker=:x)
    plot!([az_music_max, az_music_max], [ymin, 0],
        label="Predicted Azimuth Angle = $(az_music_max)°",
        marker=:x)
    savefig("../plots/MUSIC_Power_Spectra.png")

    #= 
    Step 5: Plot Polar Plots of Beampattern
    =#
    plot(deg2rad.(az_list), P_cbf_db, proj=:polar, 
            label="CBF: $(az_cbf_max)°");
    plot!(deg2rad.(az_list), P_music_db, proj=:polar,
          label="MUSIC: $(az_music_max)°");
    plot!(deg2rad.([az_gt, az_gt]),
        [ymin, 0],
        label="True Azimuth Angle = $(az_gt)°",
        marker=:x);
    plot!(deg2rad.([az_music_max, az_music_max]),
        [ymin, 0],
        label="Predicted Azimuth Angle = $(az_music_max)°",
        marker=:x)

    ylims!((ymin, maximum(P_cbf_db)));
    savefig("../plots/MUSIC_Beamformer.png")
end