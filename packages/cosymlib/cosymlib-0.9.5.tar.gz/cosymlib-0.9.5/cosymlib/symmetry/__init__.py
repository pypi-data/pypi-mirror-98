from wfnsympy import WfnSympy
from symgroupy import Symgroupy
import numpy as np


def _get_key_symgroup(label, center, central_atom, connectivity, multi, connect_thresh):
    group_key = label.lower()
    center_key = ' '.join(['{:10.8f}'.format(n) for n in center]) if center is not None else None
    connectivity_key = np.array2string(np.array(connectivity), precision=10) if connectivity is not None else None
    multi_key = int(multi)
    central_atom_key = int(central_atom)
    connect_thresh_key = '{:10.8f}'.format(connect_thresh)
    return group_key, center_key, central_atom_key, connectivity_key, multi_key, connect_thresh_key


def _get_key_wfnsym(group, vector_axis1, vector_axis2, center, alpha_occupancy, beta_occupancy):
    group_key = group.lower()
    vec1_key = ' '.join(['{:10.8f}'.format(n) for n in vector_axis1]) if vector_axis1 is not None else None
    vec2_key = ' '.join(['{:10.8f}'.format(n) for n in vector_axis2]) if vector_axis2 is not None else None
    center_key = ' '.join(['{:10.8f}'.format(n) for n in center]) if center is not None else None
    alpha_occupancy_key = ' '.join(['{:10.8f}'.format(n) for n in alpha_occupancy]) if alpha_occupancy is not None else None
    beta_occupancy_key = ' '.join(['{:10.8f}'.format(n) for n in beta_occupancy]) if beta_occupancy is not None else None
    return group_key, vec1_key, vec2_key, center_key, alpha_occupancy_key, beta_occupancy_key


