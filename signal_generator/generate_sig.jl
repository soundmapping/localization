using LinearAlgebra
using WAV
using DSP
using FFTW
using WAV

# include("chirp.jl")
include("../utils/delay.jl") # generate_time_delay()
include("../utils/preprocess.jl")

#=
delay_signal() delays the signal according to time delays in d
thru the frequency domain (might help for non-integerized delays)

Input:
signal      : Signal (num_samples * 1 Matrix)
d           : Delays for each sensor
fs          : Sampling Frequency of Signal (Hz)

Output:
new_sig     : Delayed Signal at respective channel/sensor
                (Matrix of size num_samples * num_sensors)
=#
function delay_signal(signal::Matrix, d::Vector, fs)
    size(sig, 2) == 1 ? 1 : @error throw(
        DimensionMismatch("signal needs to be a num_samples * 1 matrix instead of $(size(sig))")) 

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

using SignalAnalysis: istft
#=
delay_signal() delays the signal according to time delays in d
thru the frequency domain (might help for non-integerized delays)

Input:
signal      : Signal (num_samples * 1 Matrix)
delays      : Delays for each sensor
fs          : Sampling Frequency of Signal (Hz)
NFFT        : (= Window Size) Number of FFT Points to take
noverlap    : Number of samples overlapping during STFT stride
window      : (A Function) Window function before taking individual FFT

Output:
new_sig     : Delayed Signal at respective channel/sensor
                (Matrix of size num_samples * num_sensors)

For window function, refer to https://docs.juliadsp.org/stable/windows/

Guide to window size & noverlap: 
https://www.dsprelated.com/freebooks/sasp/Choice_Hop_Size.html
=#
function delay_signal(sig, delays::Vector, fs::AbstractFloat, 
    NFFT::Int=2^11, noverlap::Int=Int(NFFT * (3//4)), window=hanning)
    size(sig, 2) == 1 ? 1 : @error throw(DimensionMismatch("signal needs to be a num_samples * 1 matrix instead of $(size(sig))")) 

    # STFT of mono channel & prepare multichannel signal
    g(y, delay, freq) = y*exp(-1im*2*π*freq*delay);
    new_sig = zeros( size(sig,1), size(delays,1)); # num_samples * num_ch
    S, frequencies, times = generate_STFT(sig[:,1], sample_rate, NFFT, noverlap);

    # Delay each channel with respective delays in frequency domain,
    # followed by inv-STFT of each channel.
    for (ch, delay) in enumerate(delays)
        new_stft = Matrix{ComplexF64}(undef, size(S,1), size(S,2));
        for (time_idx, ffts) in enumerate(eachcol(S))
            delayed = g.(ffts, delay, frequencies);
            new_stft[:, time_idx] = delayed;
        end
        new_signal = istft(Real, new_stft; nfft=NFFT, noverlap=noverlap, window=window);
        new_sig[1:length(new_signal), ch] = new_signal;
        delay_int = Int(ceil(sample_rate*delay));
        new_sig[1:delay_int, ch] .= 0; # Assume no signal for causality reasons
    end

    return new_sig
end

using DSP.Util: shiftsignal!
#=
delay_signal() delays the signal according to time delays in d
by simply shifting the signal in the time domain

Input:
signal      : Signal (1 * num_samples Matrix)
delays      : Delays for each sensor
fs          : Sampling Frequency of Signal (Hz)

Output:
new_sig     : Delayed Signal at respective channel/sensor
                (Matrix of size num_samples * num_sensors)
=#
function delay_signal_shift(signal::Matrix, delays::Vector, sample_rate)
    size(sig, 2) == 1 ? 1 : @error throw(DimensionMismatch("signal needs to be a num_samples * 1 matrix instead of $(size(sig))")) 

    new_sig = zeros( size(signal,1), size(delays,1));
    for (ch, delay) in enumerate(delays)
        delay_int = Int(ceil(sample_rate * delay))
        new_sig[:, ch] = shiftsignal!(signal[:,1], delay_int);
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
function simulate_sensor_signal_from_file(filename::String, sensors::Vector, 
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
signal      : Matrix of size (# samples * 1 channel)
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

#=
simulate_sensor_signal() simulates the received signal on the sensors
based on its expected time delay and sampling rate of the sensors.

Note: This processing is done in the Complex Domain,
    hence the multichannel signal cannot be saved as a WAV File

Input:
signal      : Matrix of size (# samples * 1 channel)
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
    NFFT::Int, noverlap::Int, window::Function=hanning,
    az_gt = 0.0, c0 = 343.0)

    #= 
    Step 1: Generate delays based on sensor positions
    =#
    println("Start Simulating Signal")
    # az_gt = 0; # Ground Truth of Azimuth Angle
    delays = generate_time_delay.(sensors, az_gt, 90, c0)
    delays .-= minimum(delays) # Make all delays positive
    # println("Delays for each sensor: ", d)

    #= 
    Step 2: Simulate Wave Sample by creating multichannel
    sample with respective delays
    =#
    println("Signal has size: $(size(signal))")
    @time new_sig = delay_signal(signal, delays, sample_rate, NFFT, noverlap, window);
    println("Now Generated Signal has size: $(size(new_sig))")

    return new_sig, sample_rate
end

#=
Helper function
=#
function check_delayed_signal(orig_sig, new_sig, delays, num_period=40)
    d_max = num_period * Int(round(maximum(delays)*sample_rate));
    for (ch, sig) in enumerate(eachcol(new_sig))
        plot(orig_sig[1:d_max], label="Original Signal")
        plot!(sig[1:d_max], label="ch: $ch")
        xlabel!("Samples (n)")
        ylabel!("Amplitude")
        display(plot!([1; 1+round(delays[ch]*sample_rate)],[0;0], label="Delay"))
    end
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