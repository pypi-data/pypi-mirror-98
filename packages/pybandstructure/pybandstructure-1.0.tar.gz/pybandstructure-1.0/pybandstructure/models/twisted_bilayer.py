#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Twisted bilayer graphene'''
__all__ = ['koshino']
############################ Import modules ############################
import numpy as numpy
from numpy.linalg import norm

from pybandstructure.common import *
from pybandstructure.operators.operators import *
from pybandstructure.operators.superlattices import *
from pybandstructure.sample import Sample
########################################################################
class _kinetic_function():

    def __init__(self, theta, G , hv, der = (0,0)):
        self.theta = theta
        self.G = G
        self.hv = hv
        self.der = der
        s = np.sin(self.theta / 360. *np.pi)
        c = np.cos(self.theta / 360. *np.pi)
        self.R1 = np.array([[c, s],[-s,c]])
        self.R2 = np.array([[c, -s], [s,c]])
        self.K1 = self.G / np.sqrt(3) * np.array([np.sqrt(3)/2,0.5])
        self.K2 = self.G / np.sqrt(3) * np.array([np.sqrt(3)/2,-0.5])

    def __call__(self, k):
        if self.der == (0,0):
            return self.hv * np.concatenate((np.dot(self.R1, k - self.K1), np.dot(self.R2, k - self.K2)) )
        elif self.der == (1,0):
            return self.hv * np.concatenate((np.dot(self.R1, np.array([1.,0.])), np.dot(self.R2,np.array([1.,0.]))) )
        elif self.der == (0,1):
            return self.hv * np.concatenate((np.dot(self.R1,np.array([0.,1.])), np.dot(self.R2,np.array([0.,1.]))) )
        else:
            return 0.

def koshino_intralayer(theta, hv, reciprocal_lattice_vectors):
    '''Intralayer part of Koshino hamiltonian'''
    G = norm( reciprocal_lattice_vectors.basis_vectors[:,0] )
    kinetic_matrix = [np.kron(pauli_matrix('u'),-pauli_matrix('x')), np.kron(pauli_matrix('u'),pauli_matrix('y')),
                      np.kron(pauli_matrix('l'),-pauli_matrix('x')), np.kron(pauli_matrix('l'),pauli_matrix('y'))]
    H0 = Momentum_Conserving_Operator(matrices = [kinetic_matrix],
                                      coefficients = [_kinetic_function(theta = theta, G = G, hv = hv)],
                                      collapse = True)
    H0_lattice = build_kinetic_hamiltonian(H0, 
                                           reciprocal_lattice_vectors = reciprocal_lattice_vectors)
    return H0_lattice


def koshino_momentum(theta, hv, reciprocal_lattice_vectors):
    '''Momentum operators corresponding to Koshino hamiltonian'''
    G = norm( reciprocal_lattice_vectors.basis_vectors[:,0] )
    kinetic_matrix = [np.kron(pauli_matrix('u'), -pauli_matrix('x')), np.kron(pauli_matrix('u'), pauli_matrix('y')),
                      np.kron(pauli_matrix('l'), -pauli_matrix('x')), np.kron(pauli_matrix('l'), pauli_matrix('y'))]

    p_x = build_kinetic_term(kinetic_matrix, 
                             _kinetic_function(theta, G = G, hv = hv, der = (1,0)), 
                             reciprocal_lattice_vectors = reciprocal_lattice_vectors)
    p_x.collapse_constant_coefficients()
    p_y = build_kinetic_term(kinetic_matrix, 
                             _kinetic_function(theta, G = G, hv = hv,der = (0,1)), 
                             reciprocal_lattice_vectors = reciprocal_lattice_vectors)
    p_y.collapse_constant_coefficients()
    return [p_x, p_y]


def koshino_interlayer_AA(reciprocal_lattice_vectors):
    '''Interlayer part of Koshino hamiltonian (AA regions)'''
    const = np.exp(1j*2*np.pi/3)

    AA_coupling_plus = np.zeros([len(reciprocal_lattice_vectors)], dtype = complex)
    AA_coupling_minus = np.zeros([len(reciprocal_lattice_vectors)], dtype = complex)

    AA_coupling_plus[reciprocal_lattice_vectors[(0,0)]] = 1.
    AA_coupling_plus[reciprocal_lattice_vectors[(1,0)]] = 1. / const
    AA_coupling_plus[reciprocal_lattice_vectors[(0,1)]] = const
    AA_coupling_minus[reciprocal_lattice_vectors[(0,0)]] = 1.
    AA_coupling_minus[reciprocal_lattice_vectors[(-1,0)]] = const
    AA_coupling_minus[reciprocal_lattice_vectors[(0,-1)]] = 1. / const

    H_AA_plus = build_potential_hamiltonian(U = np.kron(pauli_matrix('+'), pauli_matrix('I')), 
                                            potential_components = AA_coupling_plus, 
                                            reciprocal_lattice_vectors = reciprocal_lattice_vectors)
    H_AA_minus = build_potential_hamiltonian(U = np.kron(pauli_matrix('-'), pauli_matrix('I')), 
                                            potential_components = AA_coupling_minus, 
                                            reciprocal_lattice_vectors = reciprocal_lattice_vectors)
    H_AA = H_AA_plus + H_AA_minus
    H_AA.collapse_constant_coefficients()
    return H_AA


