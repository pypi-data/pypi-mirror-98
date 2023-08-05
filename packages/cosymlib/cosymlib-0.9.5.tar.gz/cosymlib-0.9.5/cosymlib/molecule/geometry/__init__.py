from cosymlib import shape, tools
from cosymlib.symmetry import Symmetry
from cosymlib.symmetry.pointgroup import PointGroup
from cosymlib.tools import generate_connectivity_from_geometry
import numpy as np
from functools import wraps


def set_parameters(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args[0]._symmetry.set_parameters(kwargs)
        return func(*args, **kwargs)
    return wrapper


class Geometry:
    """
    Main geometry class

    :param positions: Cartesian coordinates
    :type positions: list
    :param symbols: Atomic elements symbols
    :type symbols: list
    :param name: Geometry name
    :type name: str
    :param connectivity: Connectivity list
    :type connectivity: list
    :param connectivity_thresh: Connectivity threshold
    :type connectivity_thresh: float

    :example:

    .. code-block:: python

        water = Geometry(positions=[[0.0, 0.0, 0.0],
                                    [0.0, 1.0, 0.0],
                                    [0.0, 0.0, 1.0],
                         symbols=['O', 'H', 'H'],
                         name='water molecule',
                         connectivity=[[1, 2], [1, 3]])


    """
    def __init__(self,
                 positions,
                 symbols=(),
                 name='',
                 connectivity=None,
                 connectivity_thresh=1.2):

        # self._central_atom = None
        self._symbols = []
        self._positions = []
        self._atom_groups = list(symbols)
        self._name = name

# TODO: This is a mess!
        for symbol in symbols:
            try:
                int(symbol)
                self._symbols.append(tools.atomic_number_to_element(int(symbol)))
            except (ValueError, TypeError):
                self._symbols.append(symbol.capitalize())
                for ida, a in enumerate(symbol):
                    try:
                        int(a)
                        self._symbols[-1] = self._symbols[-1][:ida]
                        break
                    except (ValueError, TypeError, IndexError):
                        pass

        try:
            float(positions[0])
            for symbol in positions:
                self._positions.append(float(symbol))
            self._positions = list(chunks(self._positions, 3))
        except (ValueError, TypeError, IndexError):
            for symbol in positions:
                self._positions.append([float(j) for j in symbol])

        self._positions = np.array(self._positions)
        if connectivity is None:
            self._connectivity = generate_connectivity_from_geometry(self, thresh=connectivity_thresh)
        else:
            self._connectivity = connectivity

        self._shape = shape.Shape(self)
        self._symmetry = Symmetry(self)

    def __len__(self):
        return len(self._positions)

    @property
    def name(self):
        return self._name

    # TODO: 'symmetry' and 'shape' properties should be removed. Methods inside these
    # TODO: classes should be mirrored in geometry/molecule class. See get_symmetry_measure()

    @property
    def symmetry(self):
        return self._symmetry

    @property
    def shape(self):
        return self._shape

    def set_name(self, name):
        self._name = name

    def get_connectivity(self):
        """
        Get connectivity as a list of pairs of connected atoms

        :return: The connectivity
        :rtype: list
        """
        return self._connectivity

    def set_connectivity(self, connectivity):
        self._connectivity = connectivity
        self._symmetry._connectivity = connectivity

    def set_symbols(self, symbols):
        self._symbols = symbols
        self._symmetry._symbols = symbols

    def set_positions(self, central_atom=0):
        atom, self._positions = self._positions[central_atom], np.delete(self._positions, central_atom, 0)
        self._positions = np.insert(self._positions, len(self._positions), atom, axis=0)
        self._symmetry._positions= self._positions
        self._shape._positions= self._positions

    def get_positions(self):
        """
        Get the positions in Cartesian coordinates

        :return: the coordinates
        :rtype: list
        """
        return self._positions

    def get_n_atoms(self):
        """
        Get the number of atoms

        :return: number of atoms
        :rtype: int
        """
        return len(self.get_positions())

    def get_symbols(self):
        """
        Get the atomic elements symbols

        :return: the symbols
        :rtype: list
        """
        return self._symbols

    def generate_connectivity(self, thresh=1.2):
        self._connectivity = generate_connectivity_from_geometry(self, thresh=thresh)

    # Shape methods
    def get_shape_measure(self, shape_label, central_atom=0, fix_permutation=False):
        """
        Get the Shape measure

        :param shape_label: Reference shape label
        :type shape_label: str
        :param central_atom: the central atom position
        :type central_atom: int
        :param fix_permutation: Do not permute atoms
        :type fix_permutation: bool
        :return: The measure
        :rtype: float
        """
        return self._shape.measure(shape_label, central_atom=central_atom, fix_permutation=fix_permutation)

    def get_shape_structure(self, shape_label, central_atom=0, fix_permutation=False):
        from cosymlib.molecule.geometry import Geometry
        structure_coordinates = self._shape.structure(shape_label, central_atom=central_atom, fix_permutation=fix_permutation)

        return Geometry(symbols=self.get_symbols(),
                        positions=structure_coordinates,
                        name=self.name + '_structure')

    def get_path_deviation(self, shape_label1, shape_label2, central_atom=0):
        return self._shape.path_deviation(shape_label1, shape_label2, central_atom)

    def get_generalized_coordinate(self, shape_label1, shape_label2, central_atom=0):
        return self._shape.generalized_coordinate(shape_label1, shape_label2, central_atom)

    # Symmetry methods
    @set_parameters
    def get_symmetry_measure(self, label, central_atom=0, center=None, multi=1):
        """
        Get the symmetry measure

        :param label: Symmetry point group
        :type label: str
        :param central_atom: central atom position (0 if no central atom)
        :type central_atom: int
        :param center: center of the measure in Cartesian coordinates
        :type center: list
        :return: The symmetry measure
        :rtype: float
        """

        return self._symmetry.measure(label)

    @set_parameters
    def get_symmetry_nearest_structure(self, label, central_atom=0, center=None,  multi=1):
        """
        Returns the nearest ideal structure

        :param label: symmetry point group
        :type label: str
        :param central_atom: central atom position (0 if no central atom)
        :type central_atom: int
        :param center: center of the measure in Cartesian coordinates
        :type center: list
        :return: The structure
        :rtype: Geometry
        """
        return Geometry(symbols=self.get_symbols(),
                        positions=self._symmetry.nearest_structure(label),
                        name=self.name + '_nearest')
        # return self._symmetry.nearest_structure(label)

    @set_parameters
    def get_symmetry_optimum_axis(self, label, central_atom=0, center=None):
        return self._symmetry.optimum_axis(label)

    def get_pointgroup(self, tol=0.01):
        """
        Get the symmetry point group
        :param tol: The tolerance
        :type tol: float
        :return: The point group
        :rtype: str
        """
        return PointGroup(self, tolerance=tol).get_point_group()


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]
