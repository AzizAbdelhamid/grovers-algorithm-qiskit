"""
Grover Diffuser (Amplification Operator) Builder.
"""

from qiskit import QuantumCircuit


def build_diffuser(n_qubits: int) -> QuantumCircuit:
    """
    Constructs the Grover Diffuser operator (Inversion about the mean).

    Mathematical transformation:
        D = 2|s><s| - I

    Parameters:
        n_qubits: Number of qubits in the circuit.

    Returns:
        QuantumCircuit: The diffuser sub-circuit.
    """
    qc = QuantumCircuit(n_qubits, name="Diffuser")

    # Step 1: H^n
    qc.h(range(n_qubits))

    # Step 2: X^n
    qc.x(range(n_qubits))

    # Step 3: Phase shift around |11...1>
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

    # Step 4: X^n
    qc.x(range(n_qubits))

    # Step 5: H^n
    qc.h(range(n_qubits))

    return qc