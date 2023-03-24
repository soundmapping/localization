function tone(duration=90, amp=1, f=1000, sample_rate=32000)
    # t = 0:duration;/
    n = 0:(duration.*sample_rate - 1);
    P = amp .* sin.(2 .* π .* f ./ sample_rate .* n);
    P = mapreduce(permutedims, vcat, [P']);
    return P, n
end

# using Distri

# using Plots
# P, n = tone(90, 1, 1000);
# plot(n[1:32000], P[1:32000])

# using WAV
# wavwrite(P, "test.wav", Fs=32000)

#=
(Under Construction)
TODO: Gaussian Window
=#
# using DSP # for FFT and frequency axis

# # Define the parameters of the signal
# Fs = 8000 # sampling frequency
# N = 2000 # number of samples
# f0 = 50 # center frequency of Gaussian window
# bw = 10 # bandwidth of Gaussian window

# # Generate the frequency axis
# freq = fftfreq(N, Fs)

# # Generate the Gaussian window
# window = exp.(.-(freq .- f0).^2 ./ (2 .* bw.^2))
# window ./= sum(window)
# gaussian_sig = zeros(1, N)
# for (idx, amp) in enumerate(window)
#     if freq[idx] < 0
#         continue
#     end
#     signal, n = tone(N ./ Fs, amp, freq[idx], Fs)
#     gaussian_sig .+= signal
# end

# wave = [];
# for k = 1:20
#     push!(wave, gaussian_sigs);
# end
# wave = mapreduce(permutedims, vcat, wave)

# using WAV
# wavwrite(gaussian_sig, "test.wav", Fs=Fs)

# # window .+= exp.(.-(f0 .- freq).^2 ./ (2 .* bw.^2))

# # Compute the inverse FFT of the Gaussian window to get the time-domain signal
# # signal = ifft(window)

# # Plot the frequency spectrum and time-domain signal
# using Plots
# plot(freq, abs.(fft(gaussian_sig))', xlabel="Frequency (Hz)", ylabel="Magnitude", label="Spectrum")
# plot(abs.(gaussian_sig)', xlabel="Sample", ylabel="Amplitude", label="Signal")
