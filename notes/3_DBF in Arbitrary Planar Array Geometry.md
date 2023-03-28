[Paper](https://asa.scitation.org/doi/10.1121/1.5048044)

### Assumptions
1. Source Signal is far-field in nature ($\omega \tau_{d} << \pi$)
2. Sensor Spacing is smaller than wavelength of interest ($kd << \pi$)

### Concepts
1. Expressing the DBF in its Chebyshev Form
2. Using the Jacobi-Anger Expansion to approximate the exponential function  in the beamformer's beampattern
3. Equating 1 & 2 to build a filter $\mathbf{h}(\theta_{S})$ that describes a DBF in an Arbitrary Planar Array Geometry
### Goal
Construct a filter with the following relationship:
$\Psi \mathbf{h}(\theta_{S}) = \Upsilon^{*}(\theta_{S}) \mathbf{v}_{2N}$
such that it creates the beampattern:
$B_{n}[\mathbf{h}(\omega, \theta_{S}), \theta] = \mathbf{h}^{H}(\omega, \theta_{S}) \mathbf{d}(\omega, \theta)$

### Derivation
We start from the following form of beampattern:
$B_n(\theta - \theta_{S}) = \sum_{n = 0}^{N} b_{n, N} \cos{n(\theta - \theta_{S})}$

which can be re-expressed into the following (using Euler's identity):
$B_n(\theta - \theta_{S}) = \sum_{n = 0}^{N} b_{n, N} (\frac{e^{-jn(\theta - \theta_{S})} + e^{jn(\theta - \theta_{S})} }{2})$

and result in the following:
$B_n(\theta - \theta_{S}) = \sum_{n = -N}^{N} c_{n, N} e^{jn(\theta - \theta_{S})} = \begin{bmatrix} \Upsilon(\theta_{S}) & \mathbf{b}_{2N} \end{bmatrix}^{T} \mathbf{p}_{e}(\theta)$

where 

