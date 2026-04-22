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

### Method 1 — Bell Fidelity F(|Ψ⁻⟩)   `method_1,2.py`

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

where `λ1 ≥ λ2 ≥ λ3 ≥ λ4 ≥ 0` are the square roots of the eigenvalues of R.

> **Bias note:** The `max(0, ...)` clipping creates a small upward bias near C = 0.
> At low Δt (purity < 0.5), the CHSH result (Method 3) is authoritative; concurrence
> is reported as a supplementary metric in this regime.

**Output columns:**
`dt_ps`, `vpos`, `fiber`, `C_point`, `C_mean`, `C_std`, `entangled_2sigma`, `purity`

---

### Multi-Method Comparison   `entanglement_comparison.py`

Merges all three CSVs on `(dt_ps, fiber)` via outer join, then computes:

- **Threshold Δt** — first spacing at which each method confirms entanglement (2σ)
- **Plateau statistics** — mean/std/max for points within 95% of each method's maximum
- **Recovery %** — plateau value as fraction of source baseline
- **Disagreement analysis** — points where M1, M3, M4 give different verdicts
- **Two publication figures** — 6-panel overview and annotated per-method plots


---

## Key Results

### Entanglement Detection Threshold (2σ criterion)

| Fiber       | M1  F > 0.5 | M4  C > 0  | M3  S > 2.0 | M3 / M1 ratio |
|-------------|-------------|------------|-------------|---------------|
| NANF (HCF)  | 58.5 ps     | 58.5 ps    | 97.25 ps    | 1.66×         |
| SMF-28      | 106.0 ps    | 106.0 ps   | 217.75 ps   | 2.05×         |

NANF confirms entanglement at ~half the Δt of SMF-28 across all methods.

### Plateau Values (Saturated Large-Δt Regime)

| Fiber      | F (plateau) | S (plateau) | C (plateau) | Source values             |
|------------|-------------|-------------|-------------|---------------------------|
| NANF (HCF) | ~0.943      | ~2.650      | ~0.903      | F=0.976, S=2.692, C=0.918 |
| SMF-28     | ~0.946      | ~2.685      | ~0.938      | same source               |

### Method Sensitivity Ordering



CHSH requires nonlocality (strictly stronger than entanglement). Bell fidelity and
concurrence detect entanglement at lower signal levels, especially in the mixed-state
regime at low Δt.

---

## Installation

```bash
pip install numpy scipy matplotlib pandas
```

Python ≥ 3.9. No quantum computing frameworks needed — all computations are pure
linear algebra on reconstructed density matrices.

---

## Running the Analysis

Run scripts in order — each produces CSVs consumed by the next:

```bash
python method_1,2.py            # → fidelity_witness_results.csv
python method_3.py             # → chsh_horodecki_results.csv
python method_4.py             # → concurrence_results.csv
python entanglement_comparison.py   # → merged_comparison.csv + all figures
```

All scripts assume `8207772.zip` is in the working directory.

---

## Reproducibility

All scripts call `np.random.seed(42)` once before the analysis loop. Bootstrap
resamples use this global seed stream — each data file receives a unique but
deterministic segment of the pseudorandom sequence. MLE restarts use
`np.random.default_rng(attempt * 7 + 13)` without disturbing the global state.
Running any script twice on the same data produces bit-identical output.

---

## References

- Wootters (1998) — *Phys. Rev. Lett.* **80**, 2245 — Concurrence as entanglement monotone
- Horodecki, Horodecki, Horodecki (1995) — *Phys. Lett. A* **200**, 340 — Analytical S_max
- James et al. (2001) — *Phys. Rev. A* **64**, 052312 — MLE quantum state tomography
- Werner (1989) — *Phys. Rev. A* **40**, 4277 — Werner state model
- Bell (1964) — *Physics* **1**, 195 — Bell inequality

---

## Licence

MIT. Dataset from Zenodo 8207772 is subject to its original Creative Commons licence.

