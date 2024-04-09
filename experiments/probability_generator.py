import numpy as np
from scipy.stats import multivariate_normal

def generate2dGaussian(R, means, sigmas):
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