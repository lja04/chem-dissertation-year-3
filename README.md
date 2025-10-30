# Year 3 Internship Project: Evaluating Phonon Contributions to Crystal Structure Prediction

This repository contains the code, scripts, and analysis tools developed during my Year 3 internship project focused on improving crystal structure ranking accuracy in large-scale Computational Crystal Structure Prediction (CSP) by including vibrational free energy contributions computed using harmonic phonon models.

## Project Overview

- **Background:** CSP predicts stable and metastable molecular crystal structures by exploring potential energy landscapes. Traditional methods rank predicted structures by static lattice energy, ignoring temperature-dependent vibrational effects which can significantly influence polymorph stability rankings, especially for closely ranked structures.
- **Objective:** To evaluate whether incorporating vibrational free energy corrections from harmonic phonon calculations at the force-field level improves polymorph ranking accuracy in CSP workflows, offering a balance between computational cost and accuracy.
- **Approach:** 
  - Selection of a representative subset of molecular crystal structures from a large CSP dataset using farthest point sampling on molecular fingerprints.
  - Preparation of structures for phonon calculations including trial structure formatting and supercell generation.
  - Harmonic phonon calculations combined with Debye approximations and kernel density estimation (KDE) to compute vibrational free energies.
  - Evaluation of vibrational free energy convergence with respect to k-point spacing to determine an optimal sampling strategy balancing accuracy and computational efficiency.
  - Re-ranking of crystal structures incorporating vibrational contributions and comparison with static lattice energy rankings.
  - Statistical and structural analysis to understand effects of vibrational corrections on ranking stability.

## Key Findings

- Vibrational free energy corrections led to significant reordering of some crystal structures’ predicted stabilities, confirming that vibrational effects, while often small, are essential for accurate polymorph ranking.
- An optimal k-point spacing value of 0.30 was identified to balance computational cost and vibrational free energy convergence, with some exceptions benefiting from finer k-point sampling.
- Vibrational contributions were not correlated with crystal density alone, suggesting that other structural factors influence phonon effects.
- This work supports integrating low-cost phonon-based vibrational corrections into CSP workflows to improve prediction reliability.

## Technologies and Tools

- Python 3.9 with libraries: NumPy, SciPy, Pandas, Matplotlib, RDKit
- DMACRYS software for force-field based lattice energy minimisation and phonon calculations
- NEIGHCRYS for automated DMACRYS input preparation
- Custom Python scripts for:
  - Molecular fingerprinting and structure selection (farthest point sampling)
  - Supercell generation and finite displacement phonon calculations (AutoLD)
  - Phonon data processing and vibrational free energy calculations (AutoFree)
  - Data analysis and visualization

## Usage

Scripts and notebooks in this repository facilitate the preparation of CSP datasets for phonon calculations, automate vibrational analysis, and perform structure re-ranking based on vibrational free energy corrections. Follow the documented methodology to carry out convergence testing, calculate vibrational free energies, and analyze ranking effects on polymorph stability.

---
