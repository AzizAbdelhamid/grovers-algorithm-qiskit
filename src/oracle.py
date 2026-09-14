"""
Phase Oracle Builder for Grover's Algorithm.
"""

from typing import List, Union
from qiskit import QuantumCircuit


def build_oracle(targets: Union[str, List[str]], n_qubits: int) -> QuantumCircuit:
    """
    Constructs a phase oracle for one or more target bitstrings.

    Parameters:
        targets: A single bitstring (e.g. '101') or a list of target bitstrings.
        n_qubits: Total number of qubits in the system.

    Returns:
        QuantumCircuit: The constructed phase oracle circuit.
    """
    if isinstance(targets, str):
        targets = [targets]

    qc = QuantumCircuit(n_qubits, name="Oracle")

    for target in targets:
        if len(target) != n_qubits:
            raise ValueError(
                f"Target length '{target}' ({len(target)}) does not match n_qubits ({n_qubits})."
            )

        # Apply X gates to map '0' bits to |1> so target aligns with |1...1>
        for i, bit in enumerate(reversed(target)):
            if bit == "0":
                qc.x(i)

        # Multi-controlled Z gate using Hadamard sandwich around MCX
        if n_qubits == 1:
            qc.z(0)
        elif n_qubits == 2:
            qc.cz(0, 1)
        else:
            controls = list(range(n_qubits - 1))
            target_qubit = n_qubits - 1
            qc.h(target_qubit)
            qc.mcx(controls, target_qubit)
            qc.h(target_qubit)

        # Revert X gates
        for i, bit in enumerate(reversed(target)):
            if bit == "0":
                qc.x(i)

    return qc