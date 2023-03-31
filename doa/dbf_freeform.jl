using SpecialFunctions
using LinearAlgebra

#=
Convert Cartesian Coordinates to Polar Coordinates

Input:
xy      : [x, y, z] coordinate

Output:
[r, az] : Radius, Azimuth Angle (in radians)
=#
function cartesian_to_polar(xy::Vector)
    r = xy[1]^2 + xy[2]^2 + xy[3]^2;
    az = atan(xy[2], xy[1]);
    # el = acosd(xy); # Still need some thought process
    return [sqrt(r), az];
end

#=
Convert Sensors' positions from cartesian coordinate to polar

Input:
sensors : Vector (size: # of sensors) containing
             sensor positions (3 - coordinates: [x, y. z])

Output:
polar_sensor    : Vector (size: # of sensors) containing
             sensor positions (2 - coordinates: [r, az (in degrees)])
=#
function sensors_in_polar(sensors::Vector)
    polar_sensor = [];
    for sensor in sensors
        polar = cartesian_to_polar(sensor)
        push!(polar_sensor, polar)
    end
    return polar_sensor
end

#=
Compute the individual ψ entry 

Input:
r       : Radius of sensor position from origin
az      : Azimuth Angle of sensor position from x-axis origin
order   : Order of Bessel Function
=#
function ψ(r::Real, az::Real, order::Int, f=1000, c0=343)
    ω = 2 * π * f;
    # println("Order: $order")
    return besselj(order, ω*r/c0) * exp(-1im * order * az)
end

#=
Generate the ψ matrix for Differential Beamforming

Inputs:
sensors : Vector (size: # of sensors) containing
             sensor positions (3 - coordinates: [x, y. z])
order   : Order of Differential Beamformer
f       : Frequnecy of Interest (in Hz)
c0      : Speed of Medium (in m/s)

Output:
ψ_mat   : ψ Matrix
=#
function create_ψ_matrix(sensors::Vector, order=3, f=1000, c0=343)
    polar_sensor = sensors_in_polar(sensors);
    ψ_mat = Matrix{ComplexF64}(undef, 2*order+1, size(polar_sensor,1));
    for (idx, n) in enumerate(-1*order:1:order)
        ψ_vec_n = [];
        for sensor in polar_sensor # [r, az] - coordinates
            value =  ψ(sensor[1], sensor[2], n, f, c0);
            append!(ψ_vec_n, value)
        end
        # println("ψ_vec_n = $(ψ_vec_n)")
        # println(" and its transpose: $(ψ_vec_n')")
        ψ_mat[idx, :] = ( (-1.0im)^n ) .* ψ_vec_n'; # ' only transposes
    end
    return ψ_mat
end

#=
Generate the Steering Matrix to be paired with ψ for DBF

Inputs:
az_steer_deg    : Azimuth Steering Angle (in degrees)
order           : Order of Differential Beamformer

Output:
γ               : Steering Matrix
=#
function steering_matrix(az_steer_deg, order)
    n = -1*order:1:order;
    az_steer = deg2rad(az_steer_deg);
    γ = Diagonal(exp.(-1im .* n .* az_steer));

    # Alternative
    # az_steer = az_steer_deg ./ 180 .* π;
    # γ = Diagonal(exp.(-1im .* n .*  az_steer_deg ./ 180 .* π));
    return γ
end


#=
dbf_coFree() creates the Differential Beamformer (coordinate-free)
based on the Correlation Matrix Rx and sensors' positions

Input:
Rx          : Covariance Matrix of Signal
sensors     : Sensor Positions corresponding to Rx

Output:
P           : Power of Beampattern
az_list     : List Containing Azimuth Angles (in degrees)
=#
function dbf_coFree(Rx::Matrix, sensors::Vector, order=3, f=1000, c0=343)
    # Creates 1st Order Cardioid, 2nd or 3rd -Order Hypercardioid
    v = ones(Rational, 2*order+1); # Weights associated with DBF
    v .//= size(v,1);

    println("weighting vector: $v has sum $(sum(v))")
    ψ = create_ψ_matrix(sensors, order, f, c0);
    println("ψ has rank $(rank(ψ))")
    sensor_term = ψ' * inv( ψ * ψ' );

    az_list = LinRange(-180,180,361);
    P = Vector{}(undef, size(az_list,1));
    h_filter = Vector{}(undef, size(az_list,1))
    for (idx, az) in enumerate(az_list)
        γ = steering_matrix(az, order);
        h_dbf = sensor_term * conj(γ) * v;
        P[idx] = h_dbf' * Rx * h_dbf;
    end
    return abs.(P), az_list, ψ, h_filter;
end


if abspath(PROGRAM_FILE) == @__FILE__ 
    include("../sensor.jl") # To retrieve Sensor Positions
    #=
    Step 0: Open recording or generate signal
    =#
    # To Generate Signal:
    include("../signal_generator/generate_sig.jl")
    az_gt = 90;      # Ground Truth Azimuth Angle (in degrees)
    c0 = 1500;       # Speed of Medium (in m/s)
    filename = "./signal_generator/1kHz_tone_sr32kHz.wav";
    filename = "./signal_generator/50Hz_tone_sr32kHz.wav";
    new_sig, sample_rate = simulate_sensor_signal(filename, sensors_underwater, az_gt, c0);

    # Open Multichannel Recording:
    # using WAV
    # new_sig, sample_rate = wavread("./test_signal.wav");

    #= 
    Step 1: Pre-process Signal by selecting 
        Frequency of Interest at each channel
    =#
    include("../utils/preprocess.jl")
    freq_interest = 50.0; # (Hz)
    c0 = 1500; # (m/s)
    new_S = []
    
    #=
    Note: For generated signal, use FFT instead. Doing STFT has some issues
    =#
    for signal in eachcol(new_sig)
        S_interest = choose_freq(signal, freq_interest, sample_rate); # Uses STFT
        push!(new_S, S_interest);
    end
    # test_sig = Matrix{}(undef, size(new_sig, 2)) 
    # new_S = mapreduce(permutedims, vcat, new_S);

    #=
    Step 2: Generate Beamformer Pattern based on Different 
    =#
    using Statistics
    include("./cbf.jl")
    order = 3;
    # Rx = cov(new_S, dims=2);
    Rx = new_S[:] * (new_S[:])' ./ 1;
    P_cbf, az_list = cbf(Rx, sensors_underwater, freq_interest, c0);
    P_dbf, az_list, psi, h_filter = dbf_coFree(Rx, sensors_underwater, order, freq_interest, c0);


    #= 
    Step 3: Predict the Direction of Arrival based on Maximum Power
    =#
    P_cbf_db, az_cbf_max = predict_az(P_cbf, az_list);
    P_dbf_db, az_dbf_max = predict_az(P_dbf, az_list);

    # P_cbf_db = P_cbf ./ maximum(P_cbf);
    # P_dbf_db = P_dbf ./ maximum(P_dbf);

    #= 
    Step 4: Plot Beamformer Power Spectras
    =#
    ymin = minimum([P_cbf_db; P_dbf_db;]);
    using Plots
    plot(az_list, P_cbf_db, label="DoA = $(az_cbf_max)°");
    plot!(az_list, P_dbf_db, label="DBF order $(order) = $(az_dbf_max)°");
    xlabel!("Azimuth Angle (°)");
    ylabel!("Power (dB)");
    plot!([az_gt, az_gt], [ymin, 0],
        label="True Azimuth Angle = $(az_gt)°",
        marker=:x)
    plot!([az_dbf_max, az_dbf_max], [ymin, 0],
        label="Predicted Azimuth Angle = $(az_dbf_max)°",
        marker=:x)
    savefig("./plots/DBF_coFree_order$(order)_Power_Spectra.png")

    #= 
    Step 5: Plot Polar Plots of Beampattern
    =#
    plot(deg2rad.(az_list), P_cbf_db, proj=:polar, 
                label="CBF: $(az_cbf_max)°");
    plot!(deg2rad.(az_list), P_dbf_db, proj=:polar, 
            label="DBF order $(order): $(az_dbf_max)°");
    plot!(deg2rad.([az_gt, az_gt]),
        [ymin, 0],
        label="True Azimuth Angle = $(az_gt)°",
        marker=:x);
    plot!(deg2rad.([az_dbf_max, az_dbf_max]),
        [ymin, 0],
        label="Predicted Azimuth Angle = $(az_dbf_max)°",
        marker=:x)

    ylims!((ymin, maximum(P_dbf_db)));
    savefig("./plots/DBF_coFree_order$(order)_Beamformer.png")
end