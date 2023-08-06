 #import modules
import numpy as np
import numpy.linalg as lin
import warnings
from itertools import product 
import h5py
import matplotlib.pyplot as plt

from pybandstructure.geometry.point_groups import *
from pybandstructure.common import *
#class to store samples of real or reciprocal space
class Sample:
    # '''
    # Input:
    #     basis_vectors : [dimension,dimension] float array, contains translation vectors in real space. The i-th vector is basis_vectors[:,i]
    #     denominator : int or [dimension] int sequence
    #     integer_coords : [k_points, dimension] int array, contains integer coordinates of the sample points in the basis of the basis_vectors/n_sites
    # Methods:
    #     sample[(n_1, ... , n_m)] -> i  with i = index of the point with integer coordinates (n_1, ... , n_m)
    #     sample[i] -> (n_1, ... , n_m) reverse function. ## In 1D it does not fail, because (n_1, ) should be a tuple, whereas i always an int

    #     sample.get_coords((n_1, ... , n_m)) -> momentum space coordinates of the point with integer coordinates (n_1, ... , n_m)
    #     sample.get_coords(i) -> momentum space coordinates of the i-th point of the sample
    # '''  

##What about using call and get_item
####### Magic methods ##################################################
    def __init__(self, basis_vectors, denominator, integer_coords, integer_coords_to_idx = None):
        """[summary]

        Parameters
        ----------
        basis_vectors : [type]
            [description]
        denominator : [type]
            [description]
        integer_coords : [type]
            [description]
        integer_coords_to_idx : [type], optional
            [description], by default None
        """        
        self._basis_vectors = check_input_vectors(basis_vectors)
        self._space_dimension, self._lattice_dimension = self._basis_vectors.shape
        self._denominator = check_denominator(self._lattice_dimension, denominator)
        self._integer_coords = np.atleast_2d(np.array(integer_coords, dtype = np.int32))
        assert self._integer_coords.ndim == 2, "Wrong input for integer_coords: it must have two dimension"
        assert self._integer_coords.shape[1] == self._lattice_dimension, "Wrong input for integer_coords: the number of columns should be equal to the dimension of the model"
        if integer_coords_to_idx is None:
            self._integer_coords_to_idx = self._build_dict(integer_coords)
        else:
            self._integer_coords_to_idx = integer_coords_to_idx 
        self._coords = np.transpose(self._basis_vectors @ np.transpose(self._integer_coords/self._denominator))

    def __getitem__(self, key):
        """[summary]

        Parameters
        ----------
        key : [type]
            [description]

        Returns
        -------
        [type]
            [description]

        Raises
        ------
        ValueError
            [description]
        """        
        if isinstance(key, tuple) and len(key) == self._lattice_dimension and all(isinstance(n,(int, np.integer)) for n in key):
            return self._integer_coords_to_idx[key] 
        elif isinstance(key, (int, np.integer)) or (len(key) == 1 and isinstance(key[0], (int, np.integer))):
            return tuple(self.integer_coords[key])
        else:
            raise ValueError("Given Key should be a tuple of ints or a single int") 

    def __contains__(self,key):
        """[summary]

        Parameters
        ----------
        key : [type]
            [description]

        Returns
        -------
        [type]
            [description]

        Raises
        ------
        ValueError
            [description]
        """        
        if isinstance(key, tuple) and len(key) == self._lattice_dimension and all(isinstance(n,(int, np.integer)) for n in key):
            return key in self._integer_coords_to_idx
        elif isinstance(key, (int, np.integer)) or (len(key) == 1 and isinstance(key[0], (int, np.integer))):
            return key < self.__len__()
        else:
            raise ValueError("Given Key should be a tuple of ints or a single int")

    def __len__(self):
        """[summary]

        Returns
        -------
        [type]
            [description]
        """        
        return self._integer_coords.shape[0]

