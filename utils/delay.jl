include("./coordinates.jl")

#=
Generates Time Delay based on Far-field Planar Wave
with respect to the sensor's position
Input:
sensor_pos  : Sensor Position [x, y, z] in meters
az          : Azimuth Angle (in degrees)
el          : Elevation Angle (in degrees)
c0          : Speed of Wave (m/s)

Output:
time_delay  : Time Delay of Signal at the specified sensor
=#
function generate_time_delay(sensor_pos::Vector, az::Real, el::Real, c0::Real)
    r = spherical_to_cartesian(az, el);
    # println(r)
    # println(sensor_pos)
    # println(size(sensor_pos))

    time_delay = -1* (sensor_pos ⋅ r)/ c0;

    return time_delay
end