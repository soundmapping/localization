#=
az: Azimuth Angle in degrees
el: Elevation Angle in degrees
=#
function spherical_to_cartesian(az::Real, el::Real)
    u = cosd(az) .* sind(el);
    v = sind(az) .* sind(el);
    w = cosd(el) ;

    r = [u, v, w];
    return r;
end