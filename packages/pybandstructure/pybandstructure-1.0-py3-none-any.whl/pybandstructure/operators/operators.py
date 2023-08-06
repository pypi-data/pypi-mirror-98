import numpy as np

from scipy.linalg import eigh
from numpy.linalg import multi_dot
import warnings
from tqdm import tqdm
import copy

from pybandstructure.common import *
class Momentum_Conserving_Operator():
    """[summary]
    """    

    def __init__(self, matrices, coefficients, collapse = True, hermitian = True):
        """[summary]

        Parameters
        ----------
        matrices : [type]
            [description]
        coefficients : [type]
            [description]
        collapse : bool, optional
            [description], by default True

        Raises
        ------
        TypeError
            [description]
        """        
        self.matrices = copy.deepcopy(matrices)
        self.coefficients = copy.deepcopy(coefficients)
        self.hermitian = hermitian
        self.n_terms = len(matrices)
        if self.n_terms == 0:
            self.size = 0
        else:
            if type(matrices[0]) == np.ndarray:
                self.size = matrices[0].shape[0]
            elif type(matrices[0]) == list:
                self.size = matrices[0][0].shape[0]
        #checks
        assert type(self.matrices) == list
        assert type(self.coefficients) == list
        assert len(self.coefficients) == self.n_terms
        for i,M in enumerate(self.matrices):
            if type(M) == np.ndarray:
                assert M.shape == (self.size, self.size)
                assert callable(self.coefficients[i]) or isinstance(self.coefficients[i],(int, float, complex))
            elif type(M) == list:
                assert  callable(self.coefficients[i]) or len(self.coefficients[i]) == len(M)
                for Mj in M:
                    assert Mj.shape == (self.size, self.size)
            else:
                raise TypeError('matrices must be ndarrays or lists of ndarrays')
        if collapse:
            self.collapse_constant_coefficients()

    def __call__(self, k):
        """[summary]

        Parameters
        ----------
        k : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """        
        matrix = np.zeros([self.size,self.size], dtype = complex)
        for i in range(self.n_terms):
            if type(self.matrices[i]) == np.ndarray:
                if callable(self.coefficients[i]):
                    matrix += self.coefficients[i](k) * self.matrices[i]
                else:
                    matrix += self.coefficients[i] * self.matrices[i]
            elif type(self.matrices[i]) == list:
                if callable(self.coefficients[i]):
                    coeff = self.coefficients[i](k)
                else:
                    coeff = self.coefficients[i]
                matrix += np.sum([coeff[j] * mat for j, mat in enumerate(self.matrices[i])], axis=0)
            else:
                pass
        return matrix

    def collapse_constant_coefficients(self):
        """[summary]
        """        
        constant_matrix = np.zeros([self.size,self.size], dtype = complex)
        constant_coefficients = []
        for i, f in enumerate(self.coefficients):
            if not callable(f):
                constant_coefficients.append(i)
                if type(self.matrices[i]) == np.ndarray:
                    constant_matrix += f * self.matrices[i]
                elif type(self.matrices[i]) == list:
                    constant_matrix += np.sum([f[j] * mat for j, mat in enumerate(self.matrices[i])], axis=0)
                else:
                    pass
        for index in constant_coefficients[::-1]:
            del self.coefficients[index]
            del self.matrices[index]
        if not np.allclose(constant_matrix, 0.):
            self.coefficients.append(1.)
            self.matrices.append(constant_matrix)
        self.n_terms = len(self.matrices)

    def flatten(self):
        """[summary]
        """        
        for i, m in enumerate(self.matrices):
            if type(m) == list:
                if callable(self.coefficients[i]):
                    coefficient_list = split_function(self.coefficients[i], len(m))
                else:
                    coefficient_list = self.coefficients[i]
                del self.matrices[i]
                del self.coefficients[i]
                self.matrices[i:i] = m
                self.coefficients[i:i] = coefficient_list

    def diagonalize(self, k, overlap = None, eigvals = None):
        """[summary]

        Parameters
        ----------
        k : [type]
            [description]
        overlap : [type], optional
            [description], by default None
        eigvals : [type], optional
            [description], by default None

        Returns
        -------
        [type]
            [description]
        """        
        if self.hermitian:
    
            if overlap is None:
                return eigh(self.__call__(k), check_finite = False, eigvals=eigvals)
            else:
                return eigh(self.__call__(k), overlap(k), check_finite = False, eigvals=eigvals)
        
        else:
            if overlap is None:
                return eig(self.__call__(k), check_finite = False, eigvals=eigvals)
            else:
                return eig(self.__call__(k), overlap(k), check_finite = False, eigvals=eigvals)

    def compute_matrix_elements(self, k_points, wavefunctions, wavefunctions2 = None):
        """[summary]

        Parameters
        ----------
        k_points : [type]
            [description]
        wavefunctions : [type]
            [description]
        wavefunction2 : [type], optional
            [description], by default None

        Returns
        -------
        [type]
            [description]
        """        
        k_points = np.array(k_points, dtype = float)
        n_k_points = k_points.shape[0]
        n_bands = wavefunctions.shape[1]
        #handle wavefunctions_2 absent
        if wavefunctions2 is None:
            wavefunctions2 = wavefunctions
        #array to store the results
        op_array = np.zeros([n_bands, n_bands, n_k_points], dtype = complex)
        try:
            k_iter = enumerate(tqdm(k_points))
        except:
            warnings.warn('progressbar not available')
            k_iter = enumerate(k_points)
        #except:
        #    warnings.warn('progressbar not available')
        #    k_iter = enumerate(k_points)
        for i, k in k_iter:
            op_array[:,:,i] = multi_dot([np.conj(wavefunctions[:,:,i].T),
                                        self.__call__(k), wavefunctions2[:,:,i]])
        return op_array

    def __add__(self, other):
        """[summary]

        Parameters
        ----------
        other : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """        
        if isinstance(other, Momentum_Conserving_Operator):
            return Momentum_Conserving_Operator(self.matrices + other.matrices,
                                                self.coefficients + other.coefficients)
        elif isinstance(other,  (int, float, complex)):
            return Momentum_Conserving_Operator(self.matrices + [np.identity(self.size, dtype=complex)],
                                                self.coefficients + [other])
    def __radd__(self, other):
        return self.__add__(other)
    def __mul__(self, other):
        """[summary]

        Parameters
        ----------
        other : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """        
        if isinstance(other, (int, float, complex)):
            coefficients_result = []
            for f in self.coefficients:
                if callable(f):
                    coefficients_result.append(multiply_function_scalar(f, other))
                else:
                    coefficients_result.append(f * other)
            return Momentum_Conserving_Operator(self.matrices, coefficients_result)
        else:
            print('only multiplication by scalar')

    def __rmul__(self, other):
        """[summary]

        Parameters
        ----------
        other : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """        
        return self.__mul__(other)

    def __sub__(self, other):
        """[summary]

        Parameters
        ----------
        other : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """        
        return self.__add__(-1 * other)

    def __pos__(self):
        """[summary]

        Returns
        -------
        [type]
            [description]
        """        
        return self

    def __neg__(self):
        """[summary]

        Returns
        -------
        [type]
            [description]
        """        
        return self.__mul__(-1)

    def __gt__(self, other): self._illegal('>')
    def __ge__(self, other): self._illegal('>=')
    def __lt__(self, other): self._illegal('<')
    def __le__(self, other): self._illegal('<=')
    def __pow__(self, other): self._not_implemented('**')

    def _illegal(self, operation):
        print('illegal operation "{:s}" for operators'.format(operation))
    def _not_implemented(self, operation):
        print('operation "{:s}" is not implemented for operators'.format(operation))

# class Generic_Operator():
#     def __init__(self, matrices, coefficients):
#         self.matrices = copy.deepcopy(matrices)
#         self.coefficients = copy.deepcopy(coefficients)
#         self.size = matrices[0].shape[0]
#         self.n_terms = len(matrices)

#     def __call__(self, k, q):
#         matrix = np.zeros([self.size,self.size], dtype = complex)
#         for i in range(self.n_terms):
#             matrix += self.matrices[i] * self.coefficients[i](k, q)
#         return matrix

#     def compute_matrix_elements(self, k_sample, q_sample, wavefunctions):
#         n_k_points = len(k_sample)
#         n_q_points = len(q_sample)
#         n_bands = wavefunctions.shape[1]
#         op_array = np.zeros([n_bands, n_bands, n_k_points, n_q_points], dtype = complex)

#         for i in range(n_k_points):
#             for j in range(n_q_points):
#                 k = k_sample.coords[i]
#                 q = q_sample.coords[j]
#                 index, operation, integer_part = k_sample(tsum(k_sample[i], q_sample[j]))
#                 op_array[:,:,i,j] = multi_dot([np.conj(wavefunctions[:,:,i].T),self.__call__(k,q), wavefunctions[:,:,index]])
#         return op_array




