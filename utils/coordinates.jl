#=
az: Azimuth Angle
el: Elevation Angle
=#
function spherical_to_cartesian(az::Real, el::Real)
    u = cosd(az) .* sind(el);
    v = sind(az) .* sind(el);
    w = cosd(el) ;

    r = [u, v, w];
    return r;
end