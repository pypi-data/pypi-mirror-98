# uncertainty-framework
Framework for propagating uncertainties through V-FOR-WaTer

## Install

```
pip install uncertainty-framework
```

## Examples

The examples are implemeted as a python module. The main function imports `fire` to 
have a nice command line interface. Currently there is only one example.

### Variogram estimation

This example illustrates, how the MonteCarlo simulation can be used to simulate 
measurement uncertainties on a variogram estimation. It replaces the observations by 
a gaussian distribution around the observation using a scale of `5`. The observation 
value range is `[0, 256[`. 
The `uncertainty_framework.examples.variograms` example has additional dependencies that 
need to be installed separatly:

```
pip install scikit-gstat plotly
```

Then, you can run it through the command line. It is recommended to decrease the default
number of iterations for this example.

```
python -m uncertainty_framework.examples.variograms --num-iter=500 --verbose
```

It is possbile to increase the used scale for generating new observations and also some 
of the variogram parameters are exposed:

```
python -m uncertainty_framework.examples.variograms --num-iter=500 --estimator=cressie --ons-scale=15 --verbose
```