######## Properties ####################################################
    @property
    def basis_vectors(self):
        return self._basis_vectors
    @basis_vectors.setter
    def basis_vectors(self, _):
        raise PermissionError("Sample is read only")
    @property
    def space_dimension(self):
        return self._space_dimension
    @space_dimension.setter
    def space_dimension(self, _):
        raise PermissionError("Sample is read only")
    @property
    def lattice_dimension(self):
        return self._lattice_dimension
    @lattice_dimension.setter
    def lattice_dimension(self, _):
        raise PermissionError("Sample is read only")
    @property
    def denominator(self):
        return self._denominator
    @denominator.setter
    def denominator(self, _):
        raise PermissionError("Sample is read only")
    @property
    def integer_coords(self):
        return self._integer_coords
    @integer_coords.setter
    def integer_coords(self, _):
        raise PermissionError("Sample is read only")
    @property
    def coords(self):
        return self._coords
    @coords.setter
    def coords(self, _):
        raise PermissionError("Sample is read only")

###### public methods ##################################################

    def get_integer_part(self, key):
        """[summary]

        Parameters
        ----------
        key : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """        
        return self._get_integer_part(key, self.denominator)
        
    def get_fractional_part(self, key):
        """[summary]

        Parameters
        ----------
        key : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """        
        return self._get_fractional_part(key, self.denominator)
 
    def get_coords(self, key):
        """[summary]

        Parameters
        ----------
        key : [type]
            [description]

        Returns
        -------
        [type]
            [description]

        Raises
        ------
        ValueError
            [description]
        """        
        if isinstance(key, tuple) and len(key) == self._lattice_dimension and all(isinstance(n,(int, np.integer)) for n in key):
            index = self._integer_coords_to_idx[key]
            return self._coords[index]
        elif isinstance(key, (int, np.integer)) or (len(key) == 1 and isinstance(key[0], (int, np.integer))): #dont understand second condition
            return self._coords[key]
        else:
            raise ValueError("Given Key should be a tuple of ints or a single int")

    def save(self, file_name, sample_name, file_format = 'hdf5'):
        """[summary]

        Parameters
        ----------
        file_name : [type]
            [description]
        sample_name : [type]
            [description]
        file_format : str, optional
            [description], by default 'hdf5'
        """        
        if file_format == 'hdf5':
            with h5py.File(file_name, 'a') as file_to_write:
                #sample = file_to_write.create_group(sample_name)
                file_to_write[sample_name + '/basis_vectors'] = self._basis_vectors
                file_to_write[sample_name +'/denominator'] = self._denominator
                file_to_write[sample_name +'/integer_coords'] = self._integer_coords
                file_to_write[sample_name +'/idx_keys'] = np.array(list(self._integer_coords_to_idx.keys()))
                file_to_write[sample_name + '/idx_values'] = np.array(list(self._integer_coords_to_idx.values()))
        else:
            warn('invalid file_format')

    def plot(self, **kwargs):
        """[summary]

        Raises
        ------
        NotImplementedError
            [description]
        """        
        if self._lattice_dimension == 1:
            p1 = plt.plot(self._coords[:,0], np.zeros_like(self._coords[:,0]), 'o', **kwargs)
            v = self._basis_vectors[:,0]
            v_origin = np.vstack(([0,0],v))
            p2 = plt.plot(v_origin[:,0], v_origin[:,1], 'r-')
            return p1, p2
        elif self._lattice_dimension == 2:
            p1 = plt.plot(self._coords[:,0], self._coords[:,1], 'o', **kwargs)
            for i in range(2):
                v = self._basis_vectors[:,i]
                v_origin = np.vstack(([0,0],v))
                p2 = plt.plot(v_origin[:,0], v_origin[:,1], 'r-')
            plt.axis("equal")
            return p1, p2
        else:
            raise NotImplementedError("3D plot sample not yet implemented.")



    def contour(self, point_list):
        """[summary]

        Parameters
        ----------
        point_list : [type]
            [description]

        Returns
        -------
        [type]
            [description]

        Raises
        ------
        ValueError
            [description]
        """        
        point_list_tuples = []
        for p in point_list:
            if isinstance(p, tuple) and len(p) == self._lattice_dimension and all(isinstance(n,(int, np.integer)) for n in p):
                point_list_tuples.append(p)
            elif isinstance(p, (int, np.integer)) or (len(p) == 1 and isinstance(p[0], (int, np.integer))):
                point_list_tuples.append(self[p])
            else:
                raise ValueError("Given Key should be a tuple of ints or a single int")
        cont = []
        distances = []
        points = [0]
        for i in range(len(point_list)-1):
            pts = self.points_on_line(point_list_tuples[i],point_list_tuples[i+1])
            points.append(len(pts))
            cont += pts 
            l = tdiv(tdif(point_list_tuples[i],point_list_tuples[i+1]), self.denominator)
            distances.append(lin.norm(self.basis_vectors @ l)/len(pts)*np.ones([len(pts)]))
        cont += self.points_on_line(point_list_tuples[-1], point_list_tuples[-1])
        points = np.cumsum(points)
        x = np.concatenate(([0.], np.cumsum(np.concatenate(distances))))
        index = []
        for key in cont:
            ii = self[key]
            if type(ii) == tuple: 
                index.append(ii[0])
            else:
                index.append(ii)
        index = np.array(index,dtype = int)
        return index, x, points

