#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''class for calculating and storing band structures'''
############################ Import modules ############################
import os
from warnings import warn
import numpy as np
from scipy.linalg import eigh
from numpy.linalg import multi_dot
from scipy.optimize import root_scalar
from tqdm import tqdm
import h5py
import matplotlib.pyplot as plt

from pybandstructure.common import *
from pybandstructure.sample.sample import Unit_Cell_Sample
from pybandstructure.operators.operators import *

class Band_Structure():
    def __init__(self, 
                 k_sample, 
                 energies = None, wavefunctions = None, 
                 hamiltonian = None, overlap = None,
                 momentum_operator = None, momentum_matrix = None,
                 degeneracy = 2, zero_filling = 0, 
                 density = 0, temperature = 0):

    
        assert isinstance(k_sample, Unit_Cell_Sample)
        self._k_sample = k_sample
        #add checks on dimensions
        self._energies = energies
        self._wavefunctions = wavefunctions

        assert (hamiltonian is None 
               or isinstance(hamiltonian, Momentum_Conserving_Operator))
        self._hamiltonian = hamiltonian
        assert (overlap is None 
                or isinstance(overlap, Momentum_Conserving_Operator))
        self._overlap = overlap

        assert (type(momentum_operator) == list and all([isinstance(pi, Momentum_Conserving_Operator) for pi in momentum_operator])) or momentum_operator is None
        self._momentum_operator = momentum_operator
        #add checks on dimensions
        self._momentum_matrix = momentum_matrix
    
        self._degeneracy = degeneracy
        self._zero_filling = zero_filling

        self._density = density
        self._temperature = temperature

        if self._energies is None:
            self._chemical_potential = None
        else:
            self._chemical_potential = self.compute_chemical_potential(self._density, self._temperature)

        if self._energies is None:
            self._occupations = None
        else:
            self._occupations = self.compute_occupations()
        
########### Properties #################################################

    @property
    def k_sample(self): return self._k_sample
    @k_sample.setter
    def k_sample(self, value): warn('k_sample cannot be changed.')

    @property
    def energies(self): return self._energies
    @energies.setter
    def energies(self, value): warn('energies cannot be changed.')

    @property
    def wavefunctions(self): return self._wavefunctions
    @wavefunctions.setter
    def wavefunctions(self, value): warn('wavefunctions cannot be changed.')

    @property
    def momentum_matrix(self): return self._momentum_matrix
    @momentum_matrix.setter
    def momentum_matrix(self, value): warn('momentum_matrix cannot be changed')

    @property
    def degeneracy(self): return self._degeneracy
    @degeneracy.setter
    def degeneracy(self, value): warn('degeneracy cannot be changed')

    @property
    def zero_filling(self): return self._zero_filling
    @zero_filling.setter 
    def zero_filling(self, value): warn('zero_filling cannot be changed')

    @property
    def density(self): return self._density
    @density.setter
    def density(self, value):
        warnings.warn('changing density without changing band structure')
        self._density = value
        self._chemical_potential = self.compute_chemical_potential(self._density, 
                                                                   self._temperature)
        self._occupations = self.compute_occupations()

    @property
    def temperature(self): return self._temperature
    @temperature.setter
    def temperature(self, value):
        warnings.warn('changing temperature without changing band structure')
        self._temperature = value
        self._chemical_potential = self.compute_chemical_potential(self._density, 
                                                                   self._temperature)
        self._occupations = self.compute_occupations()

    @property
    def chemical_potential(self):
        return self._chemical_potential
    @chemical_potential.setter
    def chemical_potential(self, value):
        warnings.warn('''changing chemical potential 
                         without changing band structure''')
        self._chemical_potential = value
        self._density = self.compute_density(self._chemical_potential,
                                             self._temperature)
        self._occupations = self.compute_occupations()

    @property
    def occupations(self):
        return self._occupations
    @occupations.setter
    def occupations(self, value):
        warnings.warn('''occupations cannot bee changed directly, change chemical_potential, density or temperature instead''')


  

