"""Plotting functions for 3D poses and points."""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from numpy.core.function_base import linspace  # pylint: disable=unused-import
from roboplot.basic import show_option


def ellipsoid(rx, ry, rz, n):
    """
    Numpy equivalent of Matlab's ellipsoid function.

    Args:
        rx (double): Radius of ellipsoid in X-axis.
        ry (double): Radius of ellipsoid in Y-axis.
        rz (double): Radius of ellipsoid in Z-axis.
        n (int): The granularity of the ellipsoid plotted.

    Returns:
        tuple[numpy.ndarray]: The points in the x, y and z axes to use for the surface plot.
    """
    u = np.linspace(0, 2 * np.pi, n + 1)
    v = np.linspace(0, np.pi, n + 1)
    x = -rx * np.outer(np.cos(u), np.sin(v)).T
    y = -ry * np.outer(np.sin(u), np.sin(v)).T
    z = -rz * np.outer(np.ones_like(u), np.cos(v)).T

    return x, y, z


def plot_covariance_ellipse_3d(axes,
                               origin,
                               covariance,
                               scale=1,
                               n=8,
                               alpha=0.5):
    """
    Plots a Gaussian as an uncertainty ellipse

    Based on Maybeck Vol 1, page 366
    k=2.296 corresponds to 1 std, 68.26% of all probability
    k=11.82 corresponds to 3 std, 99.74% of all probability

    Args:
        axes (matplotlib.axes.Axes): Matplotlib axes.
        origin (gtsam.Point3): The origin in the world frame.
        covariance (numpy.ndarray): The marginal covariance matrix of the 3D point
                which will be represented as an ellipse.
        scale (float): Scaling factor of the radii of the covariance ellipse.
        n (int): Defines the granularity of the ellipse. Higher values indicate finer ellipses.
        alpha (float): Transparency value for the plotted surface in the range [0, 1].
    """
    k = 11.82
    U, S, _ = np.linalg.svd(covariance)

    radii = k * np.sqrt(S)
    radii = radii * scale
    rx, ry, rz = radii

    # generate data for "unrotated" ellipsoid
    xc, yc, zc = ellipsoid(rx, ry, rz, n)

    # rotate data with orientation matrix U and center c
    data = np.kron(U[:, 0:1], xc) + np.kron(U[:, 1:2], yc) + \
        np.kron(U[:, 2:3], zc)
    n = data.shape[1]
    x = data[0:n, :] + origin[0]
    y = data[n:2 * n, :] + origin[1]
    z = data[2 * n:, :] + origin[2]

    axes.plot_surface(x, y, z, alpha=alpha, cmap='hot')


def plot_point3_on_axes(axes, point, linespec, covariance=None):
    """
    Plot a 3D point on given axis `axes` with given `linespec`.

    Args:
        axes (matplotlib.axes.Axes): Matplotlib axes.
        point (gtsam.Point3): The point to be plotted.
        linespec (string): String representing formatting options for Matplotlib.
        covariance (numpy.ndarray): Marginal covariance matrix to plot the uncertainty of the estimation.
    """
    axes.plot([point[0]], [point[1]], [point[2]], linespec)
    if covariance is not None:
        plot_covariance_ellipse_3d(axes, point, covariance)


def plot_point3(point,
                fignum=0,
                linespec="g*",
                covariance=None,
                axis_labels=('X axis', 'Y axis', 'Z axis')):
    """
    Plot a 3D point on given figure with given `linespec`.

    Args:
        point (gtsam.Point3): The point to be plotted.
        linespec (string): String representing formatting options for Matplotlib.
        fignum (int): Integer representing the figure number to use for plotting.
        covariance (numpy.ndarray): Marginal covariance matrix to plot the uncertainty of the estimation.
        axis_labels (iterable[string]): List of axis labels to set.

    Returns:
        fig: The matplotlib figure.

    """
    fig = plt.figure(fignum)
    axes = fig.gca(projection='3d')
    plot_point3_on_axes(axes, point, linespec, covariance)

    axes.set_xlabel(axis_labels[0])
    axes.set_ylabel(axis_labels[1])
    axes.set_zlabel(axis_labels[2])

    return fig


