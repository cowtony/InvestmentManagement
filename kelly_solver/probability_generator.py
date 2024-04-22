import numpy as np
from scipy.stats import multivariate_normal, norm


def generateNdRandom(r_size: int, dimension: int) -> np.ndarray:
    return np.random.dirichlet(np.ones(r_size ** dimension)).reshape((r_size,) * dimension)


def generate1dGaussian(R: np.ndarray, mean: float, sigma: float) -> np.ndarray:
    """
    Generate a 1D Gaussian probability distribution for logarithmic returns.

    :param R: 1D array representing the range of returns.
    :param mean: Mean of the logarithmic returns.
    :param sigma: Standard deviation of the logarithmic returns.
    :return: 1D array representing the probability distribution for each return.
    """
    # Calculate the logarithmic returns
    log_returns = np.log(1 + R)

    # Calculate the PDF of the normal distribution for the log returns
    probabilities = norm.pdf(log_returns, loc=mean, scale=sigma)

    # Normalize the probabilities to sum to 1
    probabilities /= probabilities.sum()

    return probabilities


def generateGaussian(R, means, sigmas):
    assert means.size == sigmas.size

    dimension = means.size
   # Create an N-dimensional meshgrid of return values
    meshgrids = np.meshgrid(*([R] * dimension), indexing='ij')
    positions = np.vstack([grid.ravel() for grid in meshgrids]).T

    # Calculate the joint probability density at each point
    covariance_matrix = np.diag(sigmas ** 2)  # Assuming independence with diagonal covariance matrix
    joint_pdf = multivariate_normal.pdf(positions, mean=means, cov=covariance_matrix)

    # Normalize the joint PDF to get the joint probabilities that sum to 1
    joint_probabilities = joint_pdf / joint_pdf.sum()

    # Reshape the flat array of probabilities back into an N-dimensional matrix
    return joint_probabilities.reshape((R.size,) * dimension)


def generate2dindependent(P1: np.ndarray, P2: np.ndarray) -> np.ndarray:
    P = np.outer(P1, P2)
    P /= P.sum()
    return P


def generate2dCorrelated(P: np.ndarray) -> np.ndarray:
    """
    Generate a 2D probability distribution from a 1D probability distribution
    with 100% correlation between the two variables.

    :param P1: 1D array representing the probability distribution.
    :return: 2D array representing the joint probability distribution.
    """
    P_joint = np.zeros((P.size, P.size))  # Initialize a 2D array with zeros
    np.fill_diagonal(P_joint, P)  # Place the 1D distribution along the diagonal of the 2D array
    return P_joint


def test():
    STATE_SIZE = 11
    R = np.linspace(-1, 1, STATE_SIZE)
    P = generate1dGaussian(R, 0, 0.1)
    print(P)

test()