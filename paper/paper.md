---
title: 'matscipy: Materials science with Python at the atomic-scale'
tags:
  - Python
  - Material Science
  - Atomistic simulations
authors:
  - name: Petr Grigorev
    orcid: 0000-0002-6409-9092
    #equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    corresponding: true # (This is how to denote the corresponding author)
    affiliation: "1" # (Multiple affiliations must be quoted)
  - name: James R. Kermode
    orcid: 0000-0001-6755-6271
    #equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 2
  - name: Lars Pastewka
    orcid: 0000-0001-8351-7336
    #equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 3
affiliations:
  - name: Aix-Marseille Universit ́e, CNRS, CINaM UMR 7325, Campus de Luminy, 13288 Marseille, France
    index: 1
  - name: Warwick Centre for Predictive Modelling, School of Engineering, University of Warwick, Coventry CV4 7AL, United Kingdom
    index: 2
  - name: Department of Microsystems Engineering, University of Freiburg, 79110 Freiburg, Germany
    index: 3
date: 14 October 2022
bibliography: paper.bib
---

# Summary

Behaviour of materials is governed by physical phenomena happening at an extreme range of length and time scales. Thus, computational modelling requires a multiscale approach. Simulation techniques operating on the atomic scale serve as a foundation for such an approach, providing necessary parameters for upper scale models. The physical model employed for an atomic simulation can vary from electronic structure calculations to empirical force fields, however, the set of tools for construction, manipulation and analysis of the system stays the same for a given application. Here we present a collection of such tools for applications including fracture mechanics, plasticity, contact mechanics and electrochemistry. 

# Statement of need

The python package `matscipy` contains a set of tools for researchers in a field of materials science and atomistic modelling. It is built around Atomic Simulation Environment (ASE) [@Larsen2017] that offers great flexibility and interoperability by providing a python interface to tens of simulation codes implementing different physical models. Below, we give a short summary for every application domain:

- Plasticity. Dislocations are extended defects in the material and are the main carriers of plasticity. `matscipy` module `dislocation.py` focuses on tools for studying structure and movement of dislocations. Construction and analysis of model atomic systems is implemented for compact and dissociated screw, as well as edge dislocations in cubic crystals. The implementation also includes large scale systems for single and double kinks. The module was employed in a study of interaction of hydrogen with screw dislocation in tungsten [@Grigorev2020].

- Fracture mechanics
- Contact mechanics
- Electrochemistry


# Acknowledgements

# References