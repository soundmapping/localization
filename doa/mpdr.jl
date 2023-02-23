using LinearAlgebra
include("./cbf.jl")


#=
Returns the MPDR Power Spectra with the associated Azimuth Angles
Input:
Rx          : Covariance Matrix of Signal
sensor      : Sensor Positions corresponding to Rx

Output:
P           : Power of MPDR Beampattern
az_list     : List Containing Azimuth Angles
=#
function mvdr(Rx, sensor)
    println("For Sanity Check, Rank of Covariance Matrix: $(rank(Rx))")
    P_mvdr, az_list = cbf(inv(Rx), sensor);
    return (1 ./ P_mvdr), az_list
end

if abspath(PROGRAM_FILE) == @__FILE__ 

    #= 
    Step 1: Pre-process Signal by selecting 
          Frequency of Interest at each channel
    =#
    include("../sensor.jl") # To retrieve Sensor Positions
    include("../signal_generator/generate_sig.jl")
    include("../utils/preprocess.jl")
    using WAV
    # new_sig, sample_rate = wavread("./test_signal.wav");
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
    P, az_list = cbf(Rx, sensor);
    P_mvdr, az_list = mvdr(Rx, sensor); # Technically MPDR

    #= 
    Step 3: Predict the Direction of Arrival based on Maximum Power
    =#
    P_cbf_db, az_cbf_max = predict_az(P, az_list);
    P_mvdr_db, az_mvdr_max = predict_az(P_mvdr, az_list);
    print("Predicted MVDR azimuth angle: $(az_mvdr_max)°");

    #= 
    Step 4: Plot Beamformer Power Spectras
    =#
    ymin = minimum([P_cbf_db; P_mvdr_db]);
    using Plots
    plot(az_list, P_cbf_db, label="DoA = $(az_cbf_max)°");
    plot!(az_list, P_mvdr_db, label="MVDR DoA = $(az_mvdr_max)°")
    xlabel!("Azimuth Angle (°)");
    ylabel!("Power (dB)");
    plot!([az_gt, az_gt], [ymin, 0],
        label="True Azimuth Angle = $(az_gt)°",
        marker=:x)
    plot!([az_mvdr_max, az_mvdr_max], [ymin, 0],
        label="Predicted Azimuth Angle = $(az_mvdr_max)°",
        marker=:x)
    savefig("../plots/MVDR_Power_Spectra.png")

    #= 
    Step 5: Plot Polar Plots of Beampattern
    =#
    plot(deg2rad.(az_list), P_cbf_db, proj=:polar, 
            label="CBF: $(az_cbf_max)°");
    plot!(deg2rad.(az_list), P_music_db, proj=:polar,
          label="MUSIC: $(az_music_max)°");
    plot!(deg2rad.(az_list), P_mvdr_db, proj=:polar,
          label="MVDR: $(az_mvdr_max)°");
    plot!(deg2rad.([az_gt, az_gt]),
        [ymin, 0],
        label="True Azimuth Angle = $(az_gt)°",
        marker=:x);
    plot!(deg2rad.([az_mvdr_max, az_mvdr_max]),
        [ymin, 0],
        label="Predicted Azimuth Angle = $(az_mvdr_max)°",
        marker=:x)

    ylims!((ymin, maximum(P_cbf_db)));
    savefig("../plots/MVDR_Beamformer.png")
end
