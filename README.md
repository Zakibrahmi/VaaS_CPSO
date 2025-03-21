# Vehicle-as-a-Service Composition using Composite Particle Swarm Optimization

This repository contains the implementation of the solution proposed in the paper:  
**"Vehicle as a Service: Multi-modal Transportation Service Selection with Composite Particle Swarm Optimization"** *(currently under review)*.

The solution is designed to generate a **Vehicle-as-a-Service (VaaS) Composition** in **Smart Urban Networks**, focusing on efficient multi-modal transportation service selection.

## Getting Started

### Prerequisites
Ensure you have Python installed on your system. You can install the required dependencies using:
```bash
pip install -r requirements.txt
```
## Running the Code

To execute the solution, run the following command while commited instruction according to the scenario to be executed:
```bash
python main.py
```

## 📂 Repository Structure

The repository is organized as follows:


### Folder Descriptions:
- **`main.py`**: The main script to execute the solution and experiments.
- **`netwrok_smart/region.py`**: Script to generate regions datasets for simulations and others functions.
- **`netwrok_smart/vaas.py`**: Script to generate VaaSs datasets for simulations and others functions.
- **`crop.py, pso_vaas.py,  vaas_ffca.py, and random_vaas.py`**: Scripts of algorithms.
- **`composition/`**: contains the main scripts of our solution. 
- **`utils/`**: Contains reusable helper functions and modules.
- **`data/`**: Stores datasets generated for the experiments.
- **`results/`**: Includes results files including csv files.
- **`requirements.txt`**: Lists all Python dependencies needed for the project.
- **`README.md`**: This file contains documentation for the repository.


