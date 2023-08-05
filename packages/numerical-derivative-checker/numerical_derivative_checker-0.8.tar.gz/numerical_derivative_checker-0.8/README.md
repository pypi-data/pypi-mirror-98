# Numerical Derivative Checker
This package contains a numericcal derivative checker that can be used to verify first or second order derivatives by 
comparing them to the central finite difference approximation.

The following combinations of input and output types are currently supported

| Derivative order    |        |  Output type |        |
| -------------  |:------:|:----------------:|:------:|
|                |        | _scalar_           | _vector_ |
|                | _scalar_ | first / second     | first  |
| **Input type** | _vector_ | first / second     | first  |
|                | _matrix_ | first            | ---  |

# Sampling types
In ```helper_functions.py```, there are different sampling routines defined to randomize the function inputs. 
The following samplers are currently implemented:
- ScalarSampler
- VectorSampler
- MatrixSampler
- PosDefMatrixSampler

Each sampling routine has various parameters such as minimum/maximum values or dimensionality.

# Examples
 
Scalar input and output: f(x) = x**2
```
from numerical_derivative_checker import check_derivative, ScalarSampler
check_derivative(sampler=ScalarSampler(n_samples=200),
                 fun=lambda x: np.sin(x),
                 grad=lambda x: np.cos(x),
                 hess=lambda x: -np.sin(x))
```

Vector input and scalar output: f(x) = x^T A x
```
from numerical_derivative_checker import check_derivative, VectorSampler
A = np.random.rand(5, 5)
check_derivative(sampler=VectorSampler(n=5),
                 fun=lambda x: x @ A @ x,
                 grad=lambda x: (A + A.T) @ x)
```


Pos. def. matrix input and scalar output: f(X) = log(det(X))
```
from numerical_derivative_checker import check_derivative, PosDefMatrixSampler
check_derivative(sampler=PosDefMatrixSampler(n=3),
                 fun=lambda x: np.linalg.det(x),
                 grad=lambda x: np.linalg.det(x) * np.linalg.inv(x),
                 tol=1e-3)
```

see ```examples.py``` for more examples.