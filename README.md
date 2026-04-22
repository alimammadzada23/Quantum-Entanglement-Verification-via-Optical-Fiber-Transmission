# Quantum-Entanglement-Verification-via-Optical-Fiber-Transmission

Independent re-analysis of photon-pair entanglement through NANF (Hollow-Core Fiber) and SMF-28 (Standard Single-Mode Fiber) using full quantum state tomography and three complementary entanglement metrics.

Overview
This repository contains a complete, independent quantum optics data analysis pipeline applied to the published dataset Zenodo: 8207772. Polarisation-entangled photon pairs are transmitted through two fibre types across a range of time-bin spacings Δt (ps). At each spacing the two-qubit density matrix is reconstructed via Maximum-Likelihood Estimation (MLE) from nine polarisation-basis coincidence measurements, then characterised by three independent entanglement metrics.

The central physical question is: how does entanglement survive — or degrade — as a function of time-bin delay in each fibre?

Repository Structure
text
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
Data source: Place 8207772.zip (containing submission_datacode_upload.zip) in the root directory before running any script. The raw zip is not included in this repository due to size; download it from Zenodo 8207772.

Physical Background
The Entangled State
The source produces polarisation-entangled photon pairs approximating the Bell state:

∣
Ψ
−
⟩
=
1
2
(
∣
H
V
⟩
−
∣
V
H
⟩
)
∣Ψ 
−
 ⟩= 
2
 
1
 (∣HV⟩−∣VH⟩)

This state is the singlet state of two spin-½ systems: the two photon polarisations are maximally anti-correlated in every measurement basis. It is one of the four maximally entangled Bell states and achieves the Tsirelson bound of the CHSH inequality.

Why Time-Bin Spacing Matters
The two photons are generated in time-bin pairs. When the time-bin spacing Δt is small, the photons arrive nearly simultaneously at the fibre input and experience correlated temporal mode-mismatch, dispersion, and birefringence — all of which degrade entanglement. At large Δt the photons are cleanly separated in time, and the state approaches source quality. The transition region encodes the fibre's entanglement-preservation capacity.

The Two Fibres
Property	NANF (HCF)	SMF-28
Type	Hollow-core nested anti-resonant nodeless fibre	Standard solid-core single-mode
Guiding mechanism	Anti-resonant reflection	Total internal reflection
Dispersion	Ultra-low (air core)	Standard chromatic dispersion
Birefringence	Very low	Low
Entanglement threshold Δt	~97 ps (M3)	~218 ps (M3)
The core finding is that NANF reaches high-entanglement operation at roughly half the time-bin spacing required by SMF-28, consistent with its lower dispersion.

Methods
Shared Infrastructure (all scripts)
MLE Density Matrix Reconstruction

Given coincidence counts 
n
k
n 
k
  for projectors 
{
Π
k
}
{Π 
k
 } across 9 bases (HH, HD, HR, DH, DD, DR, RH, RD, RR — 4 outcomes each = 36 values), the physical density matrix is recovered by minimising the negative log-likelihood:

L
(
ρ
)
=
−
∑
k
n
k
ln
⁡
T
r
(
ρ
Π
k
)
L(ρ)=−∑ 
k
 n 
k
 lnTr(ρΠ 
k
 )

subject to 
ρ
≥
0
ρ≥0, 
T
r
(
ρ
)
=
1
Tr(ρ)=1, 
ρ
=
ρ
†
ρ=ρ 
†
 . Physicality is enforced by the Cholesky parametrisation 
ρ
=
T
†
T
/
T
r
(
T
†
T
)
ρ=T 
†
 T/Tr(T 
†
 T) where T is lower-triangular (4 real diagonal + 6 complex off-diagonal = 16 free parameters). Optimisation uses L-BFGS-B (scipy). Up to 3 random restarts are attempted if the primary initialisation fails physicality checks.

Bootstrap Uncertainty

All metrics are bootstrapped with n = 200 multinomial resamples. For each resample, the full MLE → metric pipeline is repeated. Reported uncertainties are the standard deviation across valid bootstrap samples. The 2-sigma entanglement criterion (metric_mean − 2 × metric_std) > threshold is used consistently across all methods.

