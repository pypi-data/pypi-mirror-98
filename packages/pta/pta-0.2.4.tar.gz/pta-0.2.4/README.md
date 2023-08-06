# Probabilistic Thermodynamic Analysis of Metabolic Networks
[![Join the chat at https://gitter.im/CSB-ETHZ/PTA](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/CSB-ETHZ/PTA?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Documentation Status](https://readthedocs.org/projects/probabilistic-thermodynamic-analysis/badge/?version=latest)](https://probabilistic-thermodynamic-analysis.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/pta.svg)](https://badge.fury.io/py/pta)

Probabilistic Thermodynamic Analysis (PTA) is a framework for the exploration of
the thermodynaic properties of a metabolic network. In PTA, we consider the 
*thermodynamic space* of a network, that is, the space of standard reaction 
energies and metabolite concentrations that are compatible with steady state
flux constraints. The uncertainty of the variables in the thermodynamic space is 
modeled with a probability distribution, allowing analysis with optimization and
sampling approaches:
- **Probabilistic Metabolic Optimization (PMO)** aims at finding the most probable 
values of reaction energies and metabolite concentrations that are compatible 
with the steady state constrain. This method is particularly useful to indentify
features of the network that are thermodynamically unrealistic. For example, PMO
can identify substrate channeling, incorrect cofactors or inaccurate 
directionalities.
- **Thermodynamic and Flux Sampling (TFS)** allows to jointly sample the 
thermodynamic and flux spaces of a network. The method provides estimates of 
metabolite concentrations, reactions directions, and flux distributions.

## Installation

We provide interfaces to run PTA for both Python (preferred) and MATLAB.
- **Python**: PTA is available on the [Python Package
  Index](https://pypi.org/project/pta/), see the
  [documentation](https://probabilistic-thermodynamic-analysis.readthedocs.io/en/latest/getting_started.html)
  for the installation instructions.
- **MATLAB**: See the [instructions](MATLAB/README.md) for installing the MATLAB
  interface.

## Reproducing the examples in the PTA publication [[1](#references)]

We generated our results using the MATLAB interface. While we do not expect current
development to affect  the results obtained with PTA, the safest way to reproduce our
analysis is to check out the code at the last commit we used: [8f28b6aa](https://gitlab.com/csb.ethz/pta/-/tree/8f28b6aabaad2951ae96edc29d6a8d384b58ff43).

## Cite us

If you use PTA in a scientific publication, please cite our paper: 

Gollub, M.G., Kaltenbach, H.M., Stelling, J., 2020. "Probabilistic Thermodynamic 
Analysis of Metabolic Networks". *biorXiv*. - 
[pdf](https://www.biorxiv.org/content/10.1101/2020.08.14.250845v1.full.pdf)

## References

1. Gollub, M.G., Kaltenbach, H.M., Stelling, J., 2020. "Probabilistic Thermodynamic 
Analysis of Metabolic Networks". *biorXiv*.
2. Gerosa, L., van Rijsewijk, B.R.H., Christodoulou, D., Kochanowski, K., Schmidt, T.S., Noor, E. and Sauer, U., 2015. Pseudo-transition analysis identifies the key regulators of dynamic metabolic adaptations from steady-state data. *Cell systems*, 1(4), pp.270-282.
