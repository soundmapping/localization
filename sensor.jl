using LinearAlgebra
function check_aliasing(sensor1::Vector, sensor2::Vector, f=1000, c0=343)
    d = norm((sensor1-sensor2), 2);
    λ = c0 / f;

    return (d > λ/2)
end

function aliasing_frequency(sensor1::Vector, sensor2::Vector, c0=343.0)
    d = norm((sensor1-sensor2), 2);

    return (c0 / (2*d))
end

function dbf_condition(sensor1::Vector, sensor2::Vector, factor=0.1, f=1000, c0=343.0)
    d = norm((sensor1-sensor2), 2);
    k = 2 * π * f / c0 ;

    return (k*d < (π*factor) )
end

function dbf_max_freq(sensor1::Vector, sensor2::Vector, factor=0.1, c0=343.0)
    d = norm((sensor1-sensor2), 2);

    return (c0 * factor / (2*d))
end

function dbf_max_spacing(factor=0.1, f=1000, c0=343.0)
    return (c0 * factor / (2*f))
end

c0 = 343; # Speed of Sound (m/s)
f = 20000;   # Frequency of Interest
wavelength = c0 / f;
max_dist = wavelength / 2;

shift = [max_dist/2 max_dist/2 0]
mic1 = [0 0 0] - shift
mic2 = [0 max_dist 0] - shift
mic3 = [max_dist max_dist 0] - shift
mic4 = [max_dist 0 0] - shift
sensors = [mic1; mic2; mic3; mic4]

# sensors = randn(25, 3)

#=
Sensor Positions for Matrix Creator
=#
mic1 = [0.02009, -0.0485, 0]
mic2 = [-0.02009, -0.0485, 0]
mic3 = [-0.0485, -0.02009, 0]
mic4 = [-0.0485, 0.02009, 0]
mic5 = [-0.02009, 0.0485, 0]
mic6 = [0.02009, 0.0485, 0]
mic7 = [0.0485, 0.02009, 0]
mic8 = [0.0485, -0.02009, 0]

# mic9 = [0.04009, -0.0285, 0] # For oddity

# println("Aliasing: $(check_aliasing(mic1, mic2, 800))")
# println("Aliasing Frequency: $(aliasing_frequency(mic1, mic5, 343.0)) Hz")
# println("DBF Condition: $(dbf_condition(mic1, mic2, 1000))")
# println("DBF Maximum Frequency: $(dbf_max_freq(mic1, mic2)) Hz")
# println("Maximum Spacing: $(dbf_max_spacing(0.1, 1000)) m")

sensors = [mic1, mic2, mic3, mic4, mic5, mic6, mic7, mic8]; 
println("sensors Loaded: $(size(sensors))")

#=
If run as main file, it will plot the sensors locations
on the x-y axis plane
=#
if abspath(PROGRAM_FILE) == @__FILE__ 
    using Plots
    sensors_plot = mapreduce(permutedims, vcat, sensors)
    for (idx, mic) in enumerate(sensors)
        plot!([mic[1]], [mic[2]], st=:scatter, label="mic$idx",
                framestyle=:origin,
                aspect_ratio=:equal)
    end
    xlabel!("x - position (m)")
    ylabel!("y - position (m)")
    title!("sensors Positions")
    savefig("./plots/sensors.png")

    # println("sensors_plot shape: $(size(sensors_plot))")
    # plot(sensors_plot[:,1], sensors_plot[:,2], st=:scatter)
end