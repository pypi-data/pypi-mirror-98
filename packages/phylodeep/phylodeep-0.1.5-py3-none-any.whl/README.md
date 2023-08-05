# Phylodeep

Phylodeep is a python library for parameter estimation and model selection from phylogenetic trees, based on deep learning.

## Installation

Use the package [pip](https://pip.pypa.io/en/stable/) to install phylodeep.

## Usage 
We recommend to perform a priori model adequacy first, to assess whether the input data resembles well the 
simulations on which the neural networks were trained.


###Python

```python
import phylodeep
from phylodeep import BD, BDEI, BDSS, SUMSTATS, FULL

path_to_tree = './tests/Zurich.trees'

# set presumed sampling probability
sampling_proba = 0.20

# a priori check
model_BD_vs_BDEI = phylodeep.checkdeep(path_to_tree, model=BDSS)


# model selection
model_BDEI_vs_BD_vs_BDSS = phylodeep.modeldeep(path_to_tree, sampling_proba, vector_representation=FULL)

# the selected model is BDSS

# parameter inference
param_BDSS = phylodeep.paramdeep(path_to_tree, sampling_proba, model=BDSS, vector_representation=FULL, 
                                 ci_computation=True)

```

###Command line
```python

# we use here a tree of 200 tips

# a priori model adequacy check: highly recommended
checkdeep -t ./tests/Zurich.trees -m BD -o BD_model_adequacy.png
checkdeep -t ./tests/Zurich.trees -m BDEI -o BDEI_model_adequacy.png
checkdeep -t ./tests/Zurich.trees -m BDSS -o BDSS_model_adequacy.png

# model selection
modeldeep -t ./tests/Zurich.trees -p 0.25 -v CNN_FULL_TREE -o model_selection.csv

# parameter inference
paramdeep -t ./tests/Zurich.trees -p 0.25 -m BDSS -v CNN_FULL_TREE -o HIV_Zurich_BDSS_CNN.csv
paramdeep -t ./tests/Zurich.trees -p 0.25 -m BDSS -v FFNN_SUMSTATS -o HIV_Zurich_BDSS_FFNN_CI.csv -c
```

## Citation


## Contributing


## License