################## Constructors ########################################

    @classmethod
    def sample(cls, basis_vectors, denominator, integer_coords):
        return cls(basis_vectors, denominator, integer_coords)

    @classmethod
    def from_file(cls, file_name, sample_name, file_format = 'hdf5'):
        if file_format == 'hdf5':
            with h5py.File(file_name, 'r') as file_to_read:
                #sample = file_to_write.create_group(sample_name)
                basis_vectors = file_to_read[sample_name + '/basis_vectors'][...]
                denominator = file_to_read[sample_name +'/denominator'][...]
                integer_coords = file_to_read[sample_name +'/integer_coords'][...]
                idx_keys = file_to_read[sample_name +'/idx_keys'][...]
                idx_values = file_to_read[sample_name + '/idx_values'][...]
                integer_coords_to_idx = {}
                for i, key in enumerate(idx_keys):
                    integer_coords_to_idx[tuple(key)] = idx_values[i]
        else:
            warn('invalid file_format')

        return cls(basis_vectors, denominator, integer_coords, integer_coords_to_idx = integer_coords_to_idx)

    @classmethod
    def lattice_sample(cls, basis_vectors, cut_off):
        """[summary]

        Parameters
        ----------
        basis_vectors : [type]
            [description]
        cut_off : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """        
        basis_vectors = check_input_vectors(basis_vectors)
        space_dimension, lattice_dimension = basis_vectors.shape
        M = basis_vectors.T @ basis_vectors
        M_inv = lin.inv(M)
        n_max = [int(np.ceil(cut_off * np.sqrt(M_inv[i,i]))) for i in range(lattice_dimension)]
        integer_coords = []
        iter = product(*[range(-n,n+1,1) for n in n_max])
        for x in iter:
            if lin.multi_dot([x, M, x]) <= cut_off**2:
                integer_coords.append(x)
        integer_coords.sort(key = lambda x : lin.multi_dot([x, M, x]))
        return cls(basis_vectors = basis_vectors, 
                   denominator = 1, 
                   integer_coords = integer_coords)

    @classmethod
    def line_sample(cls, basis_vectors, cut_off):
        """[summary]

        Parameters
        ----------
        basis_vectors : [type]
            [description]
        cut_off : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """        
        basis_vectors = check_input_vectors(basis_vectors)
        space_dimension, lattice_dimension = basis_vectors.shape
        #create integer coords
        n_max = int(np.floor(cut_off / lin.norm(basis_vectors[:,0])))
        integer_coords = np.zeros([2 * n_max + 1, lattice_dimension], dtype= int)
        integer_coords[:,0] = np.arange(-n_max, n_max +1, dtype=int)
        return cls(basis_vectors = basis_vectors, 
                   denominator = 1, 
                   integer_coords = integer_coords)

