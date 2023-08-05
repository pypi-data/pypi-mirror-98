import enum
import numpy as np
from abc import ABC, abstractmethod

FLOAT_MAX = 1e1
DIM_MAX = 10


class VariableType(enum.Enum):
    SCALAR = 1
    VECTOR = 2
    MATRIX = 3


class FunctionType(enum.Enum):
    SCALAR = 1
    VECTOR = 2


def identity_vec(dim: int,
                 i: int) -> np.ndarray:
    v = np.zeros(dim)
    np.put(v, i, 1)
    return v


def identity_mat(dim_i: int,
                 dim_j: int,
                 i: int,
                 j: int) -> np.ndarray:
    v = np.zeros((dim_i, dim_j))
    v[i, j] = 1
    return v


class Sampler(ABC):
    n_samples: int
    @abstractmethod
    def draw(self):
        pass


class ScalarSampler(Sampler):
    """This class generates random samples of scalars."""
    def __init__(self, n_samples=10, min_val=None, max_val=None):
        """
        :param n_samples: number of samples to generate (used in derivative_check)
        :param min_val: minimum value of the samples
        :param max_val: maximum value of the samples
        """
        self.n_samples = n_samples
        if min_val is None:
            self.min_val = -FLOAT_MAX
        else:
            self.min_val = min_val
        if max_val is None:
            self.max_val = FLOAT_MAX
        else:
            self.max_val = max_val

    def draw(self) -> float:
        """Samples a scalar."""
        return self.min_val + np.random.rand() * (self.max_val - self.min_val)


class VectorSampler(Sampler):
    """This class generates random samples of vectors."""
    def __init__(self, n_samples=10, n=None, min_val=None, max_val=None):
        """
        :param n_samples: number of samples to generate (used in derivative_check)
        :param n: dimension of the vector samples
        :param min_val: n dimensional vector that defines the minimum elements of the vector samples
        :param max_val: n dimensional vector that defines the maximum elements of the vector samples
        """
        self.n_samples = n_samples
        if n is None:
            self.n = np.random.randint(DIM_MAX)
        else:
            self.n = n
        if min_val is None:
            self.min_val = -np.ones(self.n) * FLOAT_MAX
        else:
            self.min_val = min_val
        if max_val is None:
            self.max_val = np.ones(self.n) * FLOAT_MAX
        else:
            self.max_val = max_val

    def draw(self) -> np.ndarray:
        """Samples a n dimensional vector."""
        return self.min_val + np.random.rand(self.n) * (self.max_val - self.min_val)


class MatrixSampler(Sampler):
    """This class generates random samples of matrices."""
    def __init__(self, n_samples=10, n=None, m=None, min_val=None, max_val=None):
        """
        :param n_samples: number of samples to generate (used in derivative_check)
        :param n: row dimension of matrix samples
        :param m: column dimension of matrix samples
        :param min_val: (n x m) matrix that define the minimum elements of the matrix samples
        :param max_val: (n x m) matrix that define the maximum elements of the matrix samples
        """
        self.n_samples = n_samples
        if n is None or m is None:
            self.n = np.random.randint(DIM_MAX)
            self.m = np.random.randint(DIM_MAX)
        else:
            self.n = n
            self.m = m
        if min_val is None:
            self.min_val = -np.ones((self.n, self.m)) * FLOAT_MAX
        else:
            self.min_val = min_val
        if max_val is None:
            self.max_val = np.ones((self.n, self.m)) * FLOAT_MAX
        else:
            self.max_val = max_val

    def draw(self) -> np.ndarray:
        """Samples a (n x m) matrix."""
        return self.min_val + np.random.rand(self.n, self.m) * (self.max_val - self.min_val)


class PosDefMatrixSampler(Sampler):
    """This class generates random samples of positive definite matrices."""
    def __init__(self,
                 n_samples: int = 10,
                 n: int = None,
                 min_val: np.ndarray = None,
                 max_val: np.ndarray = None):
        """
        :param n_samples: number of samples to generate (used in derivative_check)
        :param n: row and column dimension of matrix samples
        :param min_val: (n x n) matrix that define the minimum elements of the matrix samples
        :param max_val: (n x n) matrix that define the maximum elements of the matrix samples
        """
        self.n_samples = n_samples
        if n is None:
            self.n = np.random.randint(DIM_MAX)
        else:
            self.n = n
        if min_val is None:
            self.min_val = -np.ones((self.n, self.n)) * FLOAT_MAX
        else:
            self.min_val = min_val
        if max_val is None:
            self.max_val = np.ones((self.n, self.n)) * FLOAT_MAX
        else:
            self.max_val = max_val

    def draw(self) -> np.ndarray:
        """Samples a positive definite matrix."""
        X = self.min_val + np.random.rand() * (self.max_val - self.min_val)
        X = 0.5 * (X + X.T)
        lambda_min = np.fabs(np.min(np.linalg.eig(X)[0]))
        X = X + np.eye(self.n) * (lambda_min + np.random.rand())
        return X
