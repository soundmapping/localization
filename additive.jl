#=
This script follows the example shown in
https://ieeexplore.ieee.org/document/9068235
=#

include("sensor.jl") # To retrieve Sensor Positions
include("./doa/cbf.jl") # Conventional Beamformer
include("./doa/dbf_freeform.jl") # Differential Beamformer (coordinate-free) 
include("./doa/music.jl") # MUSIC
# include("./doa/mpdr.jl") # MVDR

include("./utils/preprocess.jl")

function normalize_P(P, az_list) 
    (P_max, max_idx) = findmax(P);
    return (P ./ P_max), az_list[max_idx]
end

normalize_P(P) = P ./ maximum(P);

#=
Step 0: Open recording or generate signal
=#

# To Generate Signal:
include("./signal_generator/generate_sig.jl")
include("./signal_generator/tone.jl")
az_gt = -90;        # Ground Truth Azimuth Angle (in degrees)
c0 = 343;          # Speed of Medium (in m/s)
freq = 50;          # Frequency of Tone (in Hz)
amp = 1;            # Amplitude of Tone
duration = 1;       # Duration of Tone (in seconds)
sample_rate = 32000.0;
tone_sig, n = tone(duration, amp, freq, sample_rate);
new_sig1, sample_rate = simulate_sensor_signal(tone_sig, sample_rate, sensors_underwater, az_gt, c0);
new_sig2, sample_rate = simulate_sensor_signal(tone_sig, sample_rate, sensors_underwater, 120, c0);
# new_sig3, sample_rate = simulate_sensor_signal(tone_sig, sample_rate, sensors_underwater, 0, c0);
new_sig = new_sig1 .+ new_sig2 #.+ new_sig3;


#= 
Step 1: Pre-process Signal by selecting 
        Frequency of Interest at each channel
        (FFT instead of STFT)
=#
freq_interest = freq; # (Hz)
new_S = []
NFFT = size(new_sig, 1);
frequencies = sample_rate/NFFT*(0:(NFFT-1));
(_, freq_idx) = findmin( abs.(frequencies .- freq_interest) );

for signal in eachcol(new_sig)
    S_interest = fft(signal);
    S_interest = S_interest[freq_idx];
    push!(new_S, S_interest);
end

new_S1 = []
for signal in eachcol(new_sig1)
    S_interest = fft(signal);
    S_interest = S_interest[freq_idx];
    push!(new_S1, S_interest);
end

new_S2 = []
for signal in eachcol(new_sig2)
    S_interest = fft(signal);
    S_interest = S_interest[freq_idx];
    push!(new_S2, S_interest);
end

#=
Step 2a: Generate Beamformer Pattern based on Different 
=#
Rx = (1 ./ 1) .* new_S * new_S';
println("\nFor Conventional Beamforming: ");
@time P_cbf, az_list = cbf(Rx, sensors_underwater, freq_interest, c0);
println("\nFor DBF (Coordinate-Free) Beamformer: ")
order = 3;
@time P_dbf, az_list = dbf_coFree(Rx, sensors_underwater, order, freq_interest, c0);
# println("\nFor MUSIC Beamformer: ");
@time P_music, az_list = music(Rx, sensors_underwater, 2, freq_interest, c0); # MUSIC
# println("\nFor MVDR/MPDR Beamformer: ");
# @time P_mvdr, az_list = mvdr(Rx, sensors_underwater, freq_interest, c0); # Technically MPDR
println("\n")

Rx1 = (1 ./ 1) .* new_S1 * new_S1';
P1_cbf, az_list = cbf(Rx1, sensors_underwater, freq_interest, c0);
P1_dbf, az_list = dbf_coFree(Rx1, sensors_underwater, order, freq_interest, c0);

Rx2 = (1 ./ 1) .* new_S2 * new_S2';
P2_cbf, az_list = cbf(Rx2, sensors_underwater, freq_interest, c0);
P2_dbf, az_list = dbf_coFree(Rx2, sensors_underwater, order, freq_interest, c0);


