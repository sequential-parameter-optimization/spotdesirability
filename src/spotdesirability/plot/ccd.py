import numpy as np
import matplotlib.pyplot as plt


def plotCCD(elev=20, azim=30)-> None:
    """
    Plots a Central Composite Design (CCD) for k=3 with customizable viewpoint.

    Args:
        elev (int): Elevation angle in the z-plane for the 3D plot.
        azim (int): Azimuthal angle in the x,y-plane for the 3D plot.

    Returns:
        None
    """
    # Define the number of factors (k) and axial distance (alpha)
    k = 3
    alpha = np.sqrt(k)  # Rotatable CCD

    # Generate factorial points (2^k design)
    factorial_points = np.array([[x1, x2, x3] for x1 in [-1, 1] for x2 in [-1, 1] for x3 in [-1, 1]])

    # Generate axial (star) points
    axial_points = []
    for i in range(k):
        point_positive = [0] * k
        point_negative = [0] * k
        point_positive[i] = alpha
        point_negative[i] = -alpha
        axial_points.append(point_positive)
        axial_points.append(point_negative)
    axial_points = np.array(axial_points)

    # Center point
    center_point = np.array([[0, 0, 0]])

    # Plot the CCD
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Plot factorial points
    ax.scatter(factorial_points[:, 0], factorial_points[:, 1], factorial_points[:, 2], c="blue", label="Factorial Points (2^k)", s=50)

    # Plot axial points
    ax.scatter(axial_points[:, 0], axial_points[:, 1], axial_points[:, 2], c="red", label="Axial Points (±α)", s=50)

    # Plot center point
    ax.scatter(center_point[:, 0], center_point[:, 1], center_point[:, 2], c="green", label="Center Point", s=100)

    # Connect edges of the cube (factorial points)
    for i in range(len(factorial_points)):
        for j in range(i + 1, len(factorial_points)):
            # Check if points differ by only one coordinate
            if np.sum(np.abs(factorial_points[i] - factorial_points[j])) == 2:
                ax.plot(
                    [factorial_points[i, 0], factorial_points[j, 0]], [factorial_points[i, 1], factorial_points[j, 1]], [factorial_points[i, 2], factorial_points[j, 2]], color="black", linewidth=0.5
                )

    # Add axes through the origin
    ax.plot([-alpha, alpha], [0, 0], [0, 0], color="gray", linestyle="--", label="X1 Axis")
    ax.plot([0, 0], [-alpha, alpha], [0, 0], color="gray", linestyle="--", label="X2 Axis")
    ax.plot([0, 0], [0, 0], [-alpha, alpha], color="gray", linestyle="--", label="X3 Axis")

    # Set plot labels
    ax.set_xlabel("X1")
    ax.set_ylabel("X2")
    ax.set_zlabel("X3")
    ax.set_title("Central Composite Design (CCD) for k=3")

    # Set the viewpoint
    ax.view_init(elev=elev, azim=azim)

    # Add legend
    ax.legend()

    # Show the plot
    plt.show()
