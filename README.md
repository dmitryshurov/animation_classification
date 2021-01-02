# Animation classification

## About the project

This project is a WIP prototype of an experimantal skeleton-based animation classification system. Developed in Python 3.7.

It uses brute force sliding window search to compare library animations to the recorded animations and calculates the score. It then lays out library animations on the timeline to reconstruct the best match.

## Quickstart

From the project root directory, do the following steps.

Install dependencies:
```
pip install requirements.txt
```

Set up the environment (Windows)
```
set PYTHONPATH=%PYTHONPATH%;%CD%/src
```

Set up the environment (Linux)
```
export PYTHONPATH=${PYTHONPATH}:${PWD}/src
```

Run unit tests (optional)
```
python -m unittest discover
```

Run the demo
```
python demos/animation_recognition_demo.py data/recorded_animation.chan data/animation_library 
```

Build UML