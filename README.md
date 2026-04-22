# Quantum Entanglement Verification via Optical Fiber Transmission

Independent re-analysis of photon-pair entanglement through NANF (Hollow-Core Fiber) and SMF-28 (Standard Single-Mode Fiber) using full quantum state tomography and three complementary entanglement metrics.

## Overview

This repository contains a complete, independent quantum optics data analysis pipeline applied to the published dataset **Zenodo: 8207772**. Polarisation-entangled photon pairs are transmitted through two fibre types across a range of time-bin spacings $\Delta t$ (ps). At each spacing, the two-qubit density matrix is reconstructed via Maximum-Likelihood Estimation (MLE) from nine polarisation-basis coincidence measurements, then characterised by three independent entanglement metrics.

The central physical question is: **how does entanglement survive — or degrade — as a function of time-bin delay in each fibre?**

### Repository Structure

```text
.
├── method_12.py                   # Method 1 & 2 — Bell Fidelity F(|Ψ⁻⟩) & Entanglement Witness W
├── method_3.py                    # Method 3 — CHSH S_max via Horodecki (1995)
├── method_4.py                    # Method 4 — Concurrence C (Wootters 1998)
├── entanglement_comparison.py     # Multi-method merger, statistics & 6-panel figure
│
├── results/
│   ├── fidelity_witness_results.csv       # M1/M2 output: F, W, E_ZZ, E_XX, E_YY per dt
│   ├── chsh_horodecki_results.csv         # M3 output: S_mean, S_std, significance per dt
│   ├── concurrence_results.csv            # M4 output: C_point, C_mean, C_std per dt
│   └── merged_comparison.csv              # All three methods joined on (dt_ps, fiber)
│
└── figures/
    ├── entanglement_verification.png      # 4-panel: authors' C & purity + our F & W
    ├── chsh_smax_horodecki.png            # CHSH S_max vs dt, both fibres
    ├── concurrence_wootters.png           # Concurrence C vs dt, both fibres
    ├── comparison_6panel.png              # 6-panel multi-method comparison
    └── comparison_per_method.png          # Per-method plots with threshold annotations
