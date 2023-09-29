# XGBlogS
quick and dirty LogS approximation with xgboost+rdkit.

Aqueous solubility is usually expressed as LogS, the logarithm of aqueous solubility expressed in mol/l. Correctly estimating this value is not that easy, but a regression model on known molecules can give a somewhat decent first guess. The approach here uses XGB regressor with molecule features represented by rdkit 2D descriptors.

Putting this up here for those in a hurry who dont have time to drop this data in a regressor themselves. I did a grid search and provide a decently optimized model as is.


This is based on the data from [Estimation of Aqueous Solubility of Chemical Compounds Using E-State Indices](https://pubs.acs.org/doi/full/10.1021/ci000392t) by Tetko and co-workers 

Their numbers: `r2 0.91, RMSE 0.62`

Numbers of this model: `r2 0.93, RMSE: 0.57` (using the provided splits)

So this regressor's performance is about the same as the published method. A previous version of this model used ECFP fingerprints which has r2 of about 0.86

## requirements
sklearn pandas rdkit>2023.03 (needed for Descriptors.CalcMolDescriptors()) and xgboost

## retrain the model
Obtain the input data using

```wget https://vcclab.org/lab/alogps/logs.txt```

(make sure to check license/downloading conditions)

to retrain just run

```python train.py```

## use the model
import function mols2logS and put an array of mols in there

example:

```python
from XGBlogS import mols2logS
from rdkit import Chem

mols = [Chem.MolFromSmiles(smi) for smi in ["C(CCCC)CC(C)CC","OCCc1ccccc1"]]
print(mols2logS(mols))
```

outputs `[-4.9830585 -1.0931162]`

and that's all. enjoy!