class Symmetry:
    """
    Symmetry main class

    :param structure: a geometry, molecule or array type object
    :type structure: Geometry, Molecule, np.array
    :param central_atom: central atom position
    :type central_atom: int
    :param center: center of symmetry in Cartesian coordinates. By default center is optimized
    :type center: list
    :param connect_thresh: Connectivity threshold (Ionic radius is used as reference)
    :type connect_thresh: float
    :param multi: Number of symmetry axis to find
    :type multi: int
    :param axis: Main symmetry axis (If None, then optimize)
    :type axis: list
    :param axis2: secondary symmetry axis (If None, then optimize)
    :type axis2: list
    """

    def __init__(self,
                 structure,
                 central_atom=0,
                 center=None,
                 connect_thresh=1.2,
                 multi=1,
                 axis=None,
                 axis2=None,
                 ):

        try:
            # Interpret as Geometry or molecule
            self._coordinates = structure.get_positions()
            self._symbols = structure.get_symbols()
            self._connectivity = structure.get_connectivity()
        except AttributeError:
            # Interpret as numpy array of coordinates or list of lists
            self._coordinates = structure
            self._symbols = None
            self._connectivity = None

        # If molecule object add electronic structure
        try:
            self._electronic_structure = structure.electronic_structure
        except AttributeError:
            self._electronic_structure = None

        self._central_atom = central_atom
        self._center = center
        self._connect_thresh = connect_thresh
        self._multi = multi
        self._axis = axis
        self._axis2 = axis2
        self._results = {}

    # Modifier methods
    def set_parameters(self, parameters_dict):
        """
        Set symmetry calculation related parameters

        :param parameters_dict: parameters in dictionary
        :type parameters_dict: dict
        """
        for name, value in parameters_dict.items():
            setattr(self, '_' + name, value)

    def set_electronic_structure(self, electronic_structure):
        self._electronic_structure = electronic_structure

    def _get_symgroup_results(self, group):

        """
        # Temporal interface
        if central_atom is not None:
            self._central_atom = central_atom

        self._multi = multi
        self._center = center
        self._connect_thresh = connect_thresh
        """

        # Crude calculation call methods
        key = _get_key_symgroup(group, self._center, self._central_atom, self._connectivity, self._multi, self._connect_thresh)
        if key not in self._results:
            self._results[key] = Symgroupy(self._coordinates,
                                           group=group,
                                           labels=self._symbols,
                                           central_atom=self._central_atom,
                                           multi=self._multi,
                                           center=self._center,
                                           connectivity=self._connectivity,
                                           connect_thresh=self._connect_thresh,
                                           permutation=None)

        return self._results[key]

    def _get_wfnsym_results(self, group):
        if self._electronic_structure is None:
            raise Exception('Electronic structure not set')

        key = _get_key_wfnsym(group, self._axis, self._axis2, self._center, self._electronic_structure.alpha_occupancy,
                              self._electronic_structure.beta_occupancy)

        if key not in self._results:
            self._results[key] = WfnSympy(coordinates=self._coordinates,
                                          symbols=self._symbols,
                                          basis=self._electronic_structure.basis,
                                          center=self._center,
                                          axis=self._axis,
                                          axis2=self._axis2,
                                          alpha_mo_coeff=self._electronic_structure.coefficients_a,
                                          beta_mo_coeff=self._electronic_structure.coefficients_b,
                                          group=group.upper(),
                                          alpha_occupancy=self._electronic_structure.alpha_occupancy,
                                          beta_occupancy=self._electronic_structure.beta_occupancy)
        return self._results[key]

    ##########################################
    #       Structure symmetry methods       #
    ##########################################

    def measure(self, label):
        """
        Get symmetry measure

        :param label: Point group label
        :type label: str
        :return: The measure
        :rtype: float
        """
        return self._get_symgroup_results(label).csm

    def nearest_structure(self, label):
        """
        Get nearest structure

        :param label: Point group label
        :type label: str
        :return: The structure
        :rtype: Structure
        """
        # TODO: Improve this docstring

        return self._get_symgroup_results(label).nearest_structure

    def optimum_axis(self, label):
        """
        Get the optimum main symmetry axis

        :param label: Point group label
        :type label: str
        :return: The axis
        :rtype: list
        """
        return self._get_symgroup_results(label).optimum_axis

    def optimum_permutation(self, label):
        """
        Get the optimum atoms permutation

        :param label: point group label
        :return: The permutation
        :rtype: list
        """
        return self._get_symgroup_results(label).optimum_permutation

    def reference_axis(self, label):
        """
        Get reference axis

        :param label: point group label
        :type label: str
        :return: The axis
        :rtype: list
        """
        return self._get_symgroup_results(label).reference_axis

    def cms_multi(self, label, multi=1):
        """
        Get symmetry measure of the optimum N axis

        :param label: point group label
        :type label: str
        :param multi: number of axis
        :type multi: int
        :return: The measures
        :rtype: list
        """
        self._multi = multi
        return self._get_symgroup_results(label).cms_multi

    def axis_multi(self, label, multi=1):
        """
        Get the optimum N axis

        :param label: point group label
        :type label: str
        :param multi: number of axis
        :type multi: int
        :return: List of axis
        :rtype: list
        """
        self._multi = multi
        return self._get_symgroup_results(label).axis_multi

    ##########################################
    #       Electronic symmetry methods      #
    ##########################################

    # TODO: Consider to migrate this methods data to pandas tabular structures
    def mo_irreducible_representations(self, group):
        results = self._get_wfnsym_results(group)

        return {'labels': results.IRLab,
                'alpha': results.mo_IRd_a,
                'beta': results.mo_IRd_b}

    def wf_irreducible_representations(self, group):
        results = self._get_wfnsym_results(group)

        return {'labels': results.SymLab,
                'alpha': results.wf_IRd_a,
                'beta': results.wf_IRd_b,
                'total': results.wf_IRd}

    def mo_overlaps(self, group):
        results = self._get_wfnsym_results(group)

        return {'labels': results.SymLab,
                'alpha': results.mo_SOEVs_a,
                'beta': results.mo_SOEVs_b}

    def wf_overlaps(self, group):
        results = self._get_wfnsym_results(group)

        return {'labels': results.SymLab,
                'alpha': results.wf_SOEVs_a,
                'beta': results.wf_SOEVs_b,
                'total': results.wf_SOEVs}

    def symmetry_matrix(self, group):
        results = self._get_wfnsym_results(group)
        return {'labels': results.SymLab,
                'matrix': results.SymMat}

    def wf_measure(self, group):
        results = self._get_wfnsym_results(group)
        return {'labels': results.SymLab,
                'csm': results.csm_coef,
                'grim': results.grim_coef}

    def wf_ideal_group_table(self, group):
        results = self._get_wfnsym_results(group)
        return {'ir_labels' : results.IRLab,
                'labels': results.SymLab,
                'table': results.ideal_gt}

    def dens_measure(self, group):
        results = self._get_wfnsym_results(group)
        return {'labels': results.SymLab,
                'csm': results.csm_dens,
                'csm_coef': results.csm_dens_coef}

    def axes(self, group):
        results = self._get_wfnsym_results(group)
        return {'center' : results.center,
                'axis': results.axis,
                'axis2': results.axis2}
