# Cutting Stock Problem: Column Generation

## Overview
This repository contains the implementation and experimental analysis of the **Cutting Stock Problem (CSP)** solved using the **Column Generation** algorithm (Dynamic Simplex). The project demonstrates how to effectively overcome the combinatorial explosion of the standard approach by dynamically generating only the most promising cutting patterns.

## Requirements
This project requires python 3 to be used. If that's installed on your system, use the command pip install -r requirements.txt on the root of the project to install all the required libraries.

## Usage
To run the program, just run the main file by using python3 main.py. Once done, you can analyze the data generated and create graphs by using the script analysis.py, available in the utils folder. All the data will be in the results folder.

## Modes
The program has 2 modes: generation mode (generate random instances) and loading mode (load already present instances). To switch modes, just change the MODALITA_CARICAMENTO variable in the main.py file (true = loading mode, false = generation mode). The project already comes with some generated data and is set by default to loading mode.

## Methodology
The algorithm is structured around two interconnected mathematical models:
* **Master Problem (Reduced):** Evaluates the linear relaxation using a restricted subset of known patterns and extracts the dual variables (**shadow prices**).
* **Pricing Problem (Slave):** Formulated as an Integer Knapsack Problem. It uses the shadow prices to find a new cutting pattern that minimizes the reduced cost, respecting the physical capacity of the main bar. If no improving pattern is found (value $\le 1$), the global optimum is certified.

## Experimental Setup
The algorithm's performance was evaluated on 80 synthetic instances across 8 classes, combining:
* **Number of Modules:** Few (5-10) vs. Many (45-55)
* **Demand:** Low (1-10) vs. High (50-100)
* **Main Bar Length:** Short (2-4x max module length) vs. Long (10-20x max module length)

## Key Results
* **Material Savings:** Achieved an average saving of **>80%** in the number of stock bars compared to a baseline heuristic.
* **Quality of Solution:** For high-demand instances (mass production), the gap between the relaxed optimum and the integer rounded solution is minimal (**9.21%**). For low-demand instances, the rounding step is more punitive.
* **Computational Performance:** The algorithm is highly scalable, solving the most complex instances in under **5 seconds** with a peak memory usage of just **0.29 MB**.
* **Convergence:** Instances with longer stock bars converge faster as the Pricing problem has more combinatorial freedom to pack modules efficiently.

## Tech Stack
* **Python:** Script orchestration, instance generation, and results analysis.
* **AMPL:** Mathematical modeling of the Master and Pricing problems.
* **Gurobi:** High-performance industrial solver used for numerical stability.

## Future Developments
For instances with extremely low demand where the integer rounding is heavily penalized, this model serves as the ideal foundation for an exact **Branch-and-Price** framework.