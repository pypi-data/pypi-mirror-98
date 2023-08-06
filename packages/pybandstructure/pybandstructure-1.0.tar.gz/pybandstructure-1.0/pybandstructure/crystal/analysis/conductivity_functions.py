import numpy as np
from numba import njit
from pybandstructure.common import *


def local_conductivity_interband(omega, alpha, beta, energy_diff, occupation_diff, momentum_matrix,
                                 integrate_bz, eta):
    with np.errstate(divide = 'ignore'):
        prefactor = - occupation_diff / energy_diff
        prefactor[np.logical_not(np.isfinite(prefactor))] = 0
        energy_denominator = 1./(omega + 1j*eta + energy_diff)
        S = integrate_bz( energy_denominator *  prefactor * momentum_matrix[alpha,:,:,:] * np.conj(momentum_matrix[beta,:,:,:]) ,axis =-1)
        return (1.j * np.pi * np.sum(S, axis = (0,1)))

def generalized_drude_weight(alpha, beta, exponent ,energies, chemical_potential, temperature, momentum_matrix_intra, integrate_bz, eta):
    f = delta_function(energies - chemical_potential,  temperature, shape = 'fermi') * np.power(energies - chemical_potential, exponent)
    return np.pi * integrate_bz(np.sum(f * momentum_matrix_intra[alpha,:,:] * momentum_matrix_intra[beta,:,:], axis = 0), axis = -1) 
