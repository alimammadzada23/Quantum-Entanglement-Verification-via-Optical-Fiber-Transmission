\subsection{Analytical Extension to Bipartite Systems}

Having established the capacity-ergotropy equivalence for a single qubit, we now extend the formalism to a bipartite quantum battery ($N=2$) to investigate the role of correlations. We explicitly solve the thermodynamic equations of motion for two identical non-interacting qubits, deriving the precise spectral conditions required for thermodynamic reversibility.

We define the system as a quantum battery composed of two identical non-interacting qubits. Following the interaction-free framework established in Ref.~[Paper 2], the global Hamiltonian is defined as the tensor sum of the local Hamiltonians:
\begin{equation}
    \hat{H} = \hat{H}_A \otimes \mathbb{I}_B + \mathbb{I}_A \otimes \hat{H}_B.
    \label{eq:global_hamiltonian}
\end{equation}
Substituting the local projector $\hat{H}_k = \omega |1\rangle\langle 1|_k$, we obtain the explicit global form:
\begin{equation}
    \hat{H} = (\omega |1\rangle\langle 1|_A \otimes \mathbb{I}_B) + (\mathbb{I}_A \otimes \omega |1\rangle\langle 1|_B).
    \label{eq:explicit_global_hamiltonian}
\end{equation}
This diagonal Hamiltonian generates a four-level energy spectrum characterized by a degenerate intermediate subspace. The eigenenergies are strictly defined as $E_0=0$ (ground state $|00\rangle$), $E_1=E_2=\omega$ (intermediate states $|01\rangle, |10\rangle$), and $E_3=2\omega$ (excited state $|11\rangle$).

Let the eigenvalues of the system density matrix $\hat{\rho}$ be denoted by $\lambda_j$ and ordered ascendingly such that $\lambda_0 \le \lambda_1 \le \lambda_2 \le \lambda_3$. The thermodynamic bounds are determined by the alignment of these populations with the energy levels derived above.

The Passive Energy ($\mathcal{U}^\downarrow$) corresponds to the minimal work configuration, where the largest populations occupy the lowest energy states:
\begin{equation}
    \mathcal{U}^\downarrow(\hat{\rho}) = E_0\lambda_3 + E_1\lambda_2 + E_2\lambda_1 + E_3\lambda_0.
\end{equation}
Substituting the eigenenergies yields:
\begin{equation}
    \mathcal{U}^\downarrow(\hat{\rho}) = 0 \cdot \lambda_3 + \omega \cdot \lambda_2 + \omega \cdot \lambda_1 + 2\omega \cdot \lambda_0 = \omega(\lambda_1 + \lambda_2 + 2\lambda_0).
    \label{eq:passive_energy_bipartite}
\end{equation}
Conversely, the Active Energy ($\mathcal{U}^\uparrow$) corresponds to the maximal work configuration, assigning the largest populations to the highest energy levels:
\begin{equation}
    \mathcal{U}^\uparrow(\hat{\rho}) = 2\omega \cdot \lambda_3 + \omega \cdot \lambda_2 + \omega \cdot \lambda_1 + 0 \cdot \lambda_0 = \omega(2\lambda_3 + \lambda_1 + \lambda_2).
    \label{eq:active_energy_bipartite}
\end{equation}
Summing these extremal energies reveals a generalized spectral symmetry. Grouping terms by $\omega$ and applying the trace condition $\sum \lambda_i = 1$, we obtain the fundamental conservation law for the bipartite spectrum:
\begin{equation}
    \mathcal{U}^\uparrow + \mathcal{U}^\downarrow = \omega(2\lambda_3 + 2\lambda_2 + 2\lambda_1 + 2\lambda_0) = 2\omega\left(\sum \lambda_i\right) = 2\omega.
    \label{eq:spectral_symmetry}
\end{equation}

We now derive the direct algebraic link between the battery capacity and the extractable work. Recall the definition of capacity $C = \mathcal{U}^\uparrow - \mathcal{U}^\downarrow$. Substituting the symmetry relation $\mathcal{U}^\uparrow = 2\omega - \mathcal{U}^\downarrow$ into this definition gives:
\begin{equation}
    C = (2\omega - \mathcal{U}^\downarrow) - \mathcal{U}^\downarrow = 2\omega - 2\mathcal{U}^\downarrow.
\end{equation}
Solving for the passive energy yields $\mathcal{U}^\downarrow = \omega - \frac{1}{2}C$. We insert this result into the definition of ergotropy, $R(\hat{\rho}) = \mathcal{U}(\hat{\rho}) - \mathcal{U}^\downarrow(\hat{\rho})$, to obtain the exact constitutive relation:
\begin{equation}
    R(\hat{\rho}) = \mathcal{U}(\hat{\rho}) + \frac{1}{2} C(\hat{\rho}) - \omega.
    \label{eq:constitutive_relation_bipartite}
