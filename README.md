# Reproducible-Research-project-2026

# Reproducible Research Project 2026

## Project Description

This project reproduces selected results from:

**Nowak, M. A., & Krakauer, D. C. (1999). The Evolution of Language.**

The implementation consists of three simulation modules:

* Protolanguage Simulation
* Adaptive Dynamics Simulation
* Word Formation Simulation

The simulations generate figures illustrating the emergence and evolution of linguistic structures.

---

## Repository Approximate Structure

```text
.
├── src/
│   ├── main.py
│   ├── protolang_simulation.py
│   ├── adaptive_dynamics_simulation.py
│   ├── word_formation_simulation.py
│   └── utils.py
│
├── notebook/
│   └── report.ipynb
│
├── output/
│   └── generated figures and report
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Running the Project Using Docker

### Pull the Docker Image

```bash
docker pull timchen22/repro-project:latest
```

### Run the Container

```bash
docker run --rm \
  -v "$(pwd)/output:/app/output" \
  timchen22/repro-project:latest
```

The container executes the simulation pipeline and generates all figures used in the report.

---

## Generated Outputs

The project produces:

* Protolanguage fitness and coherence plots
* Emergence of protolanguage visualization
* Evolutionary language game optimization plots
* Optimized language profile plots
* Word formation simulation plots

These outputs are stored in the `output/` directory.

---

## Report

The repository contains a Quarto/Jupyter report summarizing the simulations and results.

The report serves as the basis for the project presentation and explains the methodology and generated figures.

---

## Reproducibility

The project is fully containerized using Docker.

The Docker image contains:

* Python 3.11
* Required Python dependencies
* Quarto
* Source code and report materials

Running the Docker container reproduces the simulation results without requiring any local installation of Python packages.

---

## Authors

Viktor Senkiv, Zeping Chen, Zihua Lai

Reproducible Research Project 2026