#= 
Step 3: Predict the Direction of Arrival based on Maximum Power
=#
using DSP.Util
P_cbf_norm, az_cbf_max = normalize_P(P_cbf, az_list);
P_dbf_norm, az_dbf_max = normalize_P(P_dbf, az_list);

P1_cbf_norm, az1_cbf_max = normalize_P(P1_cbf, az_list);
P2_cbf_norm, az2_cbf_max = normalize_P(P2_cbf, az_list);

P1_dbf_norm, az1_dbf_max = normalize_P(P1_dbf, az_list);
P2_dbf_norm, az2_dbf_max = normalize_P(P2_dbf, az_list);


println("Predicted Azimuth Angle for CBF: $(az_cbf_max)°");
println("Predicted Azimuth Angle for DBF: $(az_dbf_max)°");
println("Predicted Azimuth Angle for DBF2: $(az1_dbf_max)");
println("Predicted Azimuth Angle for DBF2: $(az2_dbf_max)");

#= 
Step 4: Plot Beamformer Power Spectras
=#
using Plots
ymin = minimum([P_cbf_db; P_dbf_db;]);
plot(az_list, P_cbf_norm, label="CBF DoA = $(az_cbf_max)°");
plot!(az_list, P1_cbf_norm,
    label="CBF1 order $order = $(az1_cbf_max)°",
    linestyle=:dash);
plot!(az_list, P2_cbf_norm,
    label="CBF2 order $order = $(az2_cbf_max)°",
    linestyle=:dash);
# plot!(az_list, P1_cbf_norm .+ P2_cbf_norm,
#     label="Add CBF order $order = $(az2_cbf_max)°");
xlabel!("Azimuth Angle (°)");
ylabel!("Power");
savefig("./plots/CBF_Additive_Spectra.png");

plot(az_list, normalize_P(P_dbf),
        label="DBF order $order = $(az_dbf_max)°");
plot!(az_list, normalize_P(P1_dbf),
    label="DBF1 order $order = $(az1_dbf_max)°",
    linestyle=:dash);
plot!(az_list, normalize_P(P2_dbf),
    label="DBF2 order $order = $(az2_dbf_max)°",
    linestyle=:dash);
# plot!(az_list,  normalize_P(P1_dbf) .+ normalize_P(P2_dbf),
#     label="Add DBF order $order = $(az_dbf_max)°");
xlabel!("Azimuth Angle (°)");
ylabel!("Power");

# Plot Ground Truth marker
# plot!([az_gt, az_gt], [ymin, 0],
#     label="True Azimuth Angle = $(az_gt)°",
#     marker=:x)
# plot!([az_cbf_max, az_cbf_max], [ymin, 0],
#     label="Predicted Azimuth Angle = $(az_cbf_max)°",
#     marker=:x)
savefig("./plots/DBF_Additive_Spectra.png");

#= 
Step 5: Plot Polar Plots of Beampattern
=#
# plot(deg2rad.(az_list), P_cbf_db, proj=:polar, 
#         label="CBF: $(az_cbf_max)°");
# plot!(deg2rad.(az_list), P_dbf_db, proj =:polar, 
#         label="DBF order $(order) = $(az_dbf_max)°",);
# plot!(deg2rad.(az_list), P_music_db, proj=:polar,
#         label="MUSIC: $(az_music_max)°");
# # plot!(deg2rad.(az_list), P_mvdr_db, proj=:polar,
# #         label="MVDR: $(az_mvdr_max)°");

# # Plot Ground Truth marker
# plot!(deg2rad.([az_gt, az_gt]),
#     [ymin, 0],
#     label="True = $(az_gt)°",
#     marker=:x);
# plot!(deg2rad.([az_cbf_max, az_cbf_max]),
#     [ymin, 0],
#     label="Predicted (CBF) = $(az_cbf_max)°",
#     marker=:x)

# ylims!((ymin, maximum(P_cbf_db)));
# savefig("./plots/Beamformer.png");
