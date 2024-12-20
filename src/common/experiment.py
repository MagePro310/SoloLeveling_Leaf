"""Data objects for Experiments and Circuit objects.
Also contains functions to convert between them.
"""
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from circuit_knitting.cutting.qpd import WeightType
from qiskit import QuantumCircuit
from qiskit.quantum_info import PauliList


@dataclass
class Experiment:
    """Data class for cut results.
    Contains the information for one partition.
    """

    circuits: list[QuantumCircuit] | None
    coefficients: list[tuple[float, WeightType]]
    n_shots: int
    observables: PauliList | dict[str, PauliList]
    partition_label: str
    result_counts: list[dict[str, int]] | None
    uuid: UUID


@dataclass
class CircuitJob:
    """Data class for single cicruit.
    The circuit is enriched with information for reconstruction.
    """

    coefficient: tuple[float, WeightType]   | None
    cregs: int
    index: int
    instance: QuantumCircuit    | None
    n_shots: int
    observable: PauliList  # Should be single pauli
    partition_label: str
    result_counts: dict[str, int] | None
    uuid: UUID


@dataclass
class CombinedJob:
    """Data class for combined circuit object.
    Order of the lists has to be correct for all!
    """

    coefficients: list[tuple[float, WeightType]] = field(default_factory=list)
    cregs: list[int] = field(default_factory=list)
    indices: list[int] = field(default_factory=list)
    instance: QuantumCircuit | None = None
    mapping: list[slice] = field(default_factory=list)
    n_shots: int = 0
    observable: PauliList | None = None
    partition_labels: list[str] = field(default_factory=list)
    result_counts: dict[str, int] | None = None
    uuids: list[UUID] = field(default_factory=list)
    
@dataclass
class ScheduledJob:
    """Data class for scheduled job.
    Additionally includes which qpu to run on.
    """
    
    job: CombinedJob    # Probably don't need CircuitJob
    qpu: int            #Depends on scheduler


def job_from_circuit(circuit: QuantumCircuit) -> CircuitJob:
    """Create a CircuitJob from a QuantumCircuit.
    
    Args:
        circuit (QuantumCircuit): The circuit to create a job from.
        
    Returns:
        CircuitJob: The created CircuitJob.
    """
    return CircuitJob(
        coefficient=None,
        cregs=len(circuit.cregs),
        index=0,
        instance=circuit,
        n_shots=1024,
        observable=PauliList(""),
        partition_label="1",
        result_counts=None,
        uuid=uuid4(),
    )
    

def jobs_from_experiment(experiment: Experiment) -> list[CircuitJob]:
    """Create a list of CircuitJobs from an Experiment.
    
    Args:
        experiment (Experiment): The experiment to create jobs from.
        
    Returns:
        list[CircuitJob]: List of CircuitJobs.
    """
    return [
        CircuitJob(
            coefficient=experiment.coefficients[idx],
            cregs=len(circuit.cregs),
            index=idx,
            instance=circuit,
            n_shots=experiment.n_shots,
            # TODO this might need to change for proper observables
            observable=experiment.observables,
            partition_label=experiment.partition_label,
            result_counts=None,
            uuid=experiment.uuid,
        )
        for idx, circuit in enumerate(experiment.circuits)
    ]