\end{equation}
We now apply the TWM protocol constraints. The protocol requires the net energy shift to be null ($\Delta \mathcal{U}_{\text{total}} = 0$). Since the energy gap $\omega$ is constant, the variation of Eq.~(\ref{eq:constitutive_relation_bipartite}) simplifies to:
\begin{equation}
    \Delta R_{\text{total}} = \Delta \mathcal{U}_{\text{total}} + \frac{1}{2}\Delta C_{\text{total}} \implies \Delta R_{\text{total}} = \frac{1}{2} \Delta C_{\text{total}}.
    \label{eq:reversibility_condition}
\end{equation}
This result mathematically proves that for the bipartite system, the condition for thermodynamic reversibility ($\Delta R = 0$) is strictly equivalent to the condition of zero net capacity shift.

For the specific Hamiltonian derived in Eq.~(\ref{eq:explicit_global_hamiltonian}), the capacity formula simplifies significantly. Substituting the full spectral expressions (Eqs.~\ref{eq:passive_energy_bipartite} and \ref{eq:active_energy_bipartite}) into the definition of capacity:
\begin{equation}
    C(\hat{\rho}) = [\omega(2\lambda_3 + \lambda_2 + \lambda_1)] - [\omega(\lambda_1 + \lambda_2 + 2\lambda_0)].
\end{equation}
The intermediate terms $\omega\lambda_1$ and $\omega\lambda_2$ appear in both the active and passive components and therefore cancel out:
\begin{equation}
    C(\hat{\rho}) = 2\omega\lambda_3 - 2\omega\lambda_0 = 2\omega(\lambda_{\max} - \lambda_{\min}).
    \label{eq:eigenvalue_spread}
\end{equation}
This derivation confirms that for a two-qubit battery, the capacity is strictly a measure of the global eigenvalue spread. Consequently, the full analytical condition for ergotropy protection ($\Delta C_{\text{total}} = 0$) is explicitly given by the expansion:
\begin{equation}
    (\lambda_{\max}^{(m)} - \lambda_{\min}^{(m)} - \lambda_{\max}^{(0)} + \lambda_{\min}^{(0)}) + (\lambda_{\max}^{(\text{fin})} - \lambda_{\min}^{(\text{fin})} - \lambda_{\max}^{(\tau)} + \lambda_{\min}^{(\tau)}) = 0.
    \label{eq:spread_protection_condition}
\end{equation}
Equation (\ref{eq:spread_protection_condition}) confirms that the protocol protects extractable work if and only if the net change in the spread of the eigenvalues over the full cycle is zero.

Finally, we derive the analytical solvability condition for the reversal strength $w$. The protocol must satisfy two simultaneous boundary conditions: the final energy must match the initial energy (to satisfy $\Delta \mathcal{U}=0$), and the final capacity is determined by the ergotropy constraint derived above.

Let $\mathcal{U}_{\text{fin}}$ and $C_{\text{fin}}$ be the required target values fixed by the history of the protocol:
\begin{align}
    \mathcal{U}_{\text{fin}} &= \mathcal{U}(\hat{\rho}_{\tau}) - [\mathcal{U}(\hat{\rho}_m) - \mathcal{U}(\hat{\rho}_0)], \label{eq:target_energy} \\
    C_{\text{fin}} &= C(\hat{\rho}_{\tau}) - [C(\hat{\rho}_m) - C(\hat{\rho}_0)]. \label{eq:target_capacity}
\end{align}
We apply the reversal operator $\hat{W}_w$ to the decayed state $\hat{\rho}_\tau$. This generates an unnormalized density matrix $\hat{\tilde{\rho}}(w)$:
\begin{equation}
    \hat{\tilde{\rho}}(w) = (\hat{W}_w \otimes \hat{W}_w)\hat{\rho}_\tau (\hat{W}_w \otimes \hat{W}_w)^\dagger.
\end{equation}
The physical normalization factor $\mathcal{N}(w) = \text{Tr}[\hat{\tilde{\rho}}(w)]$ is strictly constrained by the energy requirement:
\begin{equation}
    \mathcal{N}(w) = \frac{\text{Tr}[\hat{\tilde{\rho}}(w)\hat{H}]}{\mathcal{U}_{\text{fin}}}.
\end{equation}
Substituting this constrained normalization into the capacity formula (Eq.~\ref{eq:eigenvalue_spread}) yields the final joint equation for the control parameter:
\begin{equation}
    \frac{2\omega \cdot \mathcal{U}_{\text{fin}} \cdot [\tilde{\lambda}_{\max}(w) - \tilde{\lambda}_{\min}(w)]}{\text{Tr}[\hat{\tilde{\rho}}(w)\hat{H}]} = C_{\text{fin}}.
