using FFTW

function my_stft(x, win::Vector, noverlap::Int, fftsize::Int)
    # x: input signal
    # win: window function
    # noverlap: number of overlapping signals 
    # fftsize: FFT size (in samples)
    
    hop = length(win) - noverlap; # hop size (in samples)
    # Calculate the number of frames in the STFT
    n_frames = 1 + (length(x) - fftsize) ÷ hop
    # println("n_frames = $n_frames")
    
    # Pre-allocate the STFT matrix
    X = zeros(ComplexF64, fftsize ÷ 2 + 1, n_frames)
    
    # Apply the window function to the input signal
    # x_win = x .* win
    
    # Compute the STFT frame by frame
    for i in 1:n_frames
        # Get the current frame
        start_idx = (i - 1) * hop + 1
        end_idx = start_idx + fftsize - 1
        x_frame = x[start_idx:end_idx] .* win
        # println("x_frame @ $i: $(size(x_frame))")

        if length(x_frame) < fftsize
            # println("Prev x_frame length : $(length(x_frame))")
            x_frame = append!(x_frame, zeros(fftsize - length(x_frame)))
            # println("Modified for FFT: $(length(x_frames))")
        end
        
        # Compute the FFT of the current frame
        X_frame = fft(x_frame)
        # println("X_frame -> $(size(X_frame))")
        
        # Store the first-half of the spectrum of the current frame in the STFT matrix
        X[:, i] = X_frame[1:fftsize ÷ 2 + 1]
    end
    
    return X
end

function my_stft(x, win::Vector, noverlap::Int, fftsize::Int, sample_rate::AbstractFloat)
    hop = length(win) - noverlap;
    X = my_stft(x, win, noverlap, fftsize);
    n_frames = 1 + (length(x) - fftsize) ÷ hop

    # Calculate the time and frequency vectors
    frame_rate = sample_rate / hop
    frame_duration = hop / sample_rate
    time = frame_duration * (0:n_frames-1)
    frequency = LinRange(0, sample_rate/2, fftsize ÷ 2 + 1)
    
    return X, time, frequency
end

# Using Overlap-Add Method
function my_istft(X, win, noverlap)
    # X: STFT matrix
    # win: window function
    # noverlap: Number of Overlapping Samples during stride
    
    hop = length(win) - noverlap; # hop: hop size (in samples)
    
    # Get the number of FFT points and frames from the STFT matrix shape
    fftsize, n_frames = size(X)
    fftsize = (fftsize - 1) * 2; # Since only looking at postive frequencies during STFT
    
    # Pre-allocate the output signal
    n_samples = (n_frames - 1) * hop + fftsize
    x_recon = zeros(n_samples)
    
    # Apply the window function to the FFT frames and compute the iFFT
    for i in 1:n_frames
        # Compute the iFFT of the current frame
        x_frame = real(ifft([X[:, i]; conj(reverse(X[2:end-1, i]))]))
        # println(size(x_frame))
        
        # Apply the window function to the time-domain frame
        start_idx = (i - 1) * hop + 1
        end_idx = start_idx + fftsize - 1
        # println(fftsize)
        # println("$start_idx $end_idx $(end_idx-start_idx)")
        x_recon[start_idx:end_idx] += x_frame .* win
    end
    
    return x_recon
end