########### Methods ####################################################

    def compute_bands(self, eigvals = None):

        if (not self._energies is None) or (not self._wavefunctions is None):
            raise ValueError('bandstructure already present')

        if eigvals is None:
            n_bands = self._hamiltonian.size
        else:
            n_bands = eigvals[1] - eigvals[0] + 1
        self._energies = np.zeros([n_bands, len(self._k_sample)], dtype = float)
        self._wavefunctions = np.zeros([self._hamiltonian.size, n_bands, len(self._k_sample)], 
                                       dtype = complex)

        for i, k in tqdm(enumerate(self._k_sample.coords)):
            energies, wavefunctions = self._hamiltonian.diagonalize(k, overlap = self._overlap, eigvals = eigvals)
            self._energies[:,i] = energies
            self._wavefunctions[:,:,i] = wavefunctions
        
        self._chemical_potential = self.compute_chemical_potential(self.density, self.temperature)
        self._occupations = self.compute_occupations()

    def compute_momentum_matrix(self):
        momentum_list = []
        for pi in self._momentum_operator:
            momentum_list.append(pi.compute_matrix_elements(k_points = self._k_sample.coords, wavefunctions = self._wavefunctions))
        self._momentum_matrix = np.stack(momentum_list) 


    def save(self, file_name, band_structure_name, file_format = 'hdf5'):
        if file_format == 'hdf5':
            with h5py.File(file_name, 'a') as file_to_write:
                bands = file_to_write.create_group(band_structure_name)
                file_to_write[band_structure_name + '/energies'] = self._energies
                file_to_write[band_structure_name + '/wavefunctions'] = self._wavefunctions
                file_to_write[band_structure_name + '/k_points'] = self._k_sample.coords

                file_to_write[band_structure_name].attrs['degeneracy'] = self._degeneracy
                file_to_write[band_structure_name].attrs['zero_filling'] = self._zero_filling
                file_to_write[band_structure_name].attrs['density'] = self._density
                file_to_write[band_structure_name].attrs['temperature'] = self._temperature

                if not self._momentum_matrix is None:
                    file_to_write[band_structure_name + '/momentum_matrix'] = self._momentum_matrix
            self._k_sample.save(file_name = file_name, 
                                sample_name = band_structure_name + '/k_sample', 
                                file_format = file_format)
        else:
            warn('invalid file_format')
    
    def plot(self, contour, energy_scale = 1, emin = None, emax = None, **kwargs):
        index, distances , points =  self._k_sample.contour(contour)
        if emin is None:
            emin = 1.1 * np.amin(self._energies) - 0.1 * np.amax(self._energies)
        if emax is None:
            emax = 1.1 * np.amax(self._energies) - 0.1 * np.amin(self._energies)
        bands = []
        frame = []
        for i in range(self._energies.shape[0]):
            bands.append(plt.plot(distances, energy_scale * self.energies[i,index], **kwargs))
        for point in points:
            frame.append(plt.plot([distances[point],distances[point]],[energy_scale * emin,energy_scale * emax],lw=0.5, c='k'))
        cp = plt.plot([distances[0],distances[-1]],[ self.chemical_potential, self.chemical_potential],'--',c='k', lw=0.5)
        plt.xticks(distances[points],contour)
        plt.ylim(energy_scale * emin, energy_scale * emax)
        return bands, frame, cp
    def integrate_bz(self, array, axis):
        return self._k_sample.integrate(array, axis) * self.degeneracy / ((2. * np.pi)**self.k_sample.lattice_dimension)

    def compute_density(self, chemical_potential, temperature):
        return _compute_density(chemical_potential, temperature,
                                energies = self._energies, distribution_function = fermi_function, 
                                degeneracy = self._degeneracy, unit_cell_volume = (2. *np.pi)**(self._k_sample.lattice_dimension) / self._k_sample.cell_volume, 
                                weights = self._k_sample.weights, zero_filling = self.zero_filling)
    
    def compute_chemical_potential(self, density, temperature):
        return _compute_chemical_potential(density, temperature, 
                                energies = self._energies, distribution_function = fermi_function, 
                                degeneracy = self._degeneracy, unit_cell_volume = (2. *np.pi)**(self._k_sample.lattice_dimension) / self._k_sample.cell_volume, 
                                weights = self._k_sample.weights, zero_filling = self.zero_filling)

    def compute_occupations(self):
        return fermi_function(self._energies -self._chemical_potential, self._temperature)

    

