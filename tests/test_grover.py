"""
Unit tests for Grover's Search Algorithm package.
"""

import math
import pytest
from qiskit import QuantumCircuit
from src.oracle import build_oracle
from src.diffuser import build_diffuser
from src.grover import GroverSearch


class TestOracleAndDiffuser:
    """Tests for individual circuit component generation."""

    def test_oracle_qubit_count_and_name(self):
        """Verify phase oracle circuit dimensions and structure."""
        n_qubits = 3
        target = "101"
        oracle = build_oracle(target, n_qubits)

        assert isinstance(oracle, QuantumCircuit)
        assert oracle.num_qubits == n_qubits
        assert oracle.name == "Oracle"

    def test_oracle_invalid_target_length(self):
        """Verify error handling when target length mismatches n_qubits."""
        with pytest.raises(ValueError, match="does not match n_qubits"):
            build_oracle(targets="1010", n_qubits=3)

    def test_diffuser_qubit_count_and_name(self):
        """Verify diffuser circuit dimensions."""
        n_qubits = 4
        diffuser = build_diffuser(n_qubits)

        assert isinstance(diffuser, QuantumCircuit)
        assert diffuser.num_qubits == n_qubits
        assert diffuser.name == "Diffuser"


class TestGroverSearchPipeline:
    """Tests for full algorithm iteration count and search accuracy."""

    @pytest.mark.parametrize(
        "n_qubits, num_marked, expected_iterations",
        [
            (2, 1, 1),  # N=4, M=1 -> floor(pi/4 * sqrt(4)) = 1
            (3, 1, 2),  # N=8, M=1 -> floor(pi/4 * sqrt(8)) = 2
            (4, 1, 3),  # N=16, M=1 -> floor(pi/4 * sqrt(16)) = 3
        ],
    )
    def test_optimal_iteration_calculation(self, n_qubits, num_marked, expected_iterations):
        """Verify correct optimal iteration count calculation."""
        target = "1" * n_qubits
        grover = GroverSearch(targets=target)
        assert grover.iterations == expected_iterations

    @pytest.mark.parametrize("target", ["01", "10", "11"])
    def test_grover_search_2qubit_accuracy(self, target):
        """Verify 2-qubit search achieves > 90% probability for the target state."""
        grover = GroverSearch(targets=target)
        shots = 1000
        counts, top_result = grover.run(shots=shots)

        assert top_result == target
        assert counts[target] / shots >= 0.90

    @pytest.mark.parametrize("target", ["000", "101", "111"])
    def test_grover_search_3qubit_accuracy(self, target):
        """Verify 3-qubit search achieves high success probability."""
        grover = GroverSearch(targets=target)
        shots = 1000
        counts, top_result = grover.run(shots=shots)

        assert top_result == target
        assert counts[target] / shots >= 0.90

    def test_multi_target_search(self):
        """Verify multi-target search finds one of the valid targets."""
        targets = ["010", "101"]
        grover = GroverSearch(targets=targets, n_qubits=3)
        shots = 1000
        counts, top_result = grover.run(shots=shots)

        assert top_result in targets
        # Combined probability of targets should dominate total counts
        combined_success = sum(counts.get(t, 0) for t in targets) / shots
        assert combined_success >= 0.85