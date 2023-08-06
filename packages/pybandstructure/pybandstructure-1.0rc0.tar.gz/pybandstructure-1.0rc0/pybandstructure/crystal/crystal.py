import numpy as np
from tqdm import tqdm
from pybandstructure.geometry.crystal_geometry import Crystal_Geometry
from pybandstructure.band_structure.band_structure import Band_Structure
from warnings import warn
from pybandstructure.crystal.analysis import dos_functions
from pybandstructure.crystal.analysis import conductivity_functions

class Crystal():
    def __init__(self, geometry, band_structure, eta = 1e-6):
        assert isinstance(geometry, Crystal_Geometry)
        self._geometry = geometry
        assert isinstance(band_structure, Band_Structure)
        self._band_structure = band_structure
        self.eta = eta

    @property
    def geometry(self): return self._geometry
    @geometry.setter
    def geometry(self, _): warn('geometry cannot be changed')

    @property
    def band_structure(self): return self._band_structure
    @band_structure.setter
    def band_structure(self, _): warn('band_structure cannot be changed')

    def get_transformation_matrix(self, tensor_order):
        if tensor_order > 8 or tensor_order < 1:
            raise ValueError('''tensors with at least 1 and at most 8 indices are supported''')
        input_string =', '.join([chr(ord('a') + i) + chr(ord('i') + i) for i in range(tensor_order)])
        output_string = (''.join([chr(ord('a') + i) for i in range(tensor_order)]) + ''.join([chr(ord('i') + i) for i in range(tensor_order)]))
        path_string = input_string + '->' + output_string
        result_list = [np.einsum(path_string, 
                                    *[rho for i in range(tensor_order)]) 
                        for rho in self.geometry.point_group.group_matrices]
        result = np.sum(result_list, axis = 0)/self.geometry.point_group.cardinality
        result = np.round(result, decimals = 7)
        result[np.isclose(result,0.)] = 0.
        nz = np.stack(np.nonzero(result)[tensor_order:],axis = 1)
        if nz.size != 0:
            non_zero = [tuple(key) for key in np.unique(nz,axis = 0)]
        else:
            non_zero = []
        return result, non_zero

    #dos related functions

    def dos(self, epsilon):
        return dos_functions.dos(epsilon = epsilon, energies = self.band_structure.energies, integrate_bz = self.band_structure.integrate_bz, eta = self.eta)

    def jdos(self, epsilon, nu, mu):
        return dos_functions.jdos(epsilon = epsilon, nu = nu, mu = mu, energies = self.band_structure.energies, integrate_bz = self.band_structure.integrate_bz, eta = self.eta)

    #conductivity related functions

    def local_interband_conductivity(self, omega, use_bands = slice(None)):
        b = np.broadcast(omega)
        result = []
        energy_diff = np.expand_dims(self.band_structure.energies[use_bands,:], 1) - np.expand_dims(self.band_structure.energies[use_bands,:], 0)
        occupation_diff = np.expand_dims(self.band_structure.occupations[use_bands,:], 1) - np.expand_dims(self.band_structure.occupations[use_bands,:], 0)
        momentum_matrix = self.band_structure.momentum_matrix[:,use_bands, use_bands,:]
        transformation_matrix, nonzero_components = self.get_transformation_matrix(tensor_order = 2)
        for omega_val in tqdm(b):
            sigma_IBZ = np.zeros([self.geometry.space_dimension, self.geometry.space_dimension], dtype = complex)
            for alpha, beta in nonzero_components:
                sigma_IBZ[alpha, beta] = conductivity_functions.local_conductivity_interband(omega = omega_val[0], alpha = alpha, beta = beta, 
                    energy_diff =energy_diff, occupation_diff = occupation_diff , momentum_matrix = momentum_matrix,
                    integrate_bz = self.band_structure.integrate_bz, eta = self.eta)
            result.append(np.tensordot(transformation_matrix, sigma_IBZ, axes = 2))
        return np.array(result).reshape(b.shape + (self.geometry.space_dimension, self.geometry.space_dimension))

    def generalized_drude_weight(self, chemical_potential = None, temperature = None, exponent = 0, use_bands = slice(None)):
        if chemical_potential is None:
            chemical_potential = self.band_structure.chemical_potential
        if temperature is None:
            temperature = self.band_structure.temperature
        momentum_matrix_intra = np.real(np.einsum('aiik->aik', self.band_structure.momentum_matrix[:,use_bands,use_bands,:]))
        transformation_matrix, nonzero_components = self.get_transformation_matrix(tensor_order = 2)
        result = []
        b = np.broadcast(chemical_potential, temperature)
        for mu_val, T_val in b:
            drude_IBZ = np.zeros([self.geometry.space_dimension, self.geometry.space_dimension], dtype = float)
            for alpha, beta in nonzero_components:
                drude_IBZ[alpha, beta] = conductivity_functions.generalized_drude_weight(alpha = alpha, beta = beta, exponent =exponent ,
                    energies = self.band_structure.energies[use_bands,:], 
                    chemical_potential = mu_val, temperature = T_val, 
                    momentum_matrix_intra = momentum_matrix_intra, 
                    integrate_bz = self.band_structure.integrate_bz, eta=self.eta)
            result.append(np.tensordot(transformation_matrix, drude_IBZ, axes = 2))
        return np.array(result).reshape(b.shape + (self.geometry.space_dimension, self.geometry.space_dimension))
    
    def local_intraband_conductivity(self, omega, use_bands = slice(None)):
        b = np.broadcast(omega)
        D = self.generalized_drude_weight(use_bands=use_bands)
        result = [1j * D/(omega_val[0] + 1j * self.eta) for omega_val in b]
        return np.array(result).reshape(b.shape + (self.geometry.space_dimension, self.geometry.space_dimension))

    def local_conductivity(self, omega, use_bands = slice(None)):
        return self.local_intraband_conductivity(omega, use_bands = use_bands) + self.local_interband_conductivity(omega, use_bands = use_bands)