@show_option
def plot_3d_points(values,
                   fignum=0,
                   linespec="g*",
                   marginals=None,
                   title="3D Points",
                   axis_labels=('X axis', 'Y axis', 'Z axis')):
    """
    Plots the Point3s in `values`, with optional covariances.
    Finds all the Point3 objects in the given Values object and plots them.
    If a Marginals object is given, this function will also plot marginal
    covariance ellipses for each point.

    Args:
        values (gtsam.Values): Values dictionary consisting of points to be plotted.
        fignum (int): Integer representing the figure number to use for plotting.
        linespec (string): String representing formatting options for Matplotlib.
        marginals (numpy.ndarray): Marginal covariance matrix to plot
                the uncertainty of the estimation.
        title (string): The title of the plot.
        axis_labels (iterable[string]): List of axis labels to set.
    """

    keys = values.keys()

    # Plot points and covariance matrices
    for key in keys:
        try:
            point = values.atPoint3(key)
            if marginals is not None:
                covariance = marginals.marginalCovariance(key)
            else:
                covariance = None

            fig = plot_point3(point,
                              fignum=fignum,
                              linespec=linespec,
                              covariance=covariance,
                              axis_labels=axis_labels)

        except RuntimeError:
            continue
            # I guess it's not a Point3

    fig = plt.figure(fignum)
    fig.suptitle(title)
    fig.canvas.set_window_title(title.lower())


def plot_pose3_on_axes(axes, pose, axis_length=0.1, covariance=None):
    """
    Plot a 3D pose on given axis `axes` with given `axis_length`.

    Args:
        axes (matplotlib.axes.Axes): Matplotlib axes.
        point (gtsam.Point3): The point to be plotted.
        linespec (string): String representing formatting options for Matplotlib.
        covariance (numpy.ndarray): Marginal covariance matrix to plot the uncertainty of the estimation.
    """
    # get rotation and translation (center)
    gRp = pose.rotation().matrix()  # rotation from pose to global
    origin = pose.translation()

    # draw the camera axes
    x_axis = origin + gRp[:, 0] * axis_length
    line = np.append(origin[np.newaxis], x_axis[np.newaxis], axis=0)
    axes.plot(line[:, 0], line[:, 1], line[:, 2], 'r-')

    y_axis = origin + gRp[:, 1] * axis_length
    line = np.append(origin[np.newaxis], y_axis[np.newaxis], axis=0)
    axes.plot(line[:, 0], line[:, 1], line[:, 2], 'g-')

    z_axis = origin + gRp[:, 2] * axis_length
    line = np.append(origin[np.newaxis], z_axis[np.newaxis], axis=0)
    axes.plot(line[:, 0], line[:, 1], line[:, 2], 'b-')

    # plot the covariance
    if covariance is not None:
        # covariance matrix in pose coordinate frame
        pPp = covariance[3:6, 3:6]
        # convert the covariance matrix to global coordinate frame
        gPp = gRp @ pPp @ gRp.T
        plot_covariance_ellipse_3d(axes, origin, gPp)


@show_option
def plot_pose3(pose,
               fignum=0,
               axis_length=0.1,
               covariance=None,
               axis_labels=('X axis', 'Y axis', 'Z axis')):
    """
    Plot a 3D pose on given figure with given `axis_length`.

    Args:
        pose (gtsam.Pose3): 3D pose to be plotted.
        fignum (int): Integer representing the figure number to use for plotting.
        linespec (string): String representing formatting options for Matplotlib.
        covariance (numpy.ndarray): Marginal covariance matrix to plot the uncertainty of the estimation.
        axis_labels (iterable[string]): List of axis labels to set.

    Returns:
        fig: The matplotlib figure.
    """
    # get figure object
    fig = plt.figure(fignum)
    axes = fig.gca(projection='3d')
    plot_pose3_on_axes(axes,
                       pose,
                       covariance=covariance,
                       axis_length=axis_length)

    axes.set_xlabel(axis_labels[0])
    axes.set_ylabel(axis_labels[1])
    axes.set_zlabel(axis_labels[2])

    return fig
