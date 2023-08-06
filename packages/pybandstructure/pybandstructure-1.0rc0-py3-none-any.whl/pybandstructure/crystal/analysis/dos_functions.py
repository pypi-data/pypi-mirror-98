from pybandstructure.common import *

def dos(epsilon, energies, integrate_bz, eta):
    '''calculates the DOS using trapz_bz and E_matrix containing samples of
    the band energy'''
    b = np.broadcast(epsilon)
    result = [np.sum(integrate_bz(delta_function(epsilon_val - energies, eta, shape = 'lorentz'), axis = -1)) for epsilon_val in b]
    return np.array(result, dtype = float).reshape(b.shape)

def jdos(epsilon, nu, mu, energies, integrate_bz, eta):
    '''calculates the jDOS using trapz_bz and E_matrix containing samples of
    the band energy'''
    b = np.broadcast(epsilon)
    result = [integrate_bz(delta_function(epsilon_val - energies[nu,:]  + energies[mu,:], eta, shape = 'lorentz'), axis =-1)
        for epsilon_val in b]
    return np.array(result, dtype = float).reshape(b.shape )