def koshino_interlayer_AB(reciprocal_lattice_vectors):
    '''Interlayer part of Koshino hamiltonian (AB regions)'''
    const = np.exp(1j*2*np.pi/3)

    AB_coupling_plus_plus = np.zeros([len(reciprocal_lattice_vectors)], dtype = complex)
    AB_coupling_plus_minus = np.zeros([len(reciprocal_lattice_vectors)], dtype = complex)
    AB_coupling_minus_plus = np.zeros([len(reciprocal_lattice_vectors)], dtype = complex)
    AB_coupling_minus_minus = np.zeros([len(reciprocal_lattice_vectors)], dtype = complex)

    AB_coupling_plus_plus[reciprocal_lattice_vectors[(0,0)]] = 1
    AB_coupling_plus_plus[reciprocal_lattice_vectors[(1,0)]] = 1
    AB_coupling_plus_plus[reciprocal_lattice_vectors[(0,1)]] = 1

    AB_coupling_minus_minus[reciprocal_lattice_vectors[(0,0)]] = 1
    AB_coupling_minus_minus[reciprocal_lattice_vectors[(-1,0)]] = 1
    AB_coupling_minus_minus[reciprocal_lattice_vectors[(0,-1)]] = 1

    AB_coupling_plus_minus[reciprocal_lattice_vectors[(0,0)]] = 1
    AB_coupling_plus_minus[reciprocal_lattice_vectors[(1,0)]] = const
    AB_coupling_plus_minus[reciprocal_lattice_vectors[(0,1)]] = 1 / const

    AB_coupling_minus_plus[reciprocal_lattice_vectors[(0,0)]] = 1
    AB_coupling_minus_plus[reciprocal_lattice_vectors[(-1,0)]] = 1 / const
    AB_coupling_minus_plus[reciprocal_lattice_vectors[(0,-1)]] = const

    H_AB_plus_plus = build_potential_hamiltonian(U = np.kron(pauli_matrix('+'), pauli_matrix('+')), 
                                                potential_components = AB_coupling_plus_plus, 
                                                reciprocal_lattice_vectors = reciprocal_lattice_vectors)
    H_AB_minus_minus = build_potential_hamiltonian(U = np.kron(pauli_matrix('-'), pauli_matrix('-')), 
                                                potential_components = AB_coupling_minus_minus, 
                                                reciprocal_lattice_vectors = reciprocal_lattice_vectors)
    H_AB_plus_minus = build_potential_hamiltonian(U = np.kron(pauli_matrix('+'), pauli_matrix('-')), 
                                                potential_components = AB_coupling_plus_minus, 
                                                reciprocal_lattice_vectors = reciprocal_lattice_vectors)
    H_AB_minus_plus = build_potential_hamiltonian(U = np.kron(pauli_matrix('-'), pauli_matrix('+')), 
                                                potential_components = AB_coupling_minus_plus, 
                                                reciprocal_lattice_vectors = reciprocal_lattice_vectors)

    H_AB = H_AB_plus_plus + H_AB_minus_minus + H_AB_plus_minus + H_AB_minus_plus
    H_AB.collapse_constant_coefficients()
    return H_AB


def koshino(theta, u0, u1, hv, a, G_max):
    """Total hamiltonian of the Koshino model

    Parameters
    ----------
    theta : float
        twist angle in degrees
    u0 : float
        interlayer tunneling (AA)
    u1 : float
        interlayer tunneling (AB)
    hv : float
        hbar  * Dirac_velocity 
    a : float
        lattice constant of the original layer (0.246 nm in graphene)
    G_max : float
        cutoff in reciprocal lattice space in units of the reciprocal lattice constant

    Returns
    -------
    dict
        model
    """    
    G = 8. * np.pi * np.sin(theta / 360. * np.pi)/ (np.sqrt(3) * a)
    reciprocal_lattice_basis = G * np.array([[          0.5,         -0.5],
                                             [np.sqrt(3)/2.,np.sqrt(3)/2.]], dtype = float)
    reciprocal_lattice_vectors = Sample.lattice_sample(basis_vectors=reciprocal_lattice_basis, cut_off=G * G_max)
    H = (koshino_intralayer(theta, hv, reciprocal_lattice_vectors)
       + u0 * koshino_interlayer_AA(reciprocal_lattice_vectors)
       + u1 * koshino_interlayer_AB(reciprocal_lattice_vectors))
    H.collapse_constant_coefficients()
    momentum_operator = koshino_momentum(theta, hv, reciprocal_lattice_vectors)
    return {'hamiltonian' : H,
            'overlap' : None,
            'momentum_operator' : momentum_operator,
            'reciprocal_lattice_vectors' : reciprocal_lattice_vectors}