# FastGWR

Install dependencies:

```
1. Install any MPI implementation
For Mac:
    OpenMPI: https://www.open-mpi.org
    Microsoft MPI: https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi

2. Install `mpi4py` package
```

Example call to FastGWR which can be called on desktop or HPC:

```
mpiexec -np 4 python fastgwr-mpi.py -data input.csv -out results.csv -a -bw 1000
```

```
where:
-np 4: using 4 processors.
-data input.csv: input data matrix.
-out results.csv: output GWR results matrix including local parameter estimates, standard errors and local diagnostics.
-a (or --adaptive): Adaptive Bisquare kernel.
-f (or --fixed): Fixed Gaussian kernel.
-c (or --constant): Adding constant.
-bw 1000: Pre-defined bandwidth parameter. If missing, it will (golden-section) search for the optimal bandwidth and use that to fit GWR model.
-minbw 45: Lower bound in golden-section search.
```

The input needs to be prepared in this order:

| X-coord | Y-coord | y | X1 | X2 | ...| Xk |
|:-------:|:-------:|:-:|:--:|:--:|:--:|:--:|


```
where:
X-coord: X coordinate of the location point
Y-coord: Y coordinate of the location point
y: dependent variable
X1...Xk: independent variables
```


A friendely interface following pysal/mgwr package can be found under this branch:


```
https://github.com/Ziqi-Li/mgwr/tree/FastGWR
```


Example call to FastGWR using pysal/mgwr interface can be found in this [notebook](https://github.com/Ziqi-Li/mgwr/blob/FastGWR/mgwr/notebooks/FastGWR.ipynb)


Reference
 [FastGWR](https://www.tandfonline.com/doi/full/10.1080/13658816.2018.1521523)
```
Li,Z., Fotheringham,A.S., Li,W., Oshan,T. (2018) Fast Geographically Weighted Regression (FastGWR): 
A Scalable Algorithm to Investigate Spatial Process Heterogeneity in Millions of Observations.
International Journal of Geographic Information Science. doi: 10.1080/13658816.2018.1521523
```