\end{equation}
Expanding the target terms, we obtain the fully explicit condition:
\begin{equation}
    \frac{2\omega [\mathcal{U}_\tau - (\mathcal{U}_m - \mathcal{U}_0)] [\tilde{\lambda}_{\max}(w) - \tilde{\lambda}_{\min}(w)]}{\text{Tr}[\hat{\tilde{\rho}}(w)\hat{H}]} = C_\tau - (C_m - C_0).
    \label{eq:joint_solution}
\end{equation}
Equation (\ref{eq:joint_solution}) constitutes the rigorous analytical solution to the control problem. It allows for the determination of the unique physical root $w$ that satisfies both thermodynamic laws simultaneously, ensuring that the protocol operates strictly within the bounds of heat rectification.

\subsection{Numerical Analysis: Bipartite Entanglement Protection}

We now extend the numerical investigation to the two-qubit scenario to determine if the protocol can protect non-local quantum resources. The system is initialized in a specific class of X-states $\hat{\rho}_X(q)$, parameterized by the control variable $q \in [0, 1]$. In the computational basis $\{|gg\rangle, |ge\rangle, |eg\rangle, |ee\rangle\}$, the density matrix takes the form:
\begin{equation}
    \hat{\rho}_X(q) = 
    \begin{pmatrix}
        \frac{q}{2} & 0 & 0 & q^2 - \frac{q}{2} \\
        0 & q(1 - q) & 0 & 0 \\
        0 & 0 & (1 - q)^2 & 0 \\
        q^2 - \frac{q}{2} & 0 & 0 & \frac{q}{2}
    \end{pmatrix}. 
    
\end{equation}
This parameterization is physically significant because it allows us to continuously scan the Hilbert space from a separable product state at $q=0$ (where the system is in $|eg\rangle\langle eg|$) to a maximally entangled Bell state at $q=1$ (where the system approaches $|\Phi^+\rangle = \frac{|gg\rangle + |ee\rangle}{\sqrt{2}}$). By varying $q$, we can systematically test the protocol's efficacy across the entire spectrum of initial correlations.

\subsubsection{Initial State and Measurement Dynamics}

The protocol begins with the application of the global measurement operator. In this bipartite extension, the operator acts locally on each subsystem: $\hat{\mathbf{M}}_m = \hat{M}_m^{(A)} \otimes \hat{M}_m^{(B)}$. This factorization is physically significant: because the measurement is a Local Operation (LO), it is strictly forbidden from creating entanglement between previously uncorrelated subsystems.

Figure~4 presents the thermodynamic shifts induced immediately after this first measurement step.

\paragraph{Work Extraction Penalty (Panels a \& b):} Similar to the single-qubit case, the Ergotropy shift $\Delta \mathcal{R}$ (Panel a) and Antiergotropy shift $\Delta \mathcal{A}$ (Panel b) are universally non-positive. The measurement projects the joint population toward the ground state $|00\rangle$, resulting in an instantaneous loss of total stored energy.

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\linewidth]{MAIN/wmtq1.png}
    \caption{Thermodynamic quantities and shifts under the TWM protocol.}
    \label{fig:results}
\end{figure}

The response of the Capacity Gap $\Delta \mathcal{C}_{\text{gap}}$, shown in Panel (c), stands in distinct contrast to the single-qubit metrics. Unlike the local capacity, which admits positive shifts, the Capacity Gap exhibits a universally non-positive response (ranging from white to deep blue). The substantial negative shifts (blue gradients) confirm that the initial local measurement acts as a decorrelating operation, reducing the non-local coherences ($\rho_{14}$) responsible for the global capacity advantage. The regions of vanishing shift (white) correspond to separable limits or weak measurements where the perturbation to the correlation structure is negligible. Thus, the system incurs a deterministic ``correlation cost'' during the initial conditioning phase.

This result establishes the fundamental thermodynamic trade-off of the bipartite protocol: the system incurs a deterministic initial reduction in both energy and entanglement—defined here as the correlation cost—to condition the state into a subspace robust against collective dissipation. Consequently, the protocol functions not as an entanglement generator, which is forbidden by LOCC, but strictly as an entanglement preservation mechanism.

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\linewidth]{MAIN/wmtq2.png}
    \caption{Figure~5 characterizes the intermediate relaxation dynamics of the bipartite system. Consistent with the single-qubit results, increasing the measurement strength ($m \to 1$) suppresses the dissipative loss of global ergotropy (Panel a), effectively freezing the system's energy trajectory. Crucially, Panel (c) confirms that this stabilization extends to non-local resources: the strong measurement inhibits the contraction of the Capacity Gap ($\Delta C_{\text{gap}}$), thereby delaying the ``sudden death'' of entanglement that characterizes the unmonitored reference evolution..}
    \label{fig:results}
\end{figure}
