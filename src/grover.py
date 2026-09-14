"""
Main Grover Search Algorithm Execution Pipeline.
"""

import math
from typing import Dict, List, Optional, Tuple, Union
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from .diffuser import build_diffuser
from .oracle import build_oracle


class GroverSearch:
    """
    Grover's Search Algorithm manager.

    Automatically calculates optimal iteration counts, builds circuits, and executes simulations.
    """

    def __init__(self, targets: Union[str, List[str]], n_qubits: Optional[int] = None):
        """
        Parameters:
            targets: Target bitstring(s) to search for (e.g. '101' or ['101', '010']).
            n_qubits: Number of qubits (inferred from targets if not specified).
        """
        if isinstance(targets, str):
            self.targets = [targets]
        else:
            self.targets = targets

        self.n_qubits = n_qubits or len(self.targets[0])
        self.num_items = 2**self.n_qubits
        self.num_marked = len(self.targets)

        # Calculate optimal iteration count: floor(pi/4 * sqrt(N / M))
        self.iterations = max(
            1, math.floor((math.pi / 4) * math.sqrt(self.num_items / self.num_marked))
        )

        self.oracle = build_oracle(self.targets, self.n_qubits)
        self.diffuser = build_diffuser(self.n_qubits)
        self.circuit = self._build_full_circuit()

    def _build_full_circuit(self) -> QuantumCircuit:
        """Assembles initialization, oracle, diffuser iterations, and measurement."""
        qc = QuantumCircuit(self.n_qubits, self.n_qubits)

        # State initialization: Uniform superposition
        qc.h(range(self.n_qubits))
        qc.barrier()

        # Apply Grover iterations
        for _ in range(self.iterations):
            qc.compose(self.oracle, inplace=True)
            qc.barrier()
            qc.compose(self.diffuser, inplace=True)
            qc.barrier()

        # Measurement
        qc.measure(range(self.n_qubits), range(self.n_qubits))
        return qc

    def run(self, shots: int = 1024) -> Tuple[Dict[str, int], str]:
        """
        Executes the circuit on AerSimulator.

        Returns:
            Tuple containing:
                - counts (Dict[str, int]): Measurement outcomes.
                - top_result (str): Most frequently measured bitstring.
        """
        simulator = AerSimulator()
        result = simulator.run(self.circuit, shots=shots).result()
        counts = result.get_counts()
        top_result = max(counts, key=counts.get)
        return counts, top_result


if __name__ == "__main__":
    target = "101"
    grover = GroverSearch(targets=target)
    print(f"Searching for target |{target}> across {grover.n_qubits} qubits...")
    print(f"Optimal Grover iterations: {grover.iterations}")

    counts, top_result = grover.run(shots=1024)
    print("Measurement Results:", counts)
    print(f"Top Measured State: |{top_result}> (Target: |{target}>)")