"""Functions to plot trajectories."""

import gtsam
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from mpl_toolkits.mplot3d import Axes3D  # pylint: disable=unused-import
from roboplot.basic import show_option, set_axes_equal
from roboplot.trajectory.three_d import plot_pose3_on_axes
from roboplot.trajectory.two_d import plot_pose2_on_axes


@show_option
def plot_trajectory(values,
                    fignum=0,
                    scale=1,
                    marginals=None,
                    title="Plot Trajectory",
                    axis_labels=('X axis', 'Y axis', 'Z axis'),
                    axes_equal=True):
    """
    Plot a complete 2D/3D trajectory using poses in `values`.

    Args:
        values (gtsam.Values): Values containing some Pose2 and/or Pose3 values.
        fignum (int): Integer representing the figure number to use for plotting.
        scale (float): Value to scale the poses by.
        marginals (gtsam.Marginals): Marginalized probability values of the estimation.
            Used to plot uncertainty bounds.
        title (string): The title of the plot.
        axis_labels (iterable[string]): List of axis labels to set.
        axis_equal (bool): Flag to equi-scale all the plotting axes. Default is True.
    """
    fig = plt.figure(fignum)
    axes = fig.gca(projection='3d')

    axes.set_xlabel(axis_labels[0])
    axes.set_ylabel(axis_labels[1])
    axes.set_zlabel(axis_labels[2])

    # Plot 2D poses, if any
    poses = gtsam.utilities.allPose2s(values)
    for key in poses.keys():
        pose = poses.atPose2(key)
        if marginals:
            covariance = marginals.marginalCovariance(key)
        else:
            covariance = None

        plot_pose2_on_axes(axes,
                           pose,
                           covariance=covariance,
                           axis_length=scale)

    # Then 3D poses, if any
    poses = gtsam.utilities.allPose3s(values)
    for key in poses.keys():
        pose = poses.atPose3(key)

        # Get the covariance matrix
        if marginals:
            covariance = marginals.marginalCovariance(key)
        else:
            covariance = None

        plot_pose3_on_axes(axes,
                           pose,
                           covariance=covariance,
                           axis_length=scale)

    fig.suptitle(title)
    fig.canvas.set_window_title(title.lower())

    if axes_equal:
        # Update the plot space to encompass all plotted points
        axes.autoscale()
        # Set the 3 axes equal
        set_axes_equal(fignum)


@show_option
def plot_incremental_trajectory(values,
                                fignum=0,
                                start=0,
                                scale=1,
                                marginals=None,
                                time_interval=0.1,
                                title="Plot Trajectory",
                                axis_labels=('X axis', 'Y axis', 'Z axis'),
                                axes_equal=True):
    """
    Incrementally plot a complete 3D trajectory using poses in `values`.

    Useful for generating trajectory animations.

    Args:
        values (gtsam.Values): Values dict containing the poses.
        fignum (int): Integer representing the figure number to use for plotting.
        start (int): Starting index to start plotting from.
        scale (float): Value to scale the poses by.
        marginals (gtsam.Marginals): Marginalized probability values of the estimation.
            Used to plot uncertainty bounds.
        time_interval (float): Time in seconds to pause between each rendering.
            Used to create animation effect.
    """
    fig = plt.figure(fignum)
    axes = fig.gca(projection='3d')

    axes.set_xlabel(axis_labels[0])
    axes.set_ylabel(axis_labels[1])
    axes.set_zlabel(axis_labels[2])

    # Plot 2D poses, if any
    poses = gtsam.utilities.allPose2s(values)
    keys = gtsam.KeyVector(poses.keys())

    for key in keys[start:]:
        pose = poses.atPose2(key)
        if marginals:
            covariance = marginals.marginalCovariance(key)
        else:
            covariance = None

        plot_pose2_on_axes(axes,
                           pose,
                           covariance=covariance,
                           axis_length=scale)

    # Plot 3D poses, if any
    poses = gtsam.utilities.allPose3s(values)
    keys = gtsam.KeyVector(poses.keys())

    for key in keys[start:]:
        if values.exists(key):
            pose_i = values.atPose3(key)

            # Get the covariance matrix
            if marginals:
                covariance = marginals.marginalCovariance(key)
            else:
                covariance = None

            plot_pose3_on_axes(axes,
                               pose_i,
                               covariance=covariance,
                               axis_length=scale)

    fig.suptitle(title)
    fig.canvas.set_window_title(title.lower())

    if axes_equal:
        # Update the plot space to encompass all plotted points
        axes.autoscale()
        # Set the 3 axes equal
        set_axes_equal(fignum)

    # Pause for a fixed amount of seconds
    plt.pause(time_interval)
