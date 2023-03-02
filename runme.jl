include("sensor.jl") # To retrieve Sensor Positions
include("./doa/cbf.jl") # Conventional Beamformer
include("./doa/music.jl") # MUSIC
include("./doa/mpdr.jl") # MVDR
include("./doa/dbf.jl") # Differential Beamformer

include("./utils/preprocess.jl")

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
freq_interest = 1000; # (Hz)
new_S = []
for signal in eachcol(new_sig)
    S_interest = choose_freq(signal, freq_interest, sample_rate);
    push!(new_S, S_interest);
end
# test_sig = Matrix{}(undef, size(new_sig, 2)) 
new_S = mapreduce(permutedims, vcat, new_S);

#=
Step 2a: Generate Beamformer Pattern based on Different 
=#
using Statistics
Rx = cov(new_S, dims=2);
println("\nFor Conventional Beamforming: ");
@time P, az_list = cbf(Rx, sensors);
println("\nFor MUSIC Beamformer: ");
@time P_music, az_list = music(Rx, sensors, 1); # MUSIC
println("\nFor MVDR/MPDR Beamformer: ");
@time P_mvdr, az_list = mvdr(Rx, sensors); # Technically MPDR
println("\n")

#=
Step 2b: Generate Differential Beamformer
=#
order = 2; # Order of DBF
println("For Differential Beamformer: ");
@time P_dbf, az_list = dbf(new_S, sensors, order)
P_dbf_db = pow2db.(abs.(P_dbf));
P_dbf_db .-= maximum(P_dbf_db);
P_dbf_max, az_dbf_max = findmax(P_dbf_db);
println("\n")

#= 
Step 3: Predict the Direction of Arrival based on Maximum Power
=#
using DSP.Util
P_cbf_db, az_cbf_max = predict_az(P, az_list);
P_music_db, az_music_max = predict_az(P_music, az_list);
P_mvdr_db, az_mvdr_max = predict_az(P_mvdr, az_list);
print("Predicted Azimuth Angle for CBF: $(az_cbf_max)");

#= 
Step 4: Plot Beamformer Power Spectras
=#
using Plots
ymin = minimum([P_cbf_db; P_music_db; P_mvdr_db; P_dbf_db]);
plot(az_list, P_cbf_db, label="DoA = $(az_cbf_max)°");
plot!(az_list, P_music_db, label="MUSIC DoA = $(az_music_max)°")
plot!(az_list, P_mvdr_db, label="MVDR DoA = $(az_mvdr_max)°")
plot!(az_list, P_dbf_db,
        label="DBF order $order = $(az_list[az_dbf_max])°");
xlabel!("Azimuth Angle (°)");
ylabel!("Power (dB)");
plot!([az_gt, az_gt], [ymin, 0],
    label="True Azimuth Angle = $(az_gt)°",
    marker=:x)
plot!([az_cbf_max, az_cbf_max], [ymin, 0],
    label="Predicted Azimuth Angle = $(az_cbf_max)°",
    marker=:x)
savefig("./plots/Power_Spectra.png");

#= 
Step 5: Plot Polar Plots of Beampattern
=#
plot(deg2rad.(az_list), P_cbf_db, proj=:polar, 
        label="CBF: $(az_cbf_max)°");
plot!(deg2rad.(az_list), P_music_db, proj=:polar,
        label="MUSIC: $(az_music_max)°");
plot!(deg2rad.(az_list), P_mvdr_db, proj=:polar,
        label="MVDR: $(az_mvdr_max)°");
plot!(deg2rad.(az_list), P_dbf_db, proj =:polar, 
        label="DBF order $(order) = $(az_list[az_dbf_max])°",);
plot!(deg2rad.([az_gt, az_gt]),
    [ymin, 0],
    label="True = $(az_gt)°",
    marker=:x);
plot!(deg2rad.([az_cbf_max, az_cbf_max]),
    [ymin, 0],
    label="Predicted (CBF) = $(az_cbf_max)°",
    marker=:x)

ylims!((ymin, maximum(P_cbf_db)));
savefig("./plots/Beamformer.png");