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
