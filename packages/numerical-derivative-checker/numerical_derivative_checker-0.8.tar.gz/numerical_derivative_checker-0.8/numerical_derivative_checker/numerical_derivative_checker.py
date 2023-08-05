from numerical_derivative_checker.helper_functions import *
from typing import Callable


def check_derivative(fun: Callable[[np.ndarray], np.ndarray] = None,
                     grad: Callable[[np.ndarray], np.ndarray] = None,
                     hess: Callable[[np.ndarray], np.ndarray] = None,
                     x: np.ndarray = None,
                     sampler: Sampler = None,
                     eps: float = 1e-7,
                     tol: float = 1e-4,
                     verbose: int = 1) -> bool:
    """ This function performs a finite difference check of the gradient and Hessian function.
    The method compares the provided derivatives with the finite difference approximation
    (f(x+eps) - f(x-eps)) / (2 * eps) and returns true if they lie within tolerance tol.
    :param fun: function y=f(x) that should be checked.
    :param grad: gradient/Jacobian function of f(x).
    :param hess: Hessian function of f(x).
    :param x: input point at which the derivative should be checked.
    :param sampler: if sampler is specified, then x is ignored.
    :param eps: spacing parameter
    :param tol: tolerance parameter
    :param verbose: 0: silent, 1: only if check fails, 2: print full output
    """
    if x is None and sampler is None:
        raise ValueError("Either x or sampler needs to be defined.")

    if sampler is not None:
        X = []
        for n in range(sampler.n_samples):
            X += [sampler.draw()]
    else:
        X = [x]

    # determine input type
    if np.isscalar(X[0]):
        var_type = VariableType.SCALAR
        dim_x = (1,)
    elif len(np.shape(X[0])) == 1:
        var_type = VariableType.VECTOR
        dim_x = np.shape(X[0])
    elif len(np.shape(X[0])) == 2:
        var_type = VariableType.MATRIX
        dim_x = np.shape(X[0])
    else:
        raise ValueError('The input variable x has to be a scalar, vector or matrix.')

    # determine output type
    y = fun(X[0])
    if np.isscalar(y):
        fun_type = FunctionType.SCALAR
        dim_y = (1, )
    elif len(np.shape(y)) == 1:
        fun_type = FunctionType.VECTOR
        dim_y = np.shape(y)
    else:
        raise ValueError('The function output has to be a scalar or vector.')

    if grad:
        J = grad(X[0])
        if fun_type is FunctionType.SCALAR and var_type is VariableType.SCALAR:
            assert np.isscalar(J), "Gradient output type needs to be a scalar."

        if fun_type is VariableType.VECTOR:
            assert len(J.shape) == 2, "Gradient has wrong dimension."
            [n, m] = J.shape
            assert m == dim_x and n == dim_y, "The gradient has wrong dimension."

    if var_type is VariableType.MATRIX:
        assert fun_type is FunctionType.SCALAR, "Function output type needs to be scalar for matrix inputs."

    if hess:
        assert fun_type == FunctionType.SCALAR, \
            'The Hessian matrix can only be checked for scalar output functions.'
        assert var_type is not VariableType.MATRIX, \
            'The Hessian matrix can only be checked for scalar or vector input variables.'

    result = True
    for x in X:
        if fun is not None and grad is not None:
            J = grad(x)

            if var_type is VariableType.SCALAR:
                J_eps = (fun(x + eps) - fun(x - eps)) / (2.0 * eps)

            elif var_type is VariableType.VECTOR and fun_type is FunctionType.SCALAR:
                J_eps = np.empty(dim_x[0])
                for i in range(dim_x[0]):
                    y_p_eps = fun(x + eps * identity_vec(dim=dim_x[0], i=i))
                    y_m_eps = fun(x - eps * identity_vec(dim=dim_x[0], i=i))
                    J_eps[i] = (y_p_eps - y_m_eps) / (2 * eps)

            elif var_type is VariableType.VECTOR and fun_type is FunctionType.VECTOR:
                J_eps = np.empty((dim_y[0], dim_x[0]))
                for i in range(dim_x[0]):
                    y_p_eps = fun(x + eps * identity_vec(dim=dim_x[0], i=i))
                    y_m_eps = fun(x - eps * identity_vec(dim=dim_x[0], i=i))
                    J_eps[:, i] = (y_p_eps - y_m_eps) / (2 * eps)

            elif var_type is VariableType.MATRIX and fun_type is FunctionType.SCALAR:
                J_eps = np.empty((dim_x[0], dim_x[1]))
                for i in range(dim_x[0]):
                    for j in range(dim_x[1]):
                        y_p_eps = fun(x + eps * identity_mat(dim_i=dim_x[0], dim_j=dim_x[1], i=i, j=j))
                        y_m_eps = fun(x - eps * identity_mat(dim_i=dim_x[0], dim_j=dim_x[1], i=i, j=j))
                        J_eps[i, j] = (y_p_eps - y_m_eps) / (2 * eps)

            J_diff = np.fabs(J_eps - J)
            if np.max(J_diff) > tol:
                result = False
            if (np.max(J_diff) > tol and verbose == 1) or verbose == 2:
                print("\nResults of numerical derivative check:")
                print("x \n", x)
                print("analytic Jacobian \n", J)
                print("numeric Jacobian \n", J_eps)
                print("J_analytic - J_numeric \n", J - J_eps)
                print("max absolute error ", np.max(J_diff))
                print("max absolute error index ", np.argmax(J_diff))

        if grad is not None and hess is not None:
            H = hess(x)
            if var_type is VariableType.SCALAR and fun_type is FunctionType.SCALAR:
                H_eps = (grad(x + eps) - grad(x - eps)) / (2.0 * eps)

            if var_type is VariableType.VECTOR and fun_type is FunctionType.SCALAR:
                H_eps = np.empty((dim_x[0], dim_x[0]))
                for i in range(dim_x[0]):
                    y_p_eps = grad(x + eps * identity_vec(dim_x[0], i))
                    y_m_eps = grad(x - eps * identity_vec(dim_x[0], i))
                    H_eps[i, :] = (y_p_eps - y_m_eps) / (2.0 * eps)

            H_diff = np.fabs(H_eps - H)
            if np.max(H_diff) > tol:
                result = False
            if (np.max(J_diff) > tol and verbose == 1) or verbose == 2:
                print("\nResults of numerical derivative check:")
                print("x \n", x)
                print("analytic Hessian \n", H)
                print("numeric Hessian \n", H_eps)
                print("H_analytic - H_numeric \n", H - H_eps)
                print("max absolute error ", np.max(H_diff))
                print("max absolute error index ", np.argmax(H_diff))

    return result
