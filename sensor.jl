c0 = 343; # Speed of Sound (m/s)
f = 20000;   # Frequency of Interest
wavelength = c0 / f;
max_dist = wavelength / 2;

shift = [max_dist/2 max_dist/2 0]
mic1 = [0 0 0] - shift
mic2 = [0 max_dist 0] - shift
mic3 = [max_dist max_dist 0] - shift
mic4 = [max_dist 0 0] - shift
sensor = [mic1; mic2; mic3; mic4]

# sensor = randn(25, 3)

mic1 = [0.02009, -0.0485, 0]
mic2 = [-0.02009, -0.0485, 0]
mic3 = [-0.0485, -0.02009, 0]
mic4 = [-0.0485, 0.02009, 0]
mic5 = [-0.02009, 0.0485, 0]
mic6 = [0.02009, 0.0485, 0]
mic7 = [0.0485, 0.02009, 0]
mic8 = [0.0485, -0.02009, 0]

sensor = [mic1, mic2, mic3, mic4, mic5, mic6, mic7, mic8]; 
println("Sensor Loaded: $(size(sensor))")

#=
If run as main file, it will plot the sensor locations
on the x-y axis plane
=#
if abspath(PROGRAM_FILE) == @__FILE__ 
    using Plots
    sensor_plot = mapreduce(permutedims, vcat, sensor)
    for (idx, mic) in enumerate(sensor)
        plot!([mic[1]], [mic[2]], st=:scatter, label="mic$idx",
                framestyle=:origin,
                aspect_ratio=:equal)
    end
    xlabel!("x - position (m)")
    ylabel!("y - position (m)")
    title!("Sensor Positions")
    savefig("./doa_experiment/plots/sensor.png")

    # println("Sensor_plot shape: $(size(sensor_plot))")
    # plot(sensor_plot[:,1], sensor_plot[:,2], st=:scatter)
end