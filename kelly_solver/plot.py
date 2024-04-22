import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

def draw2dPlot(x, y, max_x=None, max_y=None):
    fig, ax = plt.subplots()
    ax.plot(x * 100, y)  # Multiply by 100 to convert to percentages
    ax.set_xlabel('Investment Portion (%)')
    ax.set_ylabel('Expected Return')
    ax.set_title('Expected Return vs. Investment Percentage')

    # Create a formatter function that adds a percentage sign at the end
    formatter = ticker.FuncFormatter(lambda y, _: f'{y}%')
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlim(0, 100)

    ax.grid(True)

    # If max_x and max_y are provided, annotate the plot with the maximum expected return
    if max_x is not None and max_y is not None:
        ax.scatter(max_x * 100, max_y, color='red')  # Highlight the max point
        ax.annotate(f'Max ROI: {max_y:.2f}\nAt {max_x * 100:.2f}%', xy=(max_x * 100, max_y), xycoords='data',
                    xytext=(max_x * 100 + 5, max_y), textcoords='data',
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3'),
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
        
    plt.show()


def draw3dPlot(x_grid, y_grid, values, points=None):
    # Plot the surface of the objective function
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    X, Y = np.meshgrid(x_grid, y_grid, indexing='ij')
    # Plot the surface
    surf = ax.plot_surface(X, Y, values, alpha=0.9, cmap='viridis', vmin=0)
    # Set labels and show plot
    fig.colorbar(surf, shrink=0.5, aspect=5)
    # Plot the Newton's method iteration points as a line
    if points is not None:
        ax.plot(points[:, 0], points[:, 1], points[:, 2], marker='o', color='r', markersize=5, label='Newton Iterations')
    ax.set_xlabel('Investment Percentage in Investment 1 (x)')
    ax.set_ylabel('Investment Percentage in Investment 2 (y)')
    ax.set_zlabel('Expected Logarithmic Growth Rate')
    ax.set_title('Expected Logarithmic Growth Rate for Investment Percentages')
    ax.legend()
    plt.show()


def draw3variablesPlot(x_range, y_range, z_range, values, points=None):
    # Flatten the ranges and values for plotting
    X, Y, Z = np.meshgrid(x_range, y_range, z_range, indexing='ij')
    X_flat = X.flatten()
    Y_flat = Y.flatten()
    Z_flat = Z.flatten()
    values_flat = values.flatten()

    valid_mask = (X_flat + Y_flat + Z_flat) < 1
    X_valid = X_flat[valid_mask]
    Y_valid = Y_flat[valid_mask]
    Z_valid = Z_flat[valid_mask]
    values_valid = values_flat[valid_mask]

    # Create a 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot with color coding
    scatter = ax.scatter(X_valid, Y_valid, Z_valid, c=values_valid, cmap='viridis', s=1)
    if points is not None:
        ax.plot(points[:, 0], points[:, 1], points[:, 2], marker='o', color='r', markersize=5, label='Newton Iterations')

    # Add a color bar to interpret the color coding
    cbar = fig.colorbar(scatter, shrink=0.5, aspect=5)
    cbar.set_label('Expected Logarithmic Growth Rate')

    # Set labels
    ax.set_xlabel('Investment Fraction 1')
    ax.set_ylabel('Investment Fraction 2')
    ax.set_zlabel('Investment Fraction 3')

    plt.show()


def drawProbability1D(R, P):
    fig, ax = plt.subplots()
    bar_width = np.min(np.diff(R)) * 0.8 if len(R) > 1 else 0.1
    ax.bar(R, P, width=bar_width, align='center', alpha=0.7)
    
    # Set x-axis ticks to match the R values
    ax.set_xticks(R)
    ax.set_xlabel('Returns')
    ax.set_ylabel('Probability')
    ax.set_title('Probability Distribution of Returns')
    
    plt.show()


def drawProbability2D(R, P):
    fig, ax = plt.subplots()
    heatmap = ax.imshow(P, cmap='viridis', origin='lower', aspect='auto')

    # Calculate the number of bins based on the shape of P
    num_bins = P.shape[0]
    
    # Calculate the tick locations based on the number of bins
    tick_locs = np.arange(num_bins)
    
    # Set the tick locations
    ax.set_xticks(tick_locs)
    ax.set_yticks(tick_locs)
    
    # If R represents the bin edges, calculate the bin centers for the labels
    if len(R) == num_bins + 1:
        bin_centers = (R[:-1] + R[1:]) / 2
        # Round the bin_centers to a certain number of decimal places
        bin_centers = np.round(bin_centers, 2)
        ax.set_xticklabels(bin_centers, rotation=45, ha='right')
        ax.set_yticklabels(bin_centers)
    else:
        # Round R to a certain number of decimal places
        R_rounded = np.round(R, 2)
        ax.set_xticklabels(R_rounded, rotation=45, ha='right')
        ax.set_yticklabels(R_rounded)

    cbar = fig.colorbar(heatmap)
    cbar.set_label('Probability')
    
    ax.set_xlabel('Return on Investment 1')
    ax.set_ylabel('Return on Investment 2')
    ax.set_title('Joint Probability Distribution of Returns')
    
    plt.show()