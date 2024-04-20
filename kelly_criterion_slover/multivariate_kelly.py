from typing import Tuple
import numpy as np


def expandDims(R: np.ndarray, dim: int, idx: int) -> np.ndarray:
        expanded_shape = np.ones(dim, dtype=int)
        expanded_shape[idx] = R.size
        return np.expand_dims(R, axis=tuple(range(idx)) + tuple(range(idx + 1, dim)))


def kellyCalculation(R: np.ndarray, P: np.ndarray, X: np.ndarray) -> Tuple[float, np.ndarray, np.ndarray]:
    """
    The function returns a single value represent the ROI for a given probability distribution and investment fraction.

    :param R: 1D array represent the range of return, example: [-10%, -5%, 0%, 5%, 10%]
    :param P: A N-dimension matrix represent the probability distribution for each investment's return combinition. Each dimention has the same length of R.
    :param X: 1D array with size N, represent the portion of each investment invested.

    :return: the log of ROI, positive means gain and negative means loss.
             the gradient
             the Hessian
    """
    assert all(len(R) == s for s in P.shape), "Each dimension of P must match the length of R"
    assert P.ndim == X.size, "The number of dimensions in P must match the size of X"
    assert np.sum(X) <= 1, "The sum of investment fractions must be less than or equal to 1"

    denominator = np.ones(P.shape)
    for i, x in enumerate(X):
        denominator += expandDims(R, X.size, i) * x

    value = np.sum(P * np.log(denominator))

    gradient = np.zeros_like(X)
    hessian = np.zeros((X.size, X.size))
    for i in range(X.size):
        Ri = expandDims(R, X.size, i)
        gradient[i] = np.sum(P * Ri / denominator)
        for j in range(X.size):
            Rj = expandDims(R, X.size, j)
            hessian[i, j] = -np.sum(P * Ri * Rj / denominator**2)

    return (value, gradient, hessian)


def kellyValue(R: np.ndarray, P: np.ndarray, X: np.ndarray) -> float:
    assert all(len(R) == s for s in P.shape), "Each dimension of P must match the length of R"
    assert P.ndim == X.size, "The number of dimensions in P must match the size of X"
    assert np.sum(X) <= 1, "The sum of investment fractions must be less than or equal to 1"

    denominator = np.ones(P.shape)
    for i, x in enumerate(X):
        denominator += expandDims(R, X.size, i) * x

    return np.sum(P * np.log(denominator))


def kellyValueV1(R: np.ndarray, P: np.ndarray, X: np.ndarray) -> float:
    assert all(len(R) == s for s in P.shape), "Each dimension of P must match the length of R"
    assert P.ndim == X.size, "The number of dimensions in P must match the size of X"
    assert np.sum(X) <= 1, "The sum of investment fractions must be less than or equal to 1"
    # Initialize an array to hold the growth rates for each combination of returns
    growth_rates = np.zeros(P.shape)
    
    # Compute the growth rate for each combination of returns and investment fractions
    for indices, _ in np.ndenumerate(growth_rates):
        denominator = 1 + sum(R[idx] * X[dim] for dim, idx in enumerate(indices))
        growth_rates[indices] = np.log(denominator)
    
    # Compute the expected logarithmic growth rate as the weighted sum of growth rates
    expected_growth_rate = np.sum(P * growth_rates)
    
    return expected_growth_rate


def kellyGradientV1(R: np.ndarray, P: np.ndarray, X: np.ndarray) -> np.ndarray:
    X = np.asarray(X)  # Ensure X is a numpy array
    
    # Initialize an array to hold the gradient for each investment
    gradient = np.zeros_like(X)
    
    # Compute the gradient for each investment fraction
    for i in range(X.size):

        first_derivative = np.zeros(P.shape)
        
        # Compute the partial growth rate for each combination of returns
        for indices, _ in np.ndenumerate(first_derivative):
            # Calculate the total return excluding the current investment
            denominator = 1 + sum(R[idx] * X[dim] for dim, idx in enumerate(indices))
            # Calculate the partial growth rate including the current investment
            first_derivative[indices] = R[indices[i]] / denominator
        
        # Compute the partial expected logarithmic growth rate as the weighted sum of partial growth rates
        gradient[i] = np.sum(P * first_derivative)
    
    return gradient


def kellyHessianV1(R: np.ndarray, P: np.ndarray, X: np.ndarray) -> np.ndarray:
    X = np.asarray(X)  # Ensure X is a numpy array

    hessian = np.zeros((X.size, X.size))
    # Compute the Hessian matrix for each pair of investment fractions
    for i in range(X.size):
        for j in range(X.size):

            second_derivative = np.zeros(P.shape)
                    
            # Compute the partial growth rate for each combination of returns
            for indices, _ in np.ndenumerate(second_derivative):
                # Calculate the total return excluding the current investment
                denominator = 1 + sum(R[idx] * X[dim] for dim, idx in enumerate(indices))
                # Calculate the partial growth rate including the current investment
                second_derivative[indices] = R[indices[i]] * R[indices[j]] / denominator ** 2
            
            hessian[i, j] = -np.sum(P * second_derivative)
    
    return hessian



def main():
    R_RANGE = 4
    DIMENSION = 8
    R = np.linspace(-1, 1, R_RANGE)
    P = np.random.dirichlet(np.ones(R.size ** DIMENSION)).reshape((R.size,) * DIMENSION)
    X = np.random.rand(DIMENSION)
    X = X / (np.sum(X) * 1.5) 

    kellyCalculation(R, P, X)


if __name__ == '__main__':
    main()