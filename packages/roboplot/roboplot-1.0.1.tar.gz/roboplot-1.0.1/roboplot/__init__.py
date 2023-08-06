from matplotlib.pyplot import show

from roboplot.trajectory.two_d import *
from roboplot.trajectory.three_d import *
from roboplot.trajectory.trajectory import *
from roboplot.graph import *
try:
    from roboplot.robot import *
except ImportError:
    print("GTDynamics unavailable. Robot plotting features not enabled.")
