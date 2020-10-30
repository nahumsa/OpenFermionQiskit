from openfermion.transforms import jordan_wigner, bravyi_kitaev
from qiskit.aqua.operators import PauliOp
from qiskit.quantum_info import Pauli


class QiskitConverter:
  """ Convert from a OpenFermion Fermionic Operator to a 
  qiskit Aqua Pauli Operator.

  """
  def __init__(self, hamiltonian, map_type):
    """ Initialization of the class.
    
    Args:
    - hamiltonian(openfermion.FermionOperator): Fermion Operator build using 
    openfermion.
    - map_type(string): Type of mapping, 'jw' for Jordan-Wigner mapping, and
    'bk' for Bravyi-Kitaev mapping.
    
    """
    self._map_type = map_type
    self._hamiltonian = hamiltonian
    self._pauli_op = self._hamiltonian_to_pauliop()
  
  @property
  def hamiltonian(self):
    """ Returns Fermionic Hamiltonian.
    """
    return self._hamiltonian
  
  @property
  def map_type(self):
    """ Returns the map type used.
    """
    return self._map_type

  @property
  def pauli_op(self):
    """ (qiskit.aqua.operator) : Summed pauli operator corresponding to the 
      fermionic operator.
    """
    return self._pauli_op

  @property
  def open_fermion_op(self):
    """ Open fermion qubit operator.
    """
    return self._qubitOp
  
  @property
  def pauli_dict(self):
    """ Dictionary with pauli strings and coefficients.
    """
    return self._Pauli_dict

  @property
  def n_qubits(self):
    """ Number of qubits needed to simulate the hamiltonian.
    """
    return self._n_qubits

  def _get_nqubits(self):
    """ Returns the number of qubits needed to simulate de qubit operator.
    """
    qubits = []
    for key, vals in self._qubitOp.terms.items():
      for qubit, _ in key:
        qubits.append(qubit)        
    return max(qubits) + 1

  def _pauli_dict(self):
    """ Creates a pauli dictionary that keeps the pauli string and the 
    coefficients.
    """
    Pauli_dict = {}
    for key, val in self._qubitOp.terms.items():
      s = 'I'*self._n_qubits
      for qubit, string in key:
        s = s[:qubit] + string + s[qubit+1:]
      Pauli_dict[s] = val
    return Pauli_dict

  def _hamiltonian_to_pauliop(self):
    """ Convert from a OpenFermion Fermionic Operator to a 
    qiskit Aqua Operator.
  
    """
    if self._map_type == 'jw':
      self._qubitOp = jordan_wigner(self._hamiltonian)
    
    elif self._map_type == 'bk':
      self._qubitOp = bravyi_kitaev(self._hamiltonian)

    self._n_qubits = self._get_nqubits()

    self._Pauli_dict = self._pauli_dict()

    Pauli_Op = 0    
    for string, coeff in self._Pauli_dict.items():
      Pauli_Op += PauliOp(Pauli(label=string), coeff)
    
    return Pauli_Op