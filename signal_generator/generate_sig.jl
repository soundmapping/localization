using LinearAlgebra
using WAV
using DSP
using FFTW
using WAV

# include("chirp.jl")
include("../utils/delay.jl") # generate_time_delay()

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
Given a WAV File, simulate_sensor_signal() simulates the signal
when received in the sensors thru its expected time delay.

Note: This processing is done in the Complex Domain,
    hence the multichannel signal cannot be saved as a WAV File

Input:
filename    : Filename of WAV File
sensors     : Vector (size: # of sensors) containing
                Sensor Positions (# of coordinates = 3)
az_gt       : Azimuth Angle to simulate (in Degrees)
c0          : Speed of Medium (in m/s)

Output:
new_sig     : Delayed Signals according to sensors' positions
sample_rate : Sampling Rate of Signal (in Hz)
az_gt       : Simulated Azimuth Angle (in Degrees)
=#
function simulate_sensor_signal(filename::String, sensors::Vector, 
                                az_gt = 0.0, c0=343.0)
    #= 
    Step 0: Open Sound File of Interest
    =#
    println("Begin Reading File $filename")
    signal, sample_rate = wavread(filename);
    println("Size: $(size(signal))")
    new_sig, sample_rate = simulate_sensor_signal(signal, sample_rate,
                                         sensors, az_gt, c0);

    return new_sig, sample_rate
end

#=
simulate_sensor_signal() simulates the received signal on the sensors
based on its expected time delay and sampling rate of the sensors.

Note: This processing is done in the Complex Domain,
    hence the multichannel signal cannot be saved as a WAV File

Input:
signal      : Matrix of size (1 channel * # samples)
sample_rate : Sampling Rate of Signal
sensors     : Vector (size: # of sensors) containing
                Sensor Positions (# of coordinates = 3)
az_gt       : Azimuth Angle to simulate (in Degrees)
c0          : Speed of Medium (in m/s)

Output:
new_sig     : Delayed Signals according to sensors' positions
sample_rate : Sampling Rate of Signal (in Hz)
az_gt       : Simulated Azimuth Angle (in Degrees)
=#
function simulate_sensor_signal(signal::Matrix, sample_rate::AbstractFloat, sensors::Vector, 
                                az_gt = 0.0, c0 = 343.0)
    
    #= 
    Step 1: Generate delays based on sensor positions
    =#
    println("Start Simulating Signal")
    # az_gt = 0; # Ground Truth of Azimuth Angle
    d = generate_time_delay.(sensors, az_gt, 90, c0)
    d .-= minimum(d) # Make all delays positive
    # println("Delays for each sensor: ", d)

    #= 
    Step 2: Simulate Wave Sample by creating multichannel
            sample with respective delays
    =#
    start_idx = Int(sample_rate);
    println("Signal has size: $(size(signal))")
    mod_signal = signal;
    mod_signal[start_idx:end, :] .= 0; # Only taking 1 second of Signal
    @time new_sig = delay_signal(mod_signal, d, sample_rate);
    println("Now Generated Signal has size: $(size(new_sig))")

    return new_sig, sample_rate
end

if abspath(PROGRAM_FILE) == @__FILE__ 
    include("../sensor.jl")
    az_gt = 0;
    filename = "./signal_generator/1kHz_tone_sr32kHz.wav";
    new_sig, sample_rate = simulate_sensor_signal(filename, sensors, az_gt);

    #=
    Step 3: Plots for references
    =#
    using Plots
    plot(signal)
    plot!(real(new_sig[:,2]))


    if abspath(PROGRAM_FILE) == @__FILE__ 
        wavwrite(real(new_sig), "test.wav", Fs=sample_rate)
    end

end