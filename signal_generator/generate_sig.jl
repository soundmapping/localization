# include("chirp.jl")
include("../sensor.jl")
using LinearAlgebra
using WAV
using DSP
using FFTW

#=
delay_signal() delays the signal according to time delays in d

Input:
signal      : Signal (num_samples * 1 Matrix)
d           : Delays for each sensor
fs          : Sampling Frequency of Signal (Hz)

Output:
new_sig     : Delayed Signal at respective channel/sensor
                (Matrix of size num_samples * num_sensors)
=#
function delay_signal(signal::Matrix, d::Vector, fs)
    g(y, delay, freq) = y*exp(-1im*2*π*freq*delay);
    Y = fft(signal);
    Y = vec(Y);
    NFFT = length(Y);
    frequencies = fs/NFFT*(0:(NFFT-1));

    new_sig = Matrix{ComplexF64}(undef, size(Y,1), size(d,1))
    for (idx, delay) in enumerate(d)
            # append!(Y.*exp(-1im.*2.*π.*freq.*delay) );
            delayed = g.(Y, delay, frequencies);
            new_sig[:, idx] = ifft(delayed);
    end
    return new_sig
end

#= 
Step 1: Generate delays based on sensor positions
=#
include("../utils/delay.jl") # generate_time_delay()
az_gt = 30; # Ground Truth of Azimuth Angle
d = generate_time_delay.(sensor, 30, 90, 343)
d .-= minimum(d) # Make all delays positive
println("Delays for each sensor: ", d)

#= 
Step 2: Simulate Wave Sample by creating multichannel
        sample with respective delays
=#
signal, sample_rate = wavread("./signal_generator/1kHz_tone_sr32kHz.wav");
start_idx = Int(sample_rate);
println("Signal has size: $(size(signal))")
mod_signal = signal;
mod_signal[start_idx:end, :] .= 0; # Only taking 1s of Signal
@time new_sig = delay_signal(mod_signal, d, sample_rate);

#=
Step 3: Plots for references
=#
using Plots
plot(signal)
plot!(real(new_sig[:,2]))
println("Now Generated Signal has size: $(size(new_sig))")

if abspath(PROGRAM_FILE) == @__FILE__ 
    wavwrite(real(new_sig), "test.wav", Fs=sample_rate)
end