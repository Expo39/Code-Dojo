# ROS 2 (placeholder track)

Last reviewed: not yet (placeholder). Before building it, research current courses and versions
with `dojo-new-track`.

Not built yet, and not part of any plan unless a learner chooses it in their roadmap
(`docs/ROADMAP.md`). When a plan reaches it, the tutor agrees the toolchain with the learner,
writes `track.json` (`docs/TRACKS.md`) and generates the first module only.

## Prerequisites

- Python fluency (first milestone of the Python track): `rclpy` nodes are written in Python.
- C++ basics (the first modules of the C/C++ track): `rclcpp` and most of the ecosystem use it.
- Linux and the terminal: processes, environment variables, packages.

## Theory (offered just in time, per module)

- Publish/subscribe and request/response messaging (before topics and services).
- Coordinate frames and transforms: translation, rotation, chaining frames (before tf2).
- Basic control loops and timing: rates, latency, why callbacks must stay short.

## Outline

Nodes, topics, services, actions, parameters, launch files, tf2, colcon, simulation in Gazebo,
then one small robot project.

## Toolchain

A ROS 2 distribution in a container (the official images) is the suggested default: it keeps
the host clean and pins the distribution.