######## Constructors ##################################################

    @classmethod
    def from_file(cls, file_name, band_structure_name, file_format = 'hdf5'):
        if file_format == 'hdf5':
            with h5py.File(file_name, 'r') as file_to_read:
                energies = file_to_read[band_structure_name + '/energies'][...]
                wavefunctions = file_to_read[band_structure_name + '/wavefunctions'][...]
                k_sample = Unit_Cell_Sample.from_file(file_name = file_name, 
                                                      sample_name = band_structure_name + '/k_sample')
                if 'momentum_matrix' in file_to_read[band_structure_name]:
                    momentum_matrix = file_to_read[band_structure_name + '/momentum_matrix'][...]
                else:
                    momentum_matrix = None
                degeneracy = file_to_read[band_structure_name].attrs['degeneracy'] 
                zero_filling = file_to_read[band_structure_name].attrs['zero_filling'] 
                density = file_to_read[band_structure_name].attrs['density']
                temperature = file_to_read[band_structure_name].attrs['temperature'] 
        else:
            warn('unrecognized file type')
        return cls(k_sample = k_sample, 
                   energies = energies, wavefunctions = wavefunctions, momentum_matrix = momentum_matrix,
                   degeneracy = degeneracy, zero_filling = zero_filling, density =  density , temperature = temperature)

    @classmethod
    def from_data(cls, k_sample, energies, wavefunctions, 
                  degeneracy = 2, zero_filling = 0, density = 0, temperature = 0,
                  momentum_matrix = None):
        return cls(k_sample = k_sample, 
                   energies = energies, wavefunctions = wavefunctions, momentum_matrix = momentum_matrix,
                   degeneracy = degeneracy, zero_filling = zero_filling, density =  density , temperature = temperature)

    @classmethod
    def from_hamiltonian(cls, k_sample, hamiltonian, overlap = None, momentum_operator = None,
                         degeneracy = 2, zero_filling=0, density=0, temperature=0):
        return cls(k_sample = k_sample, hamiltonian = hamiltonian, overlap = overlap, momentum_operator = momentum_operator,
            degeneracy = degeneracy, zero_filling = zero_filling, density =  density , temperature = temperature)
########################################################################






def _compute_density(chemical_potential, temperature, energies, distribution_function, 
                    degeneracy, unit_cell_volume, weights, zero_filling):

    return(degeneracy / unit_cell_volume *
           (np.dot(np.sum(distribution_function(energies - chemical_potential, temperature), axis = 0), weights)
            - zero_filling))

def _compute_chemical_potential(density, temperature, energies, distribution_function, 
                               degeneracy, unit_cell_volume, weights, zero_filling):
    n_bands = energies.shape[0]
    density_min = - zero_filling * degeneracy / unit_cell_volume
    density_max = density_min + n_bands * degeneracy / unit_cell_volume
    energy_min = np.amin(energies)
    energy_max = np.amax(energies)
    if density > density_min and density < density_max:
        try:
            return root_scalar(lambda mu, *args : _compute_density(mu, *args) - density,
                                args = (temperature, energies, distribution_function, 
                                        degeneracy, unit_cell_volume, weights, zero_filling),
                                bracket = [energy_min - 5. * temperature, 
                                            energy_max + 5. * temperature]).root
        except:
            try:
                warnings.warn('bracketing failed, fallback to secant method')
                return root_scalar(lambda mu, *args : _compute_density(mu, *args) - density,
                                    args = (temperature, energies, distribution_function, 
                                            degeneracy, unit_cell_volume, weights, zero_filling),
                                    x0 = energy_min, 
                                    x1 = energy_max).root
            except:
                warnings.warn('failed to calculate chemical potential')
                return np.nan
    elif density == density_min and temperature == 0.:
        return energy_min
    elif density == density_min:
        return -np.inf
    elif density == density_max and temperature == 0.:
        return energy_max
    elif density == density_max:
        return np.inf
    else:
        warnings.warn('density value out of range')
        return np.nan