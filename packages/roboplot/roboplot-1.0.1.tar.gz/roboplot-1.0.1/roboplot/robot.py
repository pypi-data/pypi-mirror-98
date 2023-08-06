import gtdynamics
import gtsam
import matplotlib.pyplot as plt

from roboplot.basic import set_axes_equal, set_title, show_option
from roboplot.trajectory.three_d import plot_pose3


@show_option
def plot_robot(robot: gtdynamics.Robot,
               root_link: str,
               fignum: int = 0,
               title: str = ""):
    """
    Plot the robot joints with connected links. Allows for visualizing robot models.

    Args:
        robot: The robot model as defined in GTDynamics.
        root_link: The base link in the provided robot.
        fignum: The figure number to plot on.
    """
    def dfs(robot, link_name):
        """Perform Depth-First-Search to get the robot tree."""
        link = robot.link(link_name)

        # append key type so there is no overwriting
        link_name += "_linkkey"

        node = {}
        node[link_name] = {}

        joints = link.getJoints()
        for j in joints:
            childLink = robot.joint(j.name()).child()

            if childLink.name() == link.name():
                continue

            # append key type so there is no overwriting
            joint_name = j.name() + "_jointkey"

            node[link_name][joint_name] = dfs(robot, childLink.name())

        return node

    # Generate the tree of links and joints via a Depth-First Search.
    robotTree = dfs(robot, root_link)

    # Plot the base link frame.
    base = robot.link(root_link)
    plot_pose3(base.wTl(), fignum=fignum)

    def preorder(tree, key):
        """
        Traverse robot tree in pre-order format to plot the joints.
        
        We traverse over links so we can get the connections between joints.

        Args:
            tree: The result of running DFS on the robot.
            key: The node key to start traversal from.
        """
        if "_linkkey" in key:
            link = robot.link(key.replace("_linkkey", ""))

            xs, ys, zs = [], [], []

            for joint in link.getJoints():
                # If the joint's parent is the root link, add a connection to it.
                if joint.parent().name() == root_link:
                    xs.append(base.wTl().translation()[0])
                    ys.append(base.wTl().translation()[1])
                    zs.append(base.wTl().translation()[2])

                wTj = joint.wTj()

                xs.append(wTj.translation()[0])
                ys.append(wTj.translation()[1])
                zs.append(wTj.translation()[2])
                plot_pose3(wTj, fignum=fignum, axis_length=0.05)

            plt.plot(xs, ys, zs, "-k")

        child_keys = tree[key].keys()
        for child_key in child_keys:
            preorder(tree[key], child_key)

    # Run preorder traversal to plot the links correctly
    preorder(robotTree, root_link + "_linkkey")

    # Set the axes to be proportional
    set_axes_equal(fignum)

    # Set the figure and window titles
    fig = set_title(fignum, title)

    return fig
