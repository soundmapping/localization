include("../sensor.jl")
include("./cbf.jl")

function create_c_vector(p)
    idx = 0:p;
    c = zeros(p+1);
    c .= (-1).^(p .- idx) .* binomial.(p, idx)
    return c
end

function create_delta_matrix(M, p)
    delta = zeros((M - p, M));
    for (idx, row) in enumerate(eachrow(delta))
        c = create_c_vector(p);
        # println("c has size $(size(c)) at $idx")
        delta[idx, idx:idx+p] = create_c_vector(p);
    end
    return delta
end

#=
new_S   : Sensor Signal
sensor  : Sensor coordinates Matrix (num_sensors * 3-coordinates)
order   : Differential Beamformer Order
=#
function dbf(new_S, sensor, order=3)
    az_list = LinRange(-180,180,361);
    weights = [];
    for (idx, az) in enumerate(az_list)
        weight = vandermonde_weight.(sensor, az, 90);
        push!(weights, weight)
    end

    delta = create_delta_matrix(size(sensor,1), order);
    P = Vector{}(undef, size(az_list,1));
    for (idx, weight) in enumerate(weights)
        data_delayed = weight .* new_S[:,1];
        diff = delta * data_delayed;
        P[idx] = diff' * diff;
    end
    return P, az_list
end

if abspath(PROGRAM_FILE) == @__FILE__ 
    az_gt = 30; # Ground Truth of Azimuth Angle
    using WAV
    include("../signal_generator/generate_sig.jl")
    # new_sig, sample_rate = wavread("./test_signal.wav");
    

    #=
    Step 1: Preprocess the Signal
    =#
    freq_interest = 1000; # (Hz)
    new_S = []
    for signal in eachcol(new_sig)
        S_interest = choose_freq(signal, freq_interest, sample_rate);
        push!(new_S, S_interest);
    end
    new_S = mapreduce(permutedims, vcat, new_S);

    #=
    Step 2: Generate Differential Beamformer
    =#
    order = 3; # Order of DBF
    P_dbf, az_list = dbf(new_S, sensor, order)
    P_dbf_db = pow2db.(abs.(P_dbf));
    P_dbf_db .-= maximum(P_dbf_db);
    P_dbf_min, az_dbf_min = findmin(P_dbf_db);

    #=
    Step 3: Plot Differential Beamformer Power Spectra
    =#
    plot(az_list, P_dbf_db,
        label="DBF order $order = $(az_list[az_dbf_min])°");
    xlabel!("Azimuth Angle (°)")
    ylabel!("Power (dB)")
    savefig("./doa_experiment/plots/dbf_spectra.png")

    #=
    Step 4: Plot Differential Beamformer Polar Plot
    =#
    using DSP.Util
    plot(deg2rad.(az_list), P_dbf_db,
        label="DBF = $(az_list[az_dbf_min])°",
        proj =:polar);
    ylims!(P_dbf_min, 0)
    savefig("./doa_experiment/plots/dbf_beamformer.png")
end