#### Variables
$\phi_{m}$ : Angular position of Sensor from x-axis of Cartesian Coordinate
$\theta$    : Angle of Incoming wave from x-axis of Cartesian Coordinate

#### Signal Model

$\mathbf{a(\theta)} =  \begin{bmatrix}  \vdots \\  \exp{j \frac{2\pi}{\lambda} r_m \cos{(\theta - \phi_{m}) }} \\  \vdots \end{bmatrix} =  \begin{bmatrix}  \vdots \\  \exp{j \mathbf{k}^{T}\mathbf{r}_{m}} \\  \vdots \end{bmatrix} \in \mathbb{C}^{M}$

#### Beampattern
- Describes the sensitivity of the beamformer for the planewave arriving on the array from direction $\theta$
$B[\mathbf{h}(\omega, \theta_{S}), \theta] = \mathbf{h}^{H}(\omega, \theta_{S}) \mathbf{d}(\omega, \theta)$
- The **Beam Output Power** can be written as:
$P(\theta_{S}) = | B[\mathbf{h}(\omega, \theta_{S}), \theta] |^{2} = \mathbf{h}^{H}(\omega, \theta_{S}) \mathbf{R_{Y}} \mathbf{h}(\omega, \theta_{S})$

#### Distortionless Constraint
- Describes the filter requirement at the steering angle (main response axis)
$\mathbf{h}^{H}(\omega, \theta_{S}) \mathbf{d}(\omega, \theta_{S}) = 1$

#### Direction of Arrival (DOA) Estimation
For a given $\mathbf{h}(\omega, \theta_{S})$ and measurement $Y$, find the candidate angles $\theta_{S} \in \{\theta_{1}, ..., \theta_{k}\}$ such that
$\arg \max_{\theta_{1}, ..., \theta_{k}} \mathbb{E}_{\mathbf{Y}} \{ |\mathbf{h}_{\theta_{S}}^{H} \mathbf{y_n}|^2 \}$

$\begin{equation} \mathbf{h_n} = \begin{bmatrix} \vdots \\ \exp{-j \frac{2\pi}{\lambda} d_i \cos{\theta_{scan}}} \\ \vdots \end{bmatrix} \end{equation}$



