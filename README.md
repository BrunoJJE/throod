# ThrooD : VR pass-through effect on a conventional monitor

This is a git repository for the project described here :

https://www.hackster.io/brunojje/throod-vr-pass-through-effect-on-a-conventional-monitor-f2d06f


## Presentation

A webcam is pointing at the user to track his eyes to precisely detect his point of view to display on the monitor a see-through illusion.

It uses :

* [Mediapipe](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker) for [eye tracking](https://research.google/blog/mediapipe-iris-real-time-iris-tracking-depth-estimation/)

* [UPBGE (Blender Game Engine)](https://upbge.org) for interactive rendering


## Installing

Install UPBGE and Mediapipe so mediapipe is available to the python used by UPBGE.

Clone this repository to get the ThrooD project files.


## Usage

Launch the rendering of the "eyes.blend" project file with UPBGE.

    $ blenderplayer blender_eyes/eyes.blend

This will display a scene made of cubes with a view point that is changed according to the position of your eyes.

Use the ESC key to quit.


## Warning

The performances is poor for now.

To get better performance, an objective of this project is to use the XDNA of the AMD Ryzen AI CPU to accelerate the iris and the hands tracking (cf. this project also track your hands, but this is not used in the rendering for now). 

