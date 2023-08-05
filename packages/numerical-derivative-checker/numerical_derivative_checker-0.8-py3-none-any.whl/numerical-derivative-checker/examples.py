from helper_functions import *
from numerical_derivative_checker import check_derivative

if __name__ == '__main__':
    # Scalar -> Scalar functions
    check_derivative(sampler=ScalarSampler(n_samples=100),
                     fun=lambda x: np.sin(x),
                     grad=lambda x: np.cos(x),
                     hess=lambda x: -np.sin(x))

    # Scalar -> Vector
    a = np.random.randn(3)
    check_derivative(sampler=ScalarSampler(min_val=0.0, max_val=10.0),
                     fun=lambda x: a * x,
                     grad=lambda x: a)

    # Vector -> Scalar functions
    check_derivative(sampler=VectorSampler(n=5),
                     fun=lambda x: np.inner(x, x),
                     grad=lambda x: 2.0 * x,
                     hess=lambda x: 2.0 * np.eye(5))

    check_derivative(sampler=VectorSampler(n=5),
                     fun=lambda x: np.inner(x, x),
                     grad=lambda x: 2.0 * x,
                     hess=lambda x: 2.0 * np.eye(5))

    C = np.random.rand(5, 5)
    check_derivative(sampler=VectorSampler(n=5),
                     fun=lambda x: x @ C @ x,
                     grad=lambda x: (C + C.T) @ x,
                     tol=1e-3)

    # Vector -> Vector functions
    A = np.random.rand(3, 5)
    check_derivative(sampler=VectorSampler(n=5),
                     fun=lambda x: A @ x,
                     grad=lambda x: A)

    # Matrix -> Scalar functions
    a = np.random.rand(3)
    b = np.random.rand(5)
    check_derivative(sampler=MatrixSampler(n=3, m=5),
                     fun=lambda x: a @ x @ b,
                     grad=lambda x: np.outer(a, b),
                     tol=1e-3)
    check_derivative(sampler=PosDefMatrixSampler(n=3),
                     fun=lambda x: np.log(np.linalg.det(x)),
                     grad=lambda x: np.linalg.inv(x),
                     tol=1e-3)