Method 1 — Bell Fidelity F(|Ψ⁻⟩) (method_12.py)
The fidelity with the target Bell state is computed from three two-qubit correlators:

F
(
∣
Ψ
−
⟩
)
=
1
4
(
1
−
E
X
X
−
E
Y
Y
−
E
Z
Z
)
F(∣Ψ 
−
 ⟩)= 
4
1
 (1−E 
XX
 −E 
YY
 −E 
ZZ
 )

where 
E
α
α
=
⟨
σ
α
⊗
σ
α
⟩
=
T
r
(
ρ
 
σ
α
⊗
σ
α
)
E 
αα
 =⟨σ 
α
 ⊗σ 
α
 ⟩=Tr(ρσ 
α
 ⊗σ 
α
 ) for 
α
∈
{
X
,
Y
,
Z
}
α∈{X,Y,Z}. These are read directly from the off-diagonal and diagonal structure of the reconstructed density matrix via the Pauli basis expansion. No MLE optimisation is required for this metric — it is a linear functional of ρ.

Threshold: F > 0.5 implies the state cannot be described by any separable mixture (entanglement witness condition).

Entanglement Witness: 
W
=
0.5
−
F
W=0.5−F. Negative W (i.e., W < 0) certifies entanglement.

Output columns: dt_ps, vpos, fiber, F_mean, F_std, W, W_std, entangled_2sig, E_ZZ, E_XX, E_YY

Method 3 — CHSH Nonlocality via Horodecki (1995) (method_3.py)
The maximum CHSH Bell parameter achievable for a given density matrix is computed analytically without searching over measurement angles. The Horodecki (1995) formula derives it from the correlation matrix T:

T
i
j
=
T
r
(
ρ
 
σ
i
⊗
σ
j
)
,
i
,
j
∈
{
x
,
y
,
z
}
T 
ij
 =Tr(ρσ 
i
 ⊗σ 
j
 ),i,j∈{x,y,z}

Let 
M
=
T
T
T
M=T 
T
 T and let 
m
1
≥
m
2
m 
1
 ≥m 
2
  be its two largest eigenvalues. Then:

S
max
⁡
=
2
m
1
+
m
2
S 
max
 =2 
m 
1
 +m 
2
 
 

Threshold: S_max > 2 violates the CHSH inequality, proving nonlocality (which implies entanglement). The Tsirelson bound 
S
=
2
2
≈
2.828
S=2 
2
 ≈2.828 is the quantum maximum, achieved only by maximally entangled Bell states.

This method gives the strongest logical claim (nonlocality → entanglement) but requires the highest signal-to-noise due to the strict threshold.

Output columns: dt_ps, vpos, fiber, S_mle, S_mean, S_std, significance_sigma, entangled_2sigma, purity, m1, m2

Method 4 — Concurrence C (Wootters 1998) (method_4.py)
Concurrence is a rigorous entanglement monotone — a quantity that is zero for separable states, one for maximally entangled states, and cannot be increased by local operations and classical communication (LOCC). It is computed via the Wootters (1998) formula:

Step 1 — Spin-flip:
ρ
~
=
(
σ
y
⊗
σ
y
)
 
ρ
∗
 
(
σ
y
⊗
σ
y
)
ρ
~
 =(σ 
y
 ⊗σ 
y
 )ρ 
∗
 (σ 
y
 ⊗σ 
y
 )

where 
ρ
∗
ρ 
∗
  is the complex conjugate in the computational basis 
{
∣
H
H
⟩
,
∣
H
V
⟩
,
∣
V
H
⟩
,
∣
V
V
⟩
}
{∣HH⟩,∣HV⟩,∣VH⟩,∣VV⟩}.

Step 2 — Auxiliary matrix:
R
=
ρ
  
ρ
~
  
ρ
R= 
ρ
  
ρ
~
  
ρ
 

where 
ρ
ρ
  is the matrix square root via eigendecomposition.

Step 3 — Concurrence:
C
(
ρ
)
=
max
⁡
(
0
,
  
λ
1
−
λ
2
−
λ
3
−
λ
4
)
C(ρ)=max(0,λ 
1
 −λ 
2
 −λ 
3
 −λ 
4
 )

where 
λ
1
≥
λ
2
≥
λ
3
≥
λ
4
≥
0
λ 
1
 ≥λ 
