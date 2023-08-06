"""Plotting functions for 2D poses."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from mpl_toolkits.mplot3d import Axes3D  # pylint: disable=unused-import
from roboplot.basic import show_option


def plot_covariance_ellipse_2d(axes, origin, covariance, alpha=0.5):
    """
    Plots a Gaussian as an uncertainty ellipse

    Based on Maybeck Vol 1, page 366
    k=2.296 corresponds to 1 std, 68.26% of all probability
    k=11.82 corresponds to 3 std, 99.74% of all probability

    Args:
        axes (matplotlib.axes.Axes): Matplotlib axes.
        origin (gtsam.Point2): The origin in the world frame.
        covariance (numpy.ndarray): The marginal covariance matrix of the 2D point
            which will be represented as an ellipse.
        alpha (float): Transparency value for the plotted surface in the range [0, 1].
    """
    k = 2.296
    e, s = np.linalg.eig(covariance[0:2, 0:2])
    s1 = s[0, 0]
    s2 = s[1, 1]

    def ellipse(a, b, c):
        q = np.arange(0, 2*np.pi, 2*np.pi/25)
        ellipse_x = np.cos(q)
        ellipse_y = np.sin(q)

        points = a*ellipse_x + b*ellipse_y
        x = c[0] + points[0, :]
        y = c[1] + points[1, :]
        return x, y

    ex, ey = ellipse(np.sqrt(s1*k)*e[:, 0], np.sqrt(s2*k)*e[:, 2], origin[0:2])

    axes.line(ex, ey, alpha=alpha, cmap='hot')


def plot_point2_on_axes(axes, point, linespec, covariance=None):
    """
    Plot a 2D point on given axis `axes` with given `linespec`.

    Args:
        axes (matplotlib.axes.Axes): Matplotlib axes.
        point (gtsam.Point2): The point to be plotted.
        linespec (string): String representing formatting options for Matplotlib.
        covariance (numpy.ndarray): Marginal covariance matrix to plot the uncertainty of the estimation.
    """
    axes.plot([point[0]], [point[1]], linespec)
    if covariance is not None:
        plot_covariance_ellipse_2d(axes, point, covariance)


def plot_point2(point, fignum=0, linespec="g*", covariance=None,
                axis_labels=('X axis', 'Y axis')):
    """
    Plot a 2D point on given figure with given `linespec`.

    Args:
        point (gtsam.Point2): The point to be plotted.
        fignum (int): Integer representing the figure number to use for plotting.
        linespec (string): String representing formatting options for Matplotlib.
        covariance (numpy.ndarray): Marginal covariance matrix to plot the uncertainty of the estimation.
        axis_labels (iterable[string]): List of axis labels to set.

    Returns:
        fig: The matplotlib figure.

    """
    fig = plt.figure(fignum)
    axes = fig.gca()
    plot_point2_on_axes(axes, point, linespec, covariance)

    axes.set_xlabel(axis_labels[0])
    axes.set_ylabel(axis_labels[1])

    return fig


@show_option
def plot_2d_points(values, fignum=0, linespec="g*", marginals=None,
                   title="2D Points", axis_labels=('X axis', 'Y axis')):
    """
    Plots the Point2s in `values`, with optional covariances.
    Finds all the Point2 objects in the given Values object and plots them.
    If a Marginals object is given, this function will also plot marginal
    covariance ellipses for each point.

    Args:
        values (gtsam.Values): Values dictionary consisting of points to be plotted.
        fignum (int): Integer representing the figure number to use for plotting.
        linespec (string): String representing formatting options for Matplotlib.
        marginals (numpy.ndarray): Marginal covariance matrix to plot the
            uncertainty of the estimation.
        title (string): The title of the plot.
        axis_labels (iterable[string]): List of axis labels to set.
    """

    keys = values.keys()

    # Plot points and covariance matrices
    for key in keys:
        try:
            point = values.atPoint2(key)
            if marginals is not None:
                covariance = marginals.marginalCovariance(key)
            else:
                covariance = None

            fig = plot_point2(point, fignum=fignum,
                              linespec=linespec,
                              covariance=covariance,
                              axis_labels=axis_labels)

        except RuntimeError:
            continue
            # I guess it's not a Point2

    fig = plt.figure(fignum)
    fig.suptitle(title)
    fig.canvas.set_window_title(title.lower())


def plot_pose2_on_axes(axes, pose, axis_length=0.1, covariance=None, k=5.0):
    """
    Plot a 2D pose on given axis `axes` with given `axis_length`.

    Args:
        axes (matplotlib.axes.Axes): Matplotlib axes.
        pose (gtsam.Pose2): The pose to be plotted.
        axis_length (float): The length of the camera axes.
        covariance (numpy.ndarray): Marginal covariance matrix
                to plot the uncertainty of the estimation.
        k (float): Covariance scaling factor. Default 5.0
    """
    # get rotation and translation (center)
    gRp = pose.rotation().matrix()  # rotation from pose to global
    origin = pose.translation()

    # draw the camera axes
    x_axis = origin + gRp[:, 0] * axis_length
    line = np.append(origin[np.newaxis], x_axis[np.newaxis], axis=0)
    axes.plot(line[:, 0], line[:, 1], 'r-')

    y_axis = origin + gRp[:, 1] * axis_length
    line = np.append(origin[np.newaxis], y_axis[np.newaxis], axis=0)
    axes.plot(line[:, 0], line[:, 1], 'g-')

    if covariance is not None:
        pPp = covariance[0:2, 0:2]
        gPp = np.matmul(np.matmul(gRp, pPp), gRp.T)

        w, v = np.linalg.eig(gPp)

        angle = np.arctan2(v[1, 0], v[0, 0])
        e1 = patches.Ellipse(origin, np.sqrt(w[0]*k), np.sqrt(w[1]*k),
                             np.rad2deg(angle), fill=False)
        axes.add_patch(e1)


def plot_pose2(pose, fignum=0, axis_length=0.1, covariance=None,
               axis_labels=('X axis', 'Y axis', 'Z axis')):
    """
    Plot a 2D pose on given figure with given `axis_length`.

    Args:
        pose (gtsam.Pose2): The pose to be plotted.
        fignum (int): Integer representing the figure number to use for plotting.
        axis_length (float): The length of the camera axes.
        covariance (numpy.ndarray): Marginal covariance matrix to plot
                the uncertainty of the estimation.
        axis_labels (iterable[string]): List of axis labels to set.
    """
    # get figure object
    fig = plt.figure(fignum)
    axes = fig.gca()
    plot_pose2_on_axes(axes, pose, axis_length=axis_length,
                       covariance=covariance)

    axes.set_xlabel(axis_labels[0])
    axes.set_ylabel(axis_labels[1])

    return fig
