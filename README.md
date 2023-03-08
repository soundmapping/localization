# Direction of Arrival Analysis

To start, after cloning the repo, run the following to install dependencies:
```
julia install.jl
```

To regenerate the [Underwater](https://ieeexplore.ieee.org/document/9068235) paper:
'''
julia underwater.jl
'''

Note: Refer to [./doa/dbf_freeform.jl](./doa/dbf_freeform.jl) on how to generate Differential Beamforming DoAs

Note 2: Its Steering Formulation can be found under [this paper](https://asa.scitation.org/doi/10.1121/1.5048044)

To visualize the sensors' location, run the following:
```
julia sensor.jl
```
Note: Plots will be generated at `./plots` folder

(Under Construction) To visualize all the DoA Algorithms, run the following:
```
julia runme.jl
```
