# Copyright 2020 Q-CTRL Pty Ltd & Q-CTRL Inc. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
"""
Module for nodes related to open quantum systems.
"""


from typing import (
    List,
    Optional,
    Tuple,
    Union,
)

import forge
import numpy as np
from scipy.sparse import coo_matrix

from qctrlcommons.node import types
from qctrlcommons.node.module import CoreNode
from qctrlcommons.node.node_data import (
    SparsePwcNodeData,
    TensorPwcNodeData,
)
from qctrlcommons.node.tensorflow import TensorNodeData
from qctrlcommons.node.utils import (
    check_argument,
    check_density_matrix_shape,
    check_lindblad_terms,
    check_oqs_hamiltonian,
)
from qctrlcommons.preconditions import check_sample_times


class DensityMatrixEvolutionPwc(CoreNode):
    r"""
    Calculates the state evolution of an open system described by the GKS-Lindblad master
    equation.

    The controls that you provide to this function have to be in piecewise constant
    format. If your controls are smooth sampleable tensor-valued functions (STFs), you
    have to discretize them with `discretize_stf` before passing them to this function.
    You may need to increase the number of segments that you choose for the
    discretization depending on the sizes of oscillations in the smooth controls.

    Parameters
    ----------
    initial_density_matrix : Union[np.ndarray, Tensor]
        A 2D array of the shape ``[D, D]`` representing the initial density matrix of
        the system, :math:`\rho_{\rm s}`. You can also pass a batch of density matrices
        and the input data shape must be ``[B, D, D]`` where ``B`` is the batch dimension.
    hamiltonian : Union[TensorPwc, SparsePwc]
        A piecewise-constant function representing the effective system Hamiltonian,
        :math:`H_{\rm s}(t)`, for the entire evolution duration. A sparse Hamiltonian gets
        converted to a dense Hamiltonian.
    lindblad_terms : List[Tuple[float, Union[np.ndarray, scipy.sparse.coo_matrix]]]
        A list of pairs, :math:`(\gamma_j, L_j)`, representing the positive decay rate
        :math:`\gamma_j` and the Lindblad operator :math:`L_j` for each coupling
        channel :math:`j`. Sparse operators get converted to dense operators.
    sample_times : np.ndarray, optional
        A 1D array of length :math:`T` specifying the times :math:`\{t_i\}` at which this
        function calculates system states. Must be ordered and contain at least one element.
    krylov_subspace_dimension : Union[Tensor, int], optional
        The dimension of the Krylov subspace `k` for the Arnoldi method, which allows a more
        efficient calculation for large Hilbert spaces. A larger value leads to
        a better precision at the cost of longer computational time. If omitted or None
        it calculates the exact piecewise constant solution.

    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor(complex)
        Systems states at sample times. The shape of the return value is ``[D, D]`` or
        ``[T, D, D]``, depending on whether you provide sample times.
        Otherwise, the shape is ``[B, T, D, D]`` if you provide a batch of initial states.

    See Also
    --------
    discretize_stf

    Notes
    -----
    Under Markovian approximation, the dynamics of an open quantum system can be described by
    the GKS-Lindblad master equation [1]_ [2]_

    .. math::
        \frac{{\rm d}\rho_{\rm s}(t)}{{\rm d}t} = -i [H_{\rm s}(t), \rho_{\rm s}(t)]
        + \sum_j \gamma_j {\mathcal D}[L_j] \rho_{\rm s}(t) \;,

    where :math:`{\mathcal D}` is a superoperator describing the decoherent process in the
    system evolution and defined as

    .. math::
        {\mathcal D}[X]\rho := X \rho X^\dagger
            - \frac{1}{2}\left( X^\dagger X \rho + \rho X^\dagger X \right)

    for any system operator :math:`X`. This function calculates the system state at the
    sample times :math:`t_j` that you provide.

    References
    ----------
    .. [1] `V. Gorini, A. Kossakowski, E. C. G. Sudarshan,
            Journal of Mathematical Physics 17, 821 (1976).
            <https://doi.org/10.1063/1.522979>`_
    .. [2] `G. Lindblad, Communications in Mathematical Physics, 48, 119–130 (1976).
            <https://doi.org/10.1007/BF01608499>`_
    """
    name = "density_matrix_evolution_pwc"
    _module_attr = "density_matrix_evolution_pwc"
    args = [
        forge.arg("initial_density_matrix", type=Union[types.Tensor, np.ndarray]),
        forge.arg("hamiltonian", type=Union[types.TensorPwc, types.SparsePwc]),
        forge.arg(
            "lindblad_terms", type=List[Tuple[float, Union[np.ndarray, coo_matrix]]]
        ),
        forge.arg("sample_times", type=Optional[np.ndarray], default=None),
        forge.arg(
            "krylov_subspace_dimension",
            type=Union[int, types.Tensor, None],
            default=None,
        ),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        sample_times = kwargs.get("sample_times")
        initial_density_matrix = kwargs.get("initial_density_matrix")
        hamiltonian = kwargs.get("hamiltonian")
        lindblad_terms = kwargs.get("lindblad_terms")

        check_argument(
            isinstance(hamiltonian, (TensorPwcNodeData, SparsePwcNodeData)),
            "Hamiltonian must be a TensorPwc or a SparsePwc.",
            {"hamiltonian": hamiltonian},
        )
        if sample_times is not None:
            check_sample_times(sample_times, "sample_times")
        check_density_matrix_shape(initial_density_matrix, "initial_density_matrix")
        check_oqs_hamiltonian(hamiltonian, initial_density_matrix.shape[-1])
        check_lindblad_terms(lindblad_terms, initial_density_matrix.shape[-1])

        initial_state_shape = initial_density_matrix.shape
        if sample_times is None:
            shape = initial_state_shape
        else:
            shape = (
                initial_state_shape[:-2]
                + (len(sample_times),)
                + initial_state_shape[-2:]
            )
        return TensorNodeData(_operation, shape=shape)
