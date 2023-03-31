include("./dbf_freeform.jl")
using Convex
using SCS
using DSP: db2pow

#=
d_vec represents the steering vector

Input:
f       : Frequency (in Hz)
θ       : Azimuth Angle (in radians)
polar   : Polar-Form of the Sensor Coordinates [r_sensor, ψ_sensor] (2 x 1 Vector)

Output:
=#
d_vec(f, θ, polar::Vector, c0=1500) = exp(1im * 2 * π * f * polar[1] / c0 * cos(θ - polar[2]))

#=
find_h_opt() uses the MDBF Formulation to find an optimal Differential Beamformer

Input:
ψ_mat   :
γ       : Steering Matrix
d       : Steering Vector
wng_pow : White Noise Gaussian Constraint based on the Formulation

=#
function find_h_opt(ψ_mat, γ, d, v, wng_pow = 10 ^ (-0/10))
    h = ComplexVariable(size(ψ_mat, 2));
    objective = norm(ψ_mat * h - γ' * v, 2);
    constraints = [1 ./ wng_pow >= norm(h,2), d' * h == 1];
    problem = minimize(objective, constraints);

    solve!(problem, SCS.Optimizer; silent_solver = true);
    h_opt = evaluate(h);
    return h_opt
end

function check_constraints(h_opt, wng_pow, d)
    con1 = (1 ./ norm(h_opt,2) >= wng_pow);
    con2 = (d' * h_opt == 1.0);
    err_con2 = abs(d' * h_opt - 1);
    println("Constraint 1: $con1")
    println("Constraint 2: $con2 w/ error: $err_con2")
end

function mdbf(Rx::Matrix, sensors::Vector, order=3, f=1000, c0=343, wng_pow=db2pow(4))
    v = ones(Rational, 2*order+1);
    v .//= size(v,1);

    println("weighting vector: $v has sum $(sum(v))")
    ψ_mat = create_ψ_matrix(sensors, order, f, c0);
    println("ψ has rank $(rank(ψ))")

    az_list = LinRange(-180,180,361);
    P = Vector{}(undef, size(az_list,1));
    h_filters = [];
    for (idx, az) in enumerate(az_list)
        γ = steering_matrix(az, order);
        d = d_vec.(freq, deg2rad(az), polar_sensor, c0);
        h_mdbf = find_h_opt(ψ_mat, γ, d, v, wng_pow);
        P[idx] = h_mdbf' * Rx * h_mdbf;
        push!(h_filters, h_mdbf)
    end
    return abs.(P), az_list, ψ, h_filter;
end