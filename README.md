# Grid-based Demo for Space Layout Design

This repository provides a grid-based simulation framework for space layout design.  
It serves as a prototype environment for experimenting with layout representation, movement dynamics, and performance evaluation metrics.

The project is intended as a foundation for future reinforcement learning-based layout optimisation research.


## Requirements

- Python 3.10
- Install dependencies via `requirements.txt`


## Structure

```markdown

grid_demo/
│
├── evaluation/               # performance metrics
├── scenario/                 # grid map and agent definition
├── utils/                    # scenario initialisation
├── visualisation/
├── main.py # entry point
├── config.py
├── README.md
└── requirements.txt

```


## Features

The demo provides the following functionalities:

- Supports customised the grid map, including facility types, quantities, footprint, and initial positions.
- Supports customised agents, including types, quantities, initial positions, movement rules, and task chains.
- Supports both single-task simulations and continuous/indefinite simulations.

