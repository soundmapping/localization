N(x, μ, σ) = (1 ./ sqrt(2 .* π .* σ) ) .* exp( -1 .* (x - μ).^2 ./ (2 .* σ) );
wrap(x) = mod( (x + π), 2*π ) - π;

dt = 1;
θ_0 = 0;
v_0 = 1;
cov = I; # Identity Matrix

A = [1 dt; 0 1]; # State Transition Matrix
C = cov;
B = [1 0]; # Measurement Matrix
var = cov; # Measurement Noise
L = -1:1:1; # Replicates

state = [θ_0 v_0];
predictions = [state];

using WAV
wavwrite(s, "save.wav")