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


def draw3dPlot(x_grid, y_grid, z_grid, points=None):
    # Plot the surface of the objective function
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Plot the surface
    surf = ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.9, cmap='viridis', vmin=0)
    # Set labels and show plot
    fig.colorbar(surf, shrink=0.5, aspect=5)
    # ax.scatter(max_x, max_y, max_z, color='red', s=50)
    # Plot the Newton's method iteration points as a line
    if points is not None:
        ax.plot(points[:, 0], points[:, 1], points[:, 2], marker='o', color='r', markersize=5, label='Newton Iterations')
    ax.set_xlabel('Investment Percentage in Investment 1 (x)')
    ax.set_ylabel('Investment Percentage in Investment 2 (y)')
    ax.set_zlabel('Expected Logarithmic Growth Rate')
    ax.set_title('Expected Logarithmic Growth Rate for Investment Percentages')
    ax.legend()
    plt.show()


def drawProbability(R, P):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Create a grid for the x and y coordinates
    x_pos, y_pos = np.meshgrid(R, R)
    x_pos = x_pos.flatten()
    y_pos = y_pos.flatten()
    z_pos = np.zeros_like(x_pos)

    # Set the height of the bars as the probabilities
    dx = dy = 0.5  # Width of the bars
    dz = P.flatten()

    # Create the bar plot
    ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, shade=True)

    # Set labels
    ax.set_xlabel('Return on Investment 1')
    ax.set_ylabel('Return on Investment 2')
    ax.set_zlabel('Probability')

    # Show the plot
    plt.show()
