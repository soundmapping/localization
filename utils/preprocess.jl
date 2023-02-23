using DSP
using DSP.Periodograms

#=
Input:
signal          : Single Channel Signal
freq_interest   : Frequency of Interest (in Hz)
fs              : Sampling Rate of Signal (in Hz)
window          : Size of Window for STFT
noverlap        : Number of Samples Overlapping

Output:
The STFT time series of the selected Frequency of Interest
=#
using DSP
using DSP.Periodograms
function choose_freq(signal, freq_interest, fs=32000, window=2^11, noverlap=2^8)
    S = spectrogram(signal, window, noverlap; fs=fs)
    frequencies = DSP.Periodograms.freq(S);
    (_, freq_idx) = findmin( abs.(frequencies .- freq_interest) )
    S = stft(signal, window, noverlap; fs=32000)

    return S[freq_idx, :]
end

#=
Input:
signal          : Single Channel Signal
freq_interest   : Frequency of Interest (in Hz)
fs              : Sampling Rate of Signal (in Hz)
window          : Size of Window for STFT
noverlap        : Number of Samples Overlapping

Output:
S               : STFT (Complex Matrix: # frequencies * # strided samples)
frequencies     : Vector containing Frequencies (given Sampling Rate fs)
times           : Vector containing timestamp (given fs, window & noverlap)
=#
function generate_STFT(signal, freq_interest, fs=32000, window=2^11, noverlap=2^8)
    S = spectrogram(signal, window, noverlap; fs=fs)
    frequencies = DSP.Periodograms.freq(S);
    times = DSP.Periodograms.time(S)
    # (_, freq_idx) = findmin( abs.(frequencies .- freq_interest) )
    S = stft(signal, window, noverlap; fs=32000)

    # return S[freq_idx, :]
    return S, frequencies, times
end

#=
choose_max_freq() returns samples whose frequency has the highest Power amplitude

Input:
signal          : Single Channel Signal
fs              : Sampling Rate of Signal (in Hz)
window          : Size of Window for STFT
noverlap        : Number of Samples Overlapping

Output:
max_S           : Vector (size: # of samples) containing highest Power amplitude
max_freq_list   : Vector (size: # of samples) containing corresponding frequency
times           : Vector containing timestamp (given fs, window & noverlap)
=#
function choose_max_freq(signal, fs=32000, window=2^11, noverlap=2^8)
    S = spectrogram(signal, window, noverlap; fs=fs);
    frequencies = DSP.Periodograms.freq(S);
    times = DSP.Periodograms.time(S);

    S = stft(signal, window, noverlap; fs=32000);
    max_freq_list = [];
    max_S = [];

    for fft_col in eachcol(S)
        (max_P, freq_idx) = findmax(abs.(fft_col));
        append!(max_freq_list, frequencies[freq_idx]);
        append!(max_S, fft_col[freq_idx]);
    end
    
    # (_, freq_idx) = findmin( abs.(frequencies .- freq_interest) )

    # return S[freq_idx, :]
    return max_S, max_freq_list, times;
end

if abspath(PROGRAM_FILE) == @__FILE__ 
    include("../sensor.jl")
    using WAV
    new_sig, sample_rate = wavread("./doa_experiment/simulation_data/chirp_32k.wav");
    new_S = [];
    new_f = [];
    t = [];
    for signal in eachcol(real(new_sig))
        S, frequencies, times = choose_max_freq(signal, sample_rate);
        println(size(S));
        # println(times)
        # println(frequencies)
        push!(new_S, S);
        push!(new_f, frequencies);
        push!(t, times);
    end
end
# DSP.Periodograms.