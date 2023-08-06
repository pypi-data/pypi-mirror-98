"""Classes and functions to plot sensor data."""

from matplotlib import pyplot as plt

from roboplot.basic import multirow, show_option


@show_option
def plot_measurements(x, y, fignum=0, xlabel="x", ylabel="y", color="b", title="Measurements"):
    """
    Plot a set of measurements as a line graph.

    Args:
        x: The x-axis data.
        y: The y-axis data.
        fignum: The figure number to plot this on.
        xlabel: The label on the x-axis.
        ylabel: The label on the y-axis.
        color: Color of the line plot (default is blue).
        title: Title of the plot.

    Returns:
        A matplotlib Figure.
    """
    fig = plt.figure(fignum)
    ax = fig.gca()

    ax.plot(x, y, "tab:{}".format(color))
    ax.set(xlabel=xlabel, ylabel=ylabel)

    fig.suptitle(title)
    fig.canvas.set_window_title(title.lower())

    return fig


@show_option
def plot_multirow_measurements(x, y, fignum=0,
                               xlabels=("x1", "x2", "x3"), ylabels=("y1", "y2", "y3"),
                               colors=("r", "g", "b"),
                               title="Multiple Measurements",
                               row_titles=("X1", "X2", "X3"),
                               normalize=False):
    """
    Plot multiple measurements over multiple rows for easy viewing and comparisons.

    Args:
        x: The x-axis data. Common to all y-axis data rows.
        y: The y-axis data. This is a NxR matrix of R sets of N data points.
        fignum: The figure number to plot this on.
        xlabels: The labels on the x-axis.
        ylabel: The labels on the y-axis.
        color: Colors of each of the line plots.
        title: Title of the plot.
        row_title: The title of each individual subplot.
        normalize: Flag to scale both axes to be of similar range.

    Returns:
        A matplotlib Figure.
    """
    fig = multirow(x, y, fignum=fignum,
                   xlabels=xlabels, ylabels=ylabels, title=title,
                   row_titles=row_titles, colors=colors,
                   normalize=normalize,
                   show=plot_multirow_measurements.__wrapped__.show,)

    return fig
