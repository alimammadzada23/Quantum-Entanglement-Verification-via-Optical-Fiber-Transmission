# Quantum Entanglement Verification via Optical Fiber Transmission

Independent re-analysis of polarisation-entangled photon-pair transmission through
NANF (Hollow-Core Fiber) and SMF-28 (Standard Single-Mode Fiber) using full quantum
state tomography and three complementary entanglement metrics.

---

## Overview

This repository applies a complete quantum optics analysis pipeline to the published
dataset [Zenodo 8207772](https://zenodo.org/record/8207772). Polarisation-entangled
photon pairs are transmitted through two fibre types across a range of time-bin
spacings Δt (ps). At each spacing, the two-qubit density matrix ρ is reconstructed
via Maximum-Likelihood Estimation (MLE) from nine polarisation-basis coincidence
measurements, then characterised by three independent entanglement metrics.

**Central question:** How does entanglement survive — or degrade — as a function of
time-bin delay in each fibre?

---

## Repository Structure



> **Data:** Place `8207772.zip` (containing `submission_datacode_upload.zip`) in the
> root directory before running any script. Download from
> [Zenodo 8207772](https://zenodo.org/record/8207772).

---

## Physical Background

### The Entangled State

The source produces photon pairs approximating the Bell singlet state:



The two photon polarisations are maximally anti-correlated in every measurement basis.
This state achieves the Tsirelson quantum bound of the CHSH inequality.

### Why Time-Bin Spacing Δt Matters

At small Δt the photons arrive nearly simultaneously at the fibre input and experience
correlated temporal mode-mismatch, dispersion, and birefringence — all of which degrade
entanglement. At large Δt the photons are cleanly separated and the state approaches
source quality. The transition region encodes the fibre's entanglement-preservation
capacity.

### The Two Fibres

| Property              | NANF (HCF)                          | SMF-28                        |
|-----------------------|-------------------------------------|-------------------------------|
| Type                  | Hollow-core nested anti-resonant    | Standard solid-core           |
| Guiding mechanism     | Anti-resonant reflection            | Total internal reflection     |
| Dispersion            | Ultra-low (air core)                | Standard chromatic            |
| Entanglement threshold (M3) | ~97 ps                        | ~218 ps                       |

NANF reaches confirmed entanglement at roughly half the time-bin spacing of SMF-28,
consistent with its lower chromatic dispersion.

---

## Methods

### Shared Infrastructure — MLE Density Matrix Reconstruction

Given coincidence counts `n_k` for projectors across 9 bases (HH, HD, HR, DH, DD, DR,
RH, RD, RR — 4 outcomes each = 36 values), the physical density matrix is recovered by
minimising the negative log-likelihood:

Physicality is enforced by the **Cholesky parametrisation**:


where T is a lower-triangular 4×4 complex matrix (4 real diagonal + 6 complex
off-diagonal = 16 free parameters). This guarantees ρ is Hermitian, positive
semidefinite, and unit trace by construction. Optimisation uses L-BFGS-B (scipy).
Up to 3 random restarts are attempted if the primary initialisation fails.

### Bootstrap Uncertainty

All metrics use n = 200 multinomial bootstrap resamples. For each resample, the full
MLE → metric pipeline is repeated. The **2-sigma entanglement criterion** is used
consistently:

---

### Method 1 — Bell Fidelity F(|Ψ⁻⟩)   `method_12.py`

Fidelity with the Bell state is computed from three two-qubit correlators:

These are linear functionals of ρ — no additional optimisation is needed.

- **Threshold:** F > 0.5 → state cannot be separable (entanglement witness condition)
- **Witness:** W = 0.5 − F  →  W < 0 certifies entanglement

**Output columns:**
`dt_ps`, `vpos`, `fiber`, `F_mean`, `F_std`, `W`, `W_std`, `entangled_2sig`,
`E_ZZ`, `E_XX`, `E_YY`

---

### Method 3 — CHSH Nonlocality via Horodecki (1995)   `method_3.py`

The maximum achievable CHSH Bell parameter is computed analytically from the
**correlation matrix** T, without searching over measurement angles:

where `m1 ≥ m2` are the two largest eigenvalues of M.

- **Threshold:** S_max > 2.0 violates the CHSH inequality → proves nonlocality → entanglement
- **Tsirelson bound:** S = 2√2 ≈ 2.828 (quantum maximum, perfect Bell state only)
- **Source baseline:** S ≈ 2.692 (inferred via Werner model from F_src = 0.9759)

**Output columns:**
`dt_ps`, `vpos`, `fiber`, `S_mle`, `S_mean`, `S_std`, `significance_sigma`,
`entangled_2sigma`, `purity`, `m1`, `m2`

---

### Method 4 — Concurrence C (Wootters 1998)   `method_4.py`

Concurrence is a rigorous entanglement monotone (C = 0: separable, C = 1: maximal).
The Wootters formula proceeds in three steps:

**Step 1 — Spin-flip state:**

where `ρ*` is the complex conjugate in the {|HH⟩, |HV⟩, |VH⟩, |VV⟩} basis.

**Step 2 — Auxiliary matrix:**

where `sqrt(ρ)` is the matrix square root via eigendecomposition:
`sqrt(ρ) = V · diag(sqrt(λ_i)) · V†`

**Step 3 — Concurrence:**
