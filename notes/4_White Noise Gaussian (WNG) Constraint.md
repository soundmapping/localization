### DBF in Aribitrary Planar Array Geometry
$\Psi(\omega) \vec{h}(\omega) = \Upsilon^{*}(\theta_{S}) \vec{v}_{2N}$

### WNG Constraint (no distortion in the look direction)
$\min_{\vec{h}(\omega)} \vec{h}^{H}(\omega) \vec{h}(\omega) \text{ s.t. } \Psi(\omega) \vec{h}(\omega) = \Upsilon^{*}(\theta_{S}) \vec{v}_{2N}$

The solution is 
$\vec{h}(\omega, \theta_{S}) = \Psi^{H}(\omega) \text{  } (\Psi(\omega)\Psi^{H}(\omega))^{-1} \text{  } \Upsilon(\theta_{S}) \vec{v}_{2N}$

### Modified DBF (DBF)
To guarantee robustness, we can use the relationship defined earlier to construct the following optimization:
$\min_{\vec{h}(\omega, \theta_{S}) } \lVert \Psi(\omega) \vec{h}(\omega) - \Upsilon^{*}(\theta_{S}) \vec{v}_{2N}\lVert^{2} \textit{  subject to    }  \lVert \vec{h}(\omega, \theta_{S}) \lVert^{2} \leq 10^{\frac{\delta}{10}} \text{,  } \vec{d}^{H}(\omega, \theta_{S}) \vec{h}(\omega, \theta_{S}) = 1$

where $\lVert \cdot \lVert$ denotes the Euclidean Norm 