2
 ≥λ 
3
 ≥λ 
4
 ≥0 are the square roots of the eigenvalues of R.

Note on bias: The max(0, ...) clipping creates a positive bias in the concurrence estimator near C = 0. Bootstrap mean C may be slightly above zero for nearly-separable states. At low Δt (purity < 0.5), the CHSH result (Method 3) is the authoritative entanglement criterion; concurrence is reported as a supplementary metric.

Output columns: dt_ps, vpos, fiber, C_point, C_mean, C_std, entangled_2sigma, purity

Multi-Method Comparison (entanglement_comparison.py)
Merges all three CSVs on (dt_ps, fiber) using outer join, computes:

Threshold Δt — first time-bin spacing at which each method confirms entanglement (2σ criterion)

Plateau statistics — mean, std, max in the saturated high-Δt regime (data-driven: points within 95% of each method's maximum)

Recovery percentage — plateau value as a fraction of the source baseline

Disagreement analysis — points where M1, M3, M4 give different verdicts, with physical interpretation

Two publication figures — 6-panel overview and per-method plots with annotated threshold crossings

Key Results
Entanglement Threshold (First Confirmed, 2σ)
Fiber	M1 (F > 0.5)	M4 (C > 0)	M3 (S > 2)	M3/M1 ratio
NANF (HCF)	58.5 ps	58.5 ps	97.25 ps	1.66×
SMF-28	106.0 ps	106.0 ps	217.75 ps	2.05×
NANF reaches confirmed entanglement at roughly half the time-bin spacing of SMF-28 across all three methods, consistent with its lower chromatic dispersion.

Plateau Values (Saturated Regime)
Fiber	F (plateau)	S (plateau)	C (plateau)	Source
NANF (HCF)	~0.943	~2.650	~0.903	F=0.976, S=2.692, C=0.918
SMF-28	~0.946	~2.685	~0.938	same source
SMF-28 reaches slightly higher plateau values at large Δt — consistent with it having a cleaner temporal mode separation at long delays despite its higher dispersion.

Method Sensitivity Order
As expected from theory: M1 (Bell fidelity) ≈ M4 (Concurrence) > M3 (CHSH) in sensitivity. CHSH is the strictest criterion (requires nonlocality, not just entanglement) while Bell fidelity and concurrence detect entanglement at lower signal levels. This ordering holds consistently for both fibres.

Figures
entanglement_verification.png — 4-panel overview
Top row: authors' concurrence and purity (reproduced from paper Fig. 4a). Bottom row: our independent Bell fidelity and entanglement witness analysis. Direct visual comparison validates consistency of MLE reconstruction.

chsh_smax_horodecki.png — CHSH Bell parameter
S_max vs Δt for NANF and SMF-28. Horizontal lines: classical bound S = 2.0, Tsirelson bound S = 2√2, source baseline S ≈ 2.692.

concurrence_wootters.png — Wootters Concurrence
Concurrence C vs Δt. Source baseline C = 0.918. Both fibres show sigmoidal rise from C ≈ 0 to plateau near source value.

comparison_6panel.png — Full multi-method comparison
Six panels: S_max, C, F, Witness W, normalised overlay (visual diagnostic only — scales not physically equivalent), and threshold bar chart.

comparison_per_method.png — Annotated threshold crossings
One panel per method, with vertical dashed lines marking the first confirmed entanglement Δt for each fibre.

Installation
bash
pip install numpy scipy matplotlib pandas
Python ≥ 3.9 required. No quantum computing frameworks needed — all computations are pure linear algebra on the reconstructed density matrices.

Reproducibility
All scripts set np.random.seed(42) globally before the analysis loop. Bootstrap resamples use this global seed stream — each file receives a unique but deterministic segment of the pseudorandom sequence. Local resampling for MLE restarts uses np.random.default_rng(attempt * 7 + 13) and does not disturb the global state. Running any script twice on the same data produces bit-identical output.

Running the Analysis
Scripts must be run in order since each produces CSVs consumed by the next:

bash
# Step 1 — Bell Fidelity and Witness (Methods 1 & 2)
python method_12.py
# Outputs: fidelity_witness_results.csv, entanglement_verification.png

# Step 2 — CHSH Nonlocality (Method 3)
python method_3.py
# Outputs: chsh_horodecki_results.csv, chsh_smax_horodecki.png

# Step 3 — Concurrence (Method 4)
python method_4.py
# Outputs: concurrence_results.csv, concurrence_wootters.png

# Step 4 — Multi-method comparison
python entanglement_comparison.py
# Outputs: merged_comparison.csv, comparison_6panel.png, comparison_per_method.png
All scripts assume 8207772.zip is in the working directory.

CSV Column Reference
fidelity_witness_results.csv
Column	Description
dt_ps	Time-bin spacing in picoseconds
vpos	Voltage position (raw calibration index)
fiber	Fibre type: HCF (NANF) or SMF28
F_mean	Bootstrap mean Bell fidelity F(
F_std	Bootstrap std of F
W	Entanglement witness W = 0.5 − F (negative = entangled)
W_std	Bootstrap std of W
entangled_2sig	True if (F_mean − 2·F_std) > 0.5
E_ZZ, E_XX, E_YY	Two-qubit correlators ⟨σ_α⊗σ_α⟩
chsh_horodecki_results.csv
Column	Description
S_mle	S_max from point-estimate MLE density matrix
S_mean	Bootstrap mean S_max
S_std	Bootstrap std
significance_sigma	(S_mean − 2.0) / S_std — sigma above classical bound
entangled_2sigma	True if (S_mean − 2·S_std) > 2.0
purity	Tr(ρ²) from MLE density matrix
m1, m2	Two largest eigenvalues of T^T T (Horodecki matrix)
concurrence_results.csv
Column	Description
C_point	Concurrence from point-estimate MLE density matrix
C_mean	Bootstrap mean concurrence
C_std	Bootstrap std
entangled_2sigma	True if (C_mean − 2·C_std) > 0
purity	Tr(ρ²) from MLE density matrix
Theoretical References
Wootters (1998) — W.K. Wootters, "Entanglement of Formation of an Arbitrary State of Two Qubits," Phys. Rev. Lett. 80, 2245. Defines concurrence as an entanglement monotone for two-qubit systems.

Horodecki et al. (1995) — M. Horodecki, P. Horodecki, R. Horodecki, "Violating Bell inequality by mixed spin-½ states: necessary and sufficient condition," Phys. Lett. A 200, 340. Derives S_max analytically from the correlation tensor T.

James et al. (2001) — D.F.V. James et al., "Measurement of qubits," Phys. Rev. A 64, 052312. Standard reference for MLE quantum state tomography of two-qubit polarisation states.

Werner (1989) — R.F. Werner, "Quantum states with Einstein-Podolsky-Rosen correlations admitting a hidden-variable model," Phys. Rev. A 40, 4277. Defines the Werner state model used for source baseline S inference.

Bell (1964) — J.S. Bell, "On the Einstein-Podolsky-Rosen paradox," Physics 1, 195. Original derivation of the Bell inequality violated by entangled quantum states.

Notes on Interpretation
Why do M1 and M4 detect entanglement earlier than M3?
Bell fidelity and concurrence are entanglement witnesses/monotones — they detect any entanglement, including weakly entangled states far from a Bell state. CHSH nonlocality is a strictly stronger property: every nonlocal state is entangled, but not every entangled state is nonlocal (especially mixed states). At low Δt the states are deeply mixed (purity ≈ 0.37–0.40), placing them in the regime where entanglement exists but CHSH violation is suppressed below the detection threshold.

Why does SMF-28 reach a higher plateau than NANF at large Δt?
At large time-bin spacings both fibres transmit the photons with clean temporal separation, so the entanglement quality approaches the source limit. SMF-28 photons may experience less polarisation mode coupling in this regime due to geometry, or the specific dataset may have longer SMF-28 scans extending into a cleaner saturation region.

Concurrence upward bias near C = 0
The max(0, ...) in the Wootters formula creates a positivity constraint that biases C upward for near-separable states. At Δt = 39.75 ps (HCF), C = 0.028 ± 0.009 passes the 2σ criterion but S = 1.33 (−36σ below classical) unambiguously fails. In the low-Δt, low-purity regime, the CHSH result is authoritative and concurrence should be interpreted with caution.

Licence
MIT. Data from Zenodo 8207772 is subject to its original Creative Commons licence.