######### Private methods ######################################################

    @classmethod
    def _build_dict(cls, integer_coords):
        dict_ = {}
        for i,key in enumerate(integer_coords):
            dict_[tuple(key)] = i
        return dict_
    
    @classmethod
    def _get_integer_part(cls, key, denominator):
        return tuple([key[i]//denominator[i] for i in range(len(denominator))])

    @classmethod
    def _get_fractional_part(cls, key, denominator):
        return tuple([key[i] % denominator[i] for i in range(len(denominator))])

    @staticmethod
    def points_on_line(p1, p2):
        dimension = len(p1)
        if len(p2)!= dimension:
            raise ValueError('Non-matching dimensions')
        #if not all([type(a)==int for a in p1+p2]):
        #    raise TypeError('Integers required')
        dist = [p2[i]-p1[i] for i in range(dimension)]
        div=np.gcd.reduce(dist)
        if div !=0:
            #wrong
            return [tuple([p1[j]+ i*dist[j]//div for j in range(dimension)]) for i in range(div)]
        else:
            return [tuple([p1[j] for j in range(dimension)])]

################################################################################
################################################################################

#basic class for unit cell sampling
class Unit_Cell_Sample(Sample):

    def __init__(self, basis_vectors, denominator, integer_coords, integer_coords_to_idx, weights, cell_volume = None, special_points = {}):
        Sample.__init__(self, 
                        basis_vectors = basis_vectors, 
                        denominator = denominator, 
                        integer_coords = integer_coords,
                        integer_coords_to_idx = integer_coords_to_idx)
        assert np.allclose(np.sum(weights),1) 
        assert len(weights) == len(integer_coords)
        self._weights = weights
        if cell_volume is None:
            self._cell_volume = np.abs(lin.det(self.basis_vectors[:self.lattice_dimension,:]))
        else:
            self._cell_volume = cell_volume
        assert type(special_points) == dict
        self._special_points = special_points

    def __getitem__(self, key):
        if isinstance(key, tuple) and len(key) == self._lattice_dimension and all(isinstance(n,(int, np.integer)) for n in key):
            integer_part = self.get_integer_part(key)
            fractional_part = self.get_fractional_part(key)
            index, operation = self._integer_coords_to_idx[fractional_part]
            return index, operation, integer_part

        elif isinstance(key, (int, np.integer)) or (len(key) == 1 and isinstance(key[0], (int, np.integer))):
            return tuple(self.integer_coords[key])

        elif isinstance(key, str):
            fractional_part = self.get_fractional_part(self._special_points[key])
            index, operation = self._integer_coords_to_idx[fractional_part]
            return index

        else:
            raise ValueError("Given Key should be a tuple of ints or a single int") 
    
    def get_coords(self, key):
        if isinstance(key, tuple) and len(key) == self._lattice_dimension and all(isinstance(n,(int, np.integer)) for n in key):
            fractional_part = self.get_fractional_part(key)
            index = self._integer_coords_to_idx[fractional_part][0]
            return self._coords[index]
        elif isinstance(key, (int, np.integer)) or (len(key) == 1 and isinstance(key[0], (int, np.integer))):
            return self._coords[key]
        elif isinstance(key, str):
            fractional_part = self.get_fractional_part(self._special_points[key])
            index, operation = self._integer_coords_to_idx[fractional_part]
            return self._coords[index]
        else:
            raise ValueError("Given Key should be a tuple of ints or a single int")

    def save(self, file_name, sample_name, file_format = 'hdf5'):
        Sample.save(self, file_name, sample_name, file_format)
        if file_format == 'hdf5':
            with h5py.File(file_name, 'a') as file_to_write:
                #sample = file_to_write.create_group(sample_name)
                file_to_write[sample_name + '/weights'] = self._weights
                dt = h5py.special_dtype(vlen=str)
                file_to_write[sample_name +'/special_points_keys'] = np.array(list(self._special_points.keys()),dtype=dt)
                file_to_write[sample_name + '/special_points_values'] = np.array(list(self._special_points.values()))
        else:
            warn('invalid file_format')

    @property
    def weights(self):
        return self._weights
    @weights.setter
    def weights(self, _):
        raise PermissionError("Sample is read only")
    
    @property
    def cell_volume(self):
        return self._cell_volume
    @cell_volume.setter
    def cell_volume(self, _):
        raise PermissionError("Sample is read only")

    @property
    def special_points(self):
        return self._special_points
    @special_points.setter
    def special_points(self, _):
        raise PermissionError("Sample is read only")

    @classmethod
    def _build_dict(cls, denominator, integer_coords, symmetry_repr):
        dict_ = {}
        for g in range(symmetry_repr.shape[0]-1,-1,-1):
            for i,key in enumerate(integer_coords):
                #careful with transpose
                vector = symmetry_repr[g,:,:].T @ np.array(key, dtype = int)
                dict_[cls._get_fractional_part(vector, denominator)] = i, g 
        return dict_

    @classmethod
    def _build_weights(cls, denominator, integer_coords, integer_coords_to_idx):
        integration_weights = np.zeros([len(integer_coords)], dtype = float)
        standard_bz = product(*[range(den) for den in denominator])
        for k in standard_bz:
            integration_weights[integer_coords_to_idx[k][0]] += 1
        return integration_weights / np.prod(denominator)

    def contour(self, point_list):
        point_list2 = []
        for point in point_list:
            if type(point) == str:
                point_list2.append(self._special_points[point])
            else:
                point_list2.append(point)
        return Sample.contour(self, point_list2)

    def integrate(self, array, axis):
        return self._cell_volume * np.tensordot(array,
                                                self._weights,
                                                axes = (axis,0))

######### constructors #################################################
    @classmethod
    def from_file(cls, file_name, sample_name, file_format = 'hdf5'):
        if file_format == 'hdf5':
            with h5py.File(file_name, 'r') as file_to_read:
                #sample = file_to_write.create_group(sample_name)
                basis_vectors = file_to_read[sample_name + '/basis_vectors'][...]
                denominator = file_to_read[sample_name +'/denominator'][...]
                integer_coords = file_to_read[sample_name +'/integer_coords'][...]
                idx_keys = file_to_read[sample_name +'/idx_keys'][...]
                idx_values = file_to_read[sample_name + '/idx_values'][...]
                integer_coords_to_idx = {}
                for i, key in enumerate(idx_keys):
                    integer_coords_to_idx[tuple(key)] = tuple(idx_values[i])
                weights = file_to_read[sample_name + '/weights'][...]
                special_points_keys = file_to_read[sample_name +'/special_points_keys'][...]
                special_points_values = file_to_read[sample_name + '/special_points_values'][...]
                special_points = {}
                for i, key in enumerate(special_points_keys):
                    special_points[str(key)] = tuple(special_points_values[i])
        else:
            warn('invalid file_format')

        return cls(basis_vectors = basis_vectors,
                   denominator =  denominator, 
                   integer_coords = integer_coords, 
                   integer_coords_to_idx = integer_coords_to_idx, 
                   weights = weights, 
                   special_points = special_points)
    @classmethod 
    def from_point_group(cls, basis_vectors, denominator, integer_coords, point_group = None, special_points = {}):
        if point_group is None:
            basis_vectors = check_input_vectors(basis_vectors)
            point_group = Point_Group(space_dimension = basis_vectors.shape[0])
        assert isinstance(point_group, Point_Group)
        assert type(special_points) == dict
        symmetry_repr = point_group.integer_representation(basis_vectors)
        integer_coords_to_idx = cls._build_dict(denominator, integer_coords, symmetry_repr)
        weights = cls._build_weights(denominator, integer_coords, integer_coords_to_idx)
        return cls(basis_vectors = basis_vectors,
            denominator =  denominator, 
            integer_coords = integer_coords, 
            integer_coords_to_idx = integer_coords_to_idx, 
            weights = weights, 
            special_points = special_points)
        return cls(basis_vectors, denominator, integer_coords, integer_coords_to_idx, weights, special_points)

    @classmethod
    def default_unit_cell(cls, basis_vectors, denominator):
        basis_vectors = check_input_vectors(basis_vectors)
        space_dimension, lattice_dimension = basis_vectors.shape
        denominator = check_denominator(lattice_dimension, denominator)
        arrs = np.meshgrid(*[np.arange(den) for den in denominator])
        integer_coords = np.stack([arr.flatten() for arr in arrs], axis = -1)
        integer_coords_to_idx = {}
        for i,key in enumerate(integer_coords):
            integer_coords_to_idx[tuple(key)] = i, 0
        weights = np.ones(len(integer_coords))/np.prod(denominator)
        special_points = {'$\Gamma$' : 0}
        return cls(basis_vectors = basis_vectors,
                   denominator =  denominator, 
                   integer_coords = integer_coords, 
                   integer_coords_to_idx = integer_coords_to_idx, 
                   weights = weights, 
                   special_points = special_points)

    @classmethod
    def centered_unit_cell(cls, basis_vectors, denominator):
        basis_vectors = check_input_vectors(basis_vectors)
        space_dimension, lattice_dimension = basis_vectors.shape
        denominator = check_denominator(lattice_dimension, denominator)
        arrs = np.meshgrid(*[np.arange(-(den//2), den//2 + den % 2) for den in denominator])
        integer_coords = np.stack([arr.flatten() for arr in arrs], axis = -1)
        integer_coords_to_idx = {}
        for i,key in enumerate(integer_coords):
            integer_coords_to_idx[tuple(key)] = i, 0
        weights = np.ones(len(integer_coords))/np.prod(denominator)
        for i,v in enumerate(integer_coords):
            if np.all(v==0):
                gamma_index = i
        special_points = {'$\Gamma$' :  gamma_index}
        return cls(basis_vectors = basis_vectors,
                   denominator =  denominator, 
                   integer_coords = integer_coords, 
                   integer_coords_to_idx = integer_coords_to_idx, 
                   weights = weights, 
                   special_points = special_points)

    @classmethod
    def centered_square_sample(cls, basis_vectors, denominator):
        basis_vectors = check_input_vectors(basis_vectors)
        space_dimension, lattice_dimension = basis_vectors.shape
        denominator = check_denominator(lattice_dimension, denominator)
        assert lattice_dimension == 2
        assert space_dimension ==2
        assert all(ni == denominator[0] for ni in denominator)
        assert denominator[0] % 2 == 1
        assert np.allclose(lin.norm(basis_vectors[:,0]), lin.norm(basis_vectors[:,1]))
        assert np.allclose(np.dot(basis_vectors[:,0], basis_vectors[:,1]), 0.)
        #create integer coords
        arrs = np.meshgrid(*[np.arange(-(den//2) , den//2 + 1) for den in denominator])
        integer_coords = np.stack([arr.flatten() for arr in arrs], axis = -1)
        integer_coords_to_idx = {}
        for i,key in enumerate(integer_coords):
            integer_coords_to_idx[tuple(key)] = i, 0
        weights = np.ones(len(integer_coords))/len(integer_coords)
        #create special points
        for i,v in enumerate(integer_coords):
            if np.all(v==0):
                gamma_index = i
        special_points = {'$\Gamma$' :  gamma_index}
        return cls(basis_vectors = basis_vectors,
                   denominator =  denominator, 
                   integer_coords = integer_coords, 
                   integer_coords_to_idx = integer_coords_to_idx, 
                   weights = weights, 
                   special_points = special_points)
    
    @classmethod 
    def irreducible_sample(cls, name, basis_vectors, denominator):
        basis_vectors = check_input_vectors(basis_vectors)
        space_dimension, lattice_dimension = basis_vectors.shape
        denominator = check_denominator(lattice_dimension, denominator)

        if name == '2D_Hexagonal_D6':
            assert lattice_dimension == 2
            assert space_dimension ==2
            assert all(ni == denominator[0] for ni in denominator)
            assert denominator[0] % 6 == 0
            assert np.allclose(lin.norm(basis_vectors[:,0]), lin.norm(basis_vectors[:,1]))
            if np.allclose(np.dot(basis_vectors[:,0], basis_vectors[:,1]), 0.5 * lin.norm(basis_vectors[:,0])**2):
                wide_angle = False
            elif np.allclose(np.dot(basis_vectors[:,0], basis_vectors[:,1]),- 0.5 * lin.norm(basis_vectors[:,0])**2):
                wide_angle = True
            else:
                raise ValueError('vectors not compatible with hexagonal symmetry')
            #create integer coords
            N = denominator[0] 
            #These are valid if wide_config == False
            v1 = np.array(np.concatenate([np.arange(j,N/2+1-np.ceil(j/2),dtype =int) for j in range(N//3+1)]), dtype=np.int32)
            v2 = np.array(np.concatenate([j*np.ones(int(N/2+1-np.ceil(j/2)-j),dtype=int) for j in range(N//3+1)]), dtype=np.int32)
            #If wide_config = True (p, q) -> (p + q, q)
            if wide_angle:
                v1 += v2
            integer_coords = np.column_stack([v1, v2])
            #set point group and special points
            point_group = D6_2D(theta0 = np.arctan2(basis_vectors[1,0], basis_vectors[0,0]))
            special_points = {'$\Gamma$' : (0,0)}
            if wide_angle:
                special_points['$M$'] = (N//2,0)
                special_points['$K$'] = (2 * N//3,N//3)
            else:
                special_points['$M$'] = (N//2,0)
                special_points['$K$'] = (N//3,N//3)
            #special_points = {'$\Gamma$' : (0,0),
            #                  '$M$' : (N//2,0),
            #                  '$K$' : (N//3,N//3)}

        elif name == '2D_Hexagonal_D3_Axes':
            #checks hexagonal
            assert lattice_dimension == 2
            assert space_dimension ==2
            assert all(ni == denominator[0] for ni in denominator)
            assert denominator[0] % 6 == 0
            assert np.allclose(lin.norm(basis_vectors[:,0]), lin.norm(basis_vectors[:,1]))
            if np.allclose(np.dot(basis_vectors[:,0], basis_vectors[:,1]), 0.5 * lin.norm(basis_vectors[:,0])**2):
                wide_angle = False
            elif np.allclose(np.dot(basis_vectors[:,0], basis_vectors[:,1]),- 0.5 * lin.norm(basis_vectors[:,0])**2):
                wide_angle = True
            else:
                raise ValueError('vectors not compatible with hexagonal symmetry')
            #create integer coords
            N = denominator[0] #Already checked to be uniform and multiple of 6 
            idx_1 = np.concatenate([np.arange(j,N/2+1-np.ceil(j/2),dtype =int) for j in range(N//3+1)])
            idx_1_nodiag = np.concatenate([np.arange(j + 1,N/2+1-np.ceil(j/2)-(j+1)%2 ,dtype =int) for j in range(N//3)])
            idx_2 = np.concatenate([j*np.ones(int(N/2+1-np.ceil(j/2)-j ),dtype=int) for j in range(N//3+1)])
            idx_2_nodiag = np.concatenate([j*np.ones(int(N/2+1-np.ceil(j/2)-j - 1-(j+1)%2),dtype=int) for j in range(N//3)])
            #There are duplicate points on the diagonal
            #These are valid if wide_config == False
            v1 = np.array(np.concatenate([idx_1, idx_2_nodiag]), dtype=np.int32)
            v2 = np.array(np.concatenate([idx_2, idx_1_nodiag]), dtype=np.int32)
            #If wide_config = True (p, q) -> (p + q, q)
            if wide_angle:
                v1 += v2
            integer_coords = np.column_stack([v1, v2])
            #set point group and special points
            point_group = D3_2D(theta0 = np.arctan2(basis_vectors[1,0], basis_vectors[0,0]))
            special_points = {'$\Gamma$' : (0,0),
                              '$M$' : (N//2,0)}
            if wide_angle:
                special_points['$M^\prime$'] = (N//2,N//2)
                special_points['$K$'] = (2 * N//3, N//3)

            else:
                special_points['$M^\prime$'] = (0,N//2)
                special_points['$K$'] = (N//3, N//3)

        elif name == '2D_Square_D4':
            #checks square
            assert lattice_dimension == 2
            assert space_dimension ==2
            assert all(ni == denominator[0] for ni in denominator)
            assert denominator[0] % 2 == 0
            assert np.allclose(lin.norm(basis_vectors[:,0]), lin.norm(basis_vectors[:,1]))
            assert np.allclose(np.dot(basis_vectors[:,0], basis_vectors[:,1]), 0.)
            #create integer coords
            N = denominator[0] #Already checked to be uniform and multiple of 6 
            v1 = np.concatenate([np.arange(j, N//2 +1, dtype = int) for j in range(N//2+1)])
            v2 = np.concatenate([j * np.ones([N//2 +1 -j], dtype = int) for j in range(N//2+1)])
            integer_coords = np.column_stack([v1, v2])
            #set point group and special points
            point_group = D4_2D(theta0 = np.arctan2(basis_vectors[1,0], basis_vectors[0,0]))
            special_points = {'$\Gamma$' : (0,0),
                              '$X$' : (N//2,0),
                              '$M$' : (N//2,N//2)}

        elif name == '2D_Rectangular_D2':
            assert lattice_dimension == 2
            assert space_dimension ==2
            assert all(ni % 2 == 0 for ni in denominator)
            assert np.allclose(np.dot(basis_vectors[:,0], basis_vectors[:,1]), 0.)
            #create integer coords        
            v1 = np.concatenate([np.arange(0, denominator[0]//2 +1, dtype = int) for j in range(denominator[1]//2+1)])
            v2 = np.concatenate([j * np.ones([denominator[0]//2 +1], dtype = int) for j in range(denominator[1]//2+1)])
            integer_coords = np.column_stack([v1, v2])
            #set point group and special points
            point_group = D2_2D(theta0 = np.arctan2(basis_vectors[1,0], basis_vectors[0,0]))
            special_points = {'$\Gamma$' : (0,0)}

        else:
            raise ValueError

        symmetry_repr = point_group.integer_representation(basis_vectors)
        integer_coords_to_idx = cls._build_dict(denominator, integer_coords, symmetry_repr)
        weights = cls._build_weights(denominator, integer_coords, integer_coords_to_idx)
        return cls(basis_vectors = basis_vectors,
                   denominator =  denominator, 
                   integer_coords = integer_coords, 
                   integer_coords_to_idx = integer_coords_to_idx, 
                   weights = weights, 
                   special_points = special_points)





'''
        
class Irreducible_BZ_Sampling(Builder):
    def __init__(self, reciprocal_vectors, n_sites, symmetry_group):
        Builder.__init__(self, reciprocal_vectors, n_sites)
        self._symmetry_group = symmetry_group
    @property
    def make(self):
        warnings.warn("Highly experimental feature")
        #Check reciprocal vectors and n_sites
        reciprocal_vectors = self.reciprocal_vectors
        n_sites = self.n_sites
        #Get integer representations on group operator, get the trasnspose because
        integer_representation = np.swapaxes(self._symmetry_group.integer_representation(reciprocal_vectors), 1,2)
        #Create auxiliary full BZ sample with no symmetry specified
        integer_coords = np.array(list(np.ndindex(n_sites)))
        sample = Sample(reciprocal_vectors,integer_coords,n_sites)
        #Transform the sample points with the symmetry group operations
        integer_transformed = np.moveaxis(integer_representation@(sample.integer_coords.T), 1,2)
        #Fold them back on the 1^st BZ
        _, integer_folded = np.divmod(integer_transformed, np.array(n_sites, dtype=np.int32))
        #Make an ndarray of ints with shape [k, R] of the index of the transformed vector q = Rk
        index_table = np.empty(integer_folded.shape[0:2], dtype=np.int)
        for pt_idx in np.ndindex(index_table.shape[0:2]):
            index_table[pt_idx] = sample[tuple(integer_folded[pt_idx])]
        index_table = index_table.T
        #Permute sample points so to be ordered according to their norm 
        norms = lin.norm(sample.points, axis = 1)
        min_dist = np.empty(len(index_table), np.int32)
        for x_idx, x in enumerate(index_table):
            temp_index_table = np.array(sorted(set(x)), np.int32)
            temp_norms = norms[temp_index_table]
            min_norm = np.argmin(temp_norms)
            min_dist[x_idx] = temp_index_table[min_norm]
        #Finally get the Irreducible BZ and integration weights
        idxs, weights = np.unique(min_dist, return_counts=True)
        return Sample(reciprocal_vectors, sample.integer_coords[idxs], n_sites, weights/np.sum(weights), self.signature)
    @property
    def signature(self):
        return self._symmetry_group.__class__.__name__ + "_Irreducible_BZ"

'''