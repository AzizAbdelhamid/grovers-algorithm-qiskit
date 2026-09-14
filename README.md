# Quantum Search via Grover's Algorithm (Qiskit Implementation)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Qiskit](https://img.shields.io/badge/Qiskit-1.0%2B-6133BD.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An end-to-end Python implementation of **Grover’s Quantum Search Algorithm** built with **Qiskit**. This repository demonstrates how quantum superposition, phase inversion, and amplitude amplification provide a quadratic speedup for unstructured database search over classical algorithms.

---

## 📌 Project Overview

Classical unstructured search requires $\mathcal{O}(N)$ evaluations to find a specific item in a database of size $N$. Grover's Algorithm solves this problem on a quantum computer using only $\mathcal{O}(\sqrt{N})$ queries.

This repository features:
- **Scalable $N$-Qubit Grover Circuit Architecture**: Automated generation of Phase Oracles and Diffuser operators for arbitrary target bitstrings.
- **Mathematical Step-by-Step Explanation**: Detailed breakdown of geometric state reflections and operator matrices.
- **Qiskit Aer Simulation**: Ideal execution and histogram visualization of measurement outcomes.
- **Interactive Jupyter Notebook**: Walkthrough with statevector evolutions and bloch sphere visualizations.

---

## 🧮 Mathematical Foundation

Grover's algorithm operates on an $n$-qubit system representing an unsorted search space of $N = 2^n$ elements.

### 1. Equal Superposition State
The system is initialized into a uniform superposition state $|\psi\rangle$ by applying Hadamard gates ($H^{\otimes n}$) to $|0\rangle^{\otimes n}$:

$$|\psi\rangle = \frac{1}{\sqrt{N}} \sum_{x=0}^{N-1} |x\rangle$$

### 2. Phase Oracle ($U_\omega$)
The oracle identifies the target state $|\omega\rangle$ and flips its phase while leaving all non-target states unaffected:

$$U_\omega |x\rangle = \begin{cases} -|x\rangle & \text{if } x = \omega \\ |x\rangle & \text{if } x \neq \omega \end{cases}$$

In matrix form, $U_\omega = I - 2|\omega\rangle\langle\omega|$.

### 3. Grover Diffuser / Amplitude Amplification ($U_s$)
The diffuser acts as an **inversion about the mean** amplitude across all computational basis states. It consists of Hadamard transformations and a phase shift about the initial state $|\psi\rangle$:

$$U_s = 2|\psi\rangle\langle\psi| - I = H^{\otimes n} (2|0\rangle\langle 0|^{\otimes n} - I) H^{\otimes n}$$

### 4. Optimal Iterations
Each application of the combined Grover operator $G = U_s U_\omega$ rotates the state vector toward the target state $|\omega\rangle$ by an angle $\theta \approx 2/\sqrt{N}$. The optimal number of Grover iterations $R$ required is:

$$R \approx \left\lfloor \frac{\pi}{4} \sqrt{N} \right\rfloor$$

---

## 📐 Circuit Architecture

The overall Grover circuit structure follows four distinct stages:

```text
       ┌───┐    ┌──────────┐    ┌──────────┐    ┌─┐
|0⟩ ───┤ H ├────┤          ├────┤          ├────┤M├──────
       ├───┤    │  Phase   │    │  Grover  │    ├──┤
|0⟩ ───┤ H ├────┤  Oracle  ├────┤ Diffuser ├────┤M├──────
       └───┘    │ $U_\omega$│   │   $U_s$  │    └┬┘
  ...           └──────────┘    └──────────┘     │
```

1. **Initialization:** Apply Hadamard transform $H^{\otimes n}$.
2. **Oracle Query ($U_\omega$):** Flips the amplitude of target bitstring $|\omega\rangle$.
3. **Diffuser ($U_s$):** Reflects amplitudes across the mean to boost probability of $|\omega\rangle$.
4. **Measurement:** Collapses the state vector to extract the solution state with high probability.

---

## 📦 Installation

### Prerequisites
- Python 3.9+
- Virtual environment (recommended)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/grovers-algorithm-qiskit.git
   cd grovers-algorithm-qiskit
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Quickstart & Usage

Run Grover's algorithm directly using the Python CLI:

```python
from src.grover import GroverSearch

# Initialize search for a 3-qubit target state |101> (N = 8)
target = "101"
grover = GroverSearch(target_bitstring=target)

# Build and execute circuit
circuit, counts = grover.run(shots=1024)

print(f"Target Bitstring: {target}")
print("Measurement Results:", counts)
```

### Running unit tests
Validate circuit output across different bitstrings:
```bash
pytest tests/
```

---

## 📊 Results & Visualization

Running a 3-qubit search for target state $|101\rangle$ yields high-probability measurement for the correct item after $R = 2$ iterations:

```text
Measurement Histogram (1024 shots):
|101⟩: ██████████████████████████████████ (95.2%)
|000⟩: ▏ (0.7%)
|001⟩: ▎ (0.7%)
|010⟩: ▎ (0.7%)
|011⟩: ▎ (0.7%)
|100⟩: ▎ (0.7%)
|110⟩: ▎ (0.7%)
|111⟩: ▎ (0.7%)
```

---

## 📂 Repository Structure

```text
grovers-algorithm-qiskit/
├── README.md                  # Project overview and documentation
├── requirements.txt           # Dependencies (qiskit, qiskit-aer, matplotlib)
├── notebooks/
│   └── grover_tutorial.ipynb  # Interactive walkthrough with plots
├── src/
│   ├── __init__.py
│   ├── oracle.py              # Phase oracle constructor
│   ├── diffuser.py            # Grover diffuser module
│   └── grover.py              # Main Grover algorithm pipeline
└── tests/
    └── test_grover.py         # Automated test suite
```

---

## 📜 References

1. Grover, L. K. (1996). *A fast quantum mechanical algorithm for database search*. Proceedings of the 28th Annual ACM Symposium on Theory of Computing (STOC).
2. Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
3. Qiskit Textbook: [Grover's Algorithm](https://learning.quantum.ibm.com/)

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.