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
Sensor based on this paper:
https://ieeexplore.ieee.org/document/9068235
=#
mic1 = [0.5, 0, 0];
mic2 = [1.0, 0, 0];
mic3 = [1.5, 0, 0];
mic4 = [2.0, 0, 0];
mic5 = [2.5, 0, 0];
mic6 = [1.6550, -0.4775, 0];
mic7 = [1.6550, 0.4775, 0];
mic8 = [1.3090, 0.9511, 0];
mic9 = [0.1545, 0.4755, 0];
mic10 = [0.3090, 0.9511, 0];
mic11 = [0.4635, 1.4270, 0];
mic12 = [0.6180, 1.9020, 0];
mic13 = [0.7725, 2.3780, 0];
mic14 = [0.9635, 1.4270, 0];
mic15 = [0.0590, 1.7200, 0];
mic16 = [-0.500, 1.5390, 0];
mic17 = [-0.4045, 0.2939, 0];
mic18 = [-0.8090, 0.5878, 0];
mic19 = [-1.2140, 0.8817, 0];
mic20 = [-1.6180, 1.1760, 0];
mic21 = [-2.0230, 1.4690, 0];
mic22 = [-1.0590, 1.3570, 0];
mic23 = [-1.6180, 0.5878, 0];
mic24 = [-1.6180, 0, 0]
mic25 = [-0.4045, -0.2939, 0];
mic26 = [-0.8090, -0.5878, 0];
mic27 = [-1.2140, -0.8817, 0];
mic28 = [-1.6180, -1.1760, 0];
mic29 = [-2.0230, -1.4690, 0];
mic30 = [-1.6180, -0.5878, 0];
mic31 = [-1.0590, -1.3570, 0];
mic32 = [-0.5, -1.5390, 0];
mic33 = [0.1545, -0.4755, 0];
mic34 = [0.3090, -0.9511, 0];
mic35 = [0.4635, -1.4270, 0];
mic36 = [0.6180, -1.9020, 0];
mic37 = [0.7725, -2.3780, 0];
mic38 = [0.0590, -1.72, 0];
mic39 = [0.9635, -1.4270, 0];
mic40 = [1.3090, -0.9511, 0];

sensors1 = [
mic1, 
mic2, 
mic3, 
mic4, 
mic5, 
mic9, 
mic10, 
mic11,
mic12,  
mic13, 
mic17, 
mic18, 
mic19, 
mic20, 
mic21, 
mic25, 
mic26, 
mic27, 
mic28, 
mic29, 
mic33, 
mic34, 
mic35, 
mic36, 
mic37, 
];

sensors2 = [
mic4, 
mic6, 
mic7, 
mic8, 
mic12, 
mic14, 
mic15, 
mic16, 
mic20, 
mic22, 
mic23, 
mic24, 
mic28, 
mic30,
mic31,
mic32, 
mic36, 
mic38, 
mic39, 
mic40, 
];

println("sensors1 Loaded: $(size(sensors1))")
println("sensors2 Loaded: $(size(sensors2))")

#=
If run as main file, it will plot the sensors locations
on the x-y axis plane
=#
if abspath(PROGRAM_FILE) == @__FILE__ 
    using Plots
    # sensors_plot = mapreduce(permutedims, vcat, sensors)
    # for (idx, mic) in enumerate(sensors)
    #     plot!([mic[1]], [mic[2]], st=:scatter, label="mic$idx",
    #             framestyle=:origin,
    #             aspect_ratio=:equal)
    # end
    # xlabel!("x - position (m)")
    # ylabel!("y - position (m)")
    # title!("sensors Positions")
    # savefig("./plots/matrix_creator.png")

    #=
    Sensors 1 Plot
    =#
    s1 = [1, 2, 3, 4, 5, 9, 10, 11, 12, 13,
     17, 18, 19, 20, 21, 25, 26, 27, 28, 29,
      33, 34, 35, 36, 37];

    for (idx, mic) in enumerate(sensors1)
        plot!([mic[1]], [mic[2]], st=:scatter, label="mic$(s1[idx])",
                framestyle=:origin,
                aspect_ratio=:equal)
    end
    xlabel!("x - position (m)")
    ylabel!("y - position (m)")
    title!("sensors1 Positions")
    savefig("./plots/sensors1.png")

    #=
    Sensors 2 Plot
    =#
    # sensors2_plot = mapreduce(permutedims, vcat, sensors2)
    # s2 = [4,6,7,8,12,14,15,16,20,22,23,24,28,30,31,32,36,38,39,40];
    # for (idx, mic) in enumerate(sensors2)
    #     plot!([mic[1]], [mic[2]], st=:scatter, label="mic$(s2[idx])",
    #             framestyle=:origin,
    #             aspect_ratio=:equal)
    # end
    # xlabel!("x - position (m)")
    # ylabel!("y - position (m)")
    # title!("sensors2 Positions")
    # savefig("./plots/sensors2.png")

    # println("sensors_plot shape: $(size(sensors_plot))")
    # plot(sensors_plot[:,1], sensors_plot[:,2], st=:scatter)
end