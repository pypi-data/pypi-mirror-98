# roboplot

Library of plotting functions for everything robotics

## About

`roboplot` aims to provide a set of easy to use functions for plotting various data and visualizations related to robotics.
The goal is for this to be fully featured and easy to use, in a functional style, to aid in rapid prototyping.

As such, `roboplot` leverages `gtsam` heavily for access to robotics primitives that are easy to work with. `gtsam` supports conversions to and from other libraries, in case you prefer something else.

## Installation

Simply run

```sh
pip install roboplot
```

To install a development version, run `pip install -e .` in the root directory.

## Documentation

TODO!

### Feature Requests

- Support for measurement streams
- Add [meshcat](https://github.com/rdeits/meshcat-python) support so we can view plots on browsers.
- Support for [Polyscope](https://github.com/nmwsharp/polyscope) for 3D geometry plotting.
- [bqplot](https://github.com/bqplot/bqplot)
- [IPyVolume](https://ipyvolume.readthedocs.io/en/latest/) for 3D shapes?
