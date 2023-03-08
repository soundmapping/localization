using Polynomials, SpecialPolynomials

#=
Guide to convert Polynomial form to Chebyshev form
Results -> B(θ, b) = ∑ b_{N, n} * cos(nθ)

Input:
weights = [a_{N, 1}, a_{N, 2}, ... a_{N, N}];

Output:
B_poly      : DBF Beamformer in Polynomial Form
B_chebyshev : DBF Beamformer in Chebyshev Form
=#
function dbf_polynomial(weights::Vector)
    weights = append!( [1 - sum(weights)], weights);

    B_poly = Polynomial(weights);
    B_chebyshev = convert(Chebyshev, B_poly);

    println("Note: x here represents cos(θ)")
    println("Polynomial Form of Differential Beamformer: $(B_poly)")
    println("Chebyshev Form of Differential Beamformer: $(B_chebyshev)")

    return B_poly, B_chebyshev
end

#=
Using the form B(θ, a) = ∑ a_{N, n} * cos(θ).^n
=#
# dipole_a = [1.0]; # Only end element = 1
cardioid_a = [1.0 / 2.0];

# Second-order weights
hypercardioid_a = [2.0 ./ 3.0];
supercardioid_a = [2.0 - sqrt(2.0)];

# Third-order Weights in Polynomial Form
hypercardioid_a = [-4.0, 4.0, 8.0];
hypercardioid_a ./= 7.0;

B_poly, B_chebyshev = dbf_polynomial(hypercardioid_a);

#=
Evaluate Differential Beamformer
=#
using Plots
θ = 0:1:360;
θ = deg2rad.(θ);
plot(θ, abs.( B_poly.( cos.(θ) ) ), proj=:polar, label="Polynomial Form")
plot!(θ, abs.( B_chebyshev.( cos.(θ) ) ), proj=:polar, label="Chebyshev Form")

