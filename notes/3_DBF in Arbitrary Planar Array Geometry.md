[Paper](https://asa.scitation.org/doi/10.1121/1.5048044)

### Assumptions
1. Source Signal is far-field in nature ($\omega \tau_{d} << \pi$)
2. Sensor Spacing is smaller than wavelength of interest ($kd << \pi$)

### Concepts
1. Expressing the DBF in its Chebyshev Form
2. Using the Jacobi-Anger Expansion to approximate the exponential function  in the beamformer's beampattern
3. Equating 1 & 2 to build a filter $\vec{h}(\theta_{S})$ that describes a DBF in an Arbitrary Planar Array Geometry

### Variables
$N$ : Order of Differential Beamformer
$M$ : Number of sensors/microphones

### Goal
Construct a filter with the following relationship:
$\Psi \vec{h}(\theta_{S}) = \Upsilon^{*}(\theta_{S}) \vec{v}_{2N}$
such that it creates the beampattern:
$B_{n}[\vec{h}(\omega, \theta_{S}), \theta] = \vec{h}^{H}(\omega, \theta_{S}) \vec{d}(\omega, \theta)$
$B_{n}[\vec{h}(\omega, \theta_{S}), \theta] = \sum_{m = 1}^{M} H^{*}_m(\omega) e^{j(\omega r_m / c_0) \cos{(\theta - \psi_{m})}}$

### Derivation
We start from the following form of beampattern:
$B_n(\theta - \theta_{S}) = \sum_{n = 0}^{N} b_{n, N} \cos{n(\theta - \theta_{S})}$

which can be re-expressed into the following (using Euler's identity):
$B_n(\theta - \theta_{S}) = \sum_{n = 0}^{N} b_{n, N} (\frac{e^{-jn(\theta - \theta_{S})} + e^{jn(\theta - \theta_{S})} }{2})$

and result in the following:
$B_n(\theta - \theta_{S}) = \sum_{n = -N}^{N} v_{n, 2N} e^{jn(\theta - \theta_{S})} = (\Upsilon(\theta_{S})\vec{v}_{2N})^{T} \vec{p}_{e}(\theta)$

where 
$\Upsilon(\theta_{S}) = \begin{bmatrix} \ddots & & \\ & e^{-jn\theta_{S}} & \\ & & \ddots \end{bmatrix} \in \mathbb{C}^{2N \times 2N}$ is a diagonal matrix with $n \in \{-N, ..., N\}$ 
$\vec{v}_{2N} = \begin{bmatrix} \vdots \\ v_{n, 2N} \\ \vdots \end{bmatrix} \in \mathbb{R}^{2N}$  with $n \in \{-N, ..., N\}$ 
$\vec{p}_{e}(\theta) = \begin{bmatrix} \vdots \\ e^{jn\theta} \\ \vdots \end{bmatrix} \in \mathbb{C}^{2N}$ with $n \in \{-N, ..., N\}$ 

*Theorem (Jacobi-Anger Expansion)*  The Optimal Approximation of the exponential function is
$e^{jz\cos{(\theta)}} = \sum_{n=-\infty}^{\infty} (j)^{n} J_{n}(z)e^{jn\theta}$
where $J_{n}(x)$ is the *n-th* order Bessel function of the first kind

Therefore, we can expand
$e^{j(\omega r_{m} / c_{0}) \cos{(\theta - \psi_{m})}} \approx \sum_{n = -N}^{N} j^{n} J_{n}(\frac{\omega r_{m}}{c_{0}}) e^{jn(\theta - \psi_{m})}$
and re-express the Beamformer term $B_{n}[\vec{h}(\omega, \theta_{S}), \theta]$ as
$B_{n}[\vec{h}(\omega, \theta_{S}), \theta] = \sum_{m = 1}^{M} H^{*}_m(\omega) e^{j(\omega r_m / c_0) \cos{(\theta - \psi_{m})}}$

$\approx \sum_{m = 1}^{M} H^{*}_m(\omega) \sum_{n = -N}^{N} j^{n} J_{n}(\frac{\omega r_{m}}{c_{0}}) e^{jn(\theta - \psi_{m})}$

$= \sum_{n = -N}^{N} j^{n}e^{jn\theta} \sum_{m = 1}^{M} H^{*}_m(\omega)  J_{n}(\frac{\omega r_{m}}{c_{0}}) e^{-jn \psi_{m}}$

$= \sum_{-N}^{N} j^{n}e^{jn\theta} \vec{\psi}^{T}_{n}(\omega)\vec{h}^{*}(\omega)$

$= (\Psi(\omega) \vec{h}(\omega))^{H} \vec{p}_{e}(\theta)$

where
$\vec{\psi}_{n}(\omega) = \begin{bmatrix} \vdots \\ J_{n}(\frac{\omega r_{m}}{c_{0}}) e^{-jn \psi_{m}}\\ \vdots \end{bmatrix} \in \mathbb{C}^{M}$
$\Psi(\omega) = \begin{bmatrix} \vdots \\ (-j)^{n}\vec{\psi}^{H}_{n} (\omega) \\ \vdots \end{bmatrix} \in \mathbb{C}^{2N \times M}$ with $n \in \{-N, ..., N\}$ 

Comparing the two equations with respect to $\vec{p}_{e}(\theta)$ , we yield the following relationship:
$\Psi(\omega) \vec{h}(\omega) = \Upsilon^{*}(\theta_{S}) \vec{v}_{2N}$

From this we can derive $\vec{h}(\omega, \theta_{S}) = \Psi^{-1}(\omega) \Upsilon(\theta_{S}) \vec{v}_{2N}$ provided $M = 2N + 1$ where the $\omega$
dependence comes from $\Psi(\omega)$ and the steering angle $\theta_{S}$ dependence comes from $\Upsilon(\theta_{S})$
