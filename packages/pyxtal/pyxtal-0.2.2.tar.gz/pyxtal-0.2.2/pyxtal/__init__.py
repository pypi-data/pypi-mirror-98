"""
main pyxtal module to create the pyxtal class
"""

# Standard Libraries
from copy import deepcopy
from random import choice, sample
import itertools
import numpy as np

from ase import Atoms
from pymatgen.core.structure import Structure, Molecule

# PyXtal imports #avoid *
from pyxtal.version import __version__
from pyxtal.molecular_crystal import (
    molecular_crystal,
    molecular_crystal_2D,
    molecular_crystal_1D,
)
from pyxtal.crystal import (
    random_cluster,
    random_crystal,
    random_crystal_1D,
    random_crystal_2D,
)
from pyxtal.symmetry import Group, Wyckoff_position, search_matched_position
from pyxtal.operations import apply_ops, SymmOp, get_inverse
from pyxtal.wyckoff_site import atom_site, mol_site, WP_merge
from pyxtal.wyckoff_split import wyckoff_split
from pyxtal.molecule import pyxtal_molecule
from pyxtal.lattice import Lattice
from pyxtal.tolerance import Tol_matrix
from pyxtal.io import read_cif, write_cif, structure_from_ext
from pyxtal.XRD import XRD
from pyxtal.constants import letters
from pyxtal.viz import display_molecular, display_atomic

# name = "pyxtal"

def print_logo():
    """
    print out the logo and version information
    """

    print(
        """
             ______       _    _          _
            (_____ \     \ \  / /        | |
             _____) )   _ \ \/ / |_  ____| |
            |  ____/ | | | )  (|  _)/ _  | |
            | |    | |_| |/ /\ \ |_( (_| | |___
            |_|     \__  /_/  \_\___)__|_|_____)
                   (____/      """
    )
    print("\n")
    print("----------------------(version", __version__, ")----------------------\n")
    print("A Python package for random crystal generation")
    print("The source code is available at https://github.com/qzhu2017/pyxtal")
    print("Developed by Zhu's group at University of Nevada Las Vegas\n\n")

class pyxtal:
    """
    Class for handling atomic crystals based on symmetry constraints

    Examples
    --------

    To create a new structure instance

    >>> from pyxtal import pyxtal
    >>> struc = pyxtal()

    one can either use pyxtal to generate a random symmetric structure

    >>> struc.from_random(3, 227, ['C'], [8])

    or load a structure from a file or ASE atoms or Pymatgen structure object

    >>> struc.from_seed('diamond.cif')     # as a string
    >>> struc.from_seed(diamond_ase)       # as a ase atoms object
    >>> struc.from_seed(diamond_pymatgen)  # as a pymatgen structure object

    as long as the struc is created, you can check their symmetry as follows

    >>> struc.get_site_labels()
    {'C': ['8a']}
    >>> struc
    ------Crystal from random------
    Dimension: 3
    Composition: C8
    Group: Fd-3m (227)
    cubic lattice:   4.3529   4.3529   4.3529  90.0000  90.0000  90.0000
    Wyckoff sites:
	 C @ [0.1250 0.1250 0.1250], WP:  8a, Site symmetry: -4 3 m

    The structure object can be easily manipulated via `apply_perturbtation`
    or `subgroup` function

    >>> struc2 = struc.subgroup_once(H=141)
    >>> struc2
    ------Crystal from Wyckoff Split------
    Dimension: 3
    Composition: C8
    Group: I41/amd (141)
    tetragonal lattice:   3.3535   3.3535   4.6461  90.0000  90.0000  90.0000
    Wyckoff sites:
    	 C @ [0.0000 0.2500 0.3750], WP:  4b, Site symmetry: -4 m 2

    Alternatively, one can also easily compute its XRD via the `pyxtal.XRD` class

    >>> xrd = struc.get_XRD()
    >>> xrd
      2theta     d_hkl     hkl       Intensity  Multi
      32.706     2.738   [ 1  1  1]   100.00        8
      54.745     1.677   [ 2  2  0]    40.95       12
      65.249     1.430   [ 3  1  1]    20.65       24
      81.116     1.186   [ 4  0  0]     5.15        6
      90.236     1.088   [ 3  3  1]     8.24       24
     105.566     0.968   [ 4  2  2]    14.44       24
     115.271     0.913   [ 5  1  1]    10.03       24
     133.720     0.838   [ 4  4  0]     9.80       12
     148.177     0.802   [ 5  3  1]    28.27       48

    Finally, the structure can be saved to different formats

    >>> struc.to_file('my.cif')
    >>> struc.to_file('my_poscar', fmt='poscar')

    or to Pymatgen/ASE structure object

    >>> pmg_struc = struc.to_pymatgen()
    >>> ase_struc = struc.to_ase()
    """

    def __init__(self, molecular=False):
        self.valid = False
        self.molecular = molecular
        self.diag = False
        self.numIons = None
        self.numMols = None
        self.source = None
        self.formula = None
        self.species = None
        self.group = None
        self.lattice = None
        self.dim = 3
        self.factor = 1.0
        self.PBC = [1,1,1]
        if molecular:
            self.molecules = []
            self.mol_sites = []
        else:
            self.atom_sites = []

    def __str__(self):
        if self.valid:
            s = "\n------Crystal from {:s}------".format(self.source)
            s += "\nDimension: {}".format(self.dim)
            s += "\nComposition: {}".format(self.formula)
            if self.group.number in [7, 14, 15] and self.diag:
                symbol = self.group.alias
            else:
                symbol = self.group.symbol
            s += "\nGroup: {} ({})".format(symbol, self.group.number)
            s += "\n{}".format(self.lattice)
            s += "\nWyckoff sites:"
            if self.molecular:
                for wyc in self.mol_sites:
                    s += "\n\t{}".format(wyc)
            else:
                for wyc in self.atom_sites:
                    s += "\n\t{}".format(wyc)
        else:
            s = "\nStructure not available."
        return s

    def __repr__(self):
        return str(self)

    def get_dof(self):
        """
        get the number of dof for the given structures:
        """
        if self.molecular:
            sites = self.mol_sites
        else:
            sites = self.atom_sites
        dof = 0
        for site in sites:
            dof += site.dof

        return self.lattice.dof + dof

    def get_site_labels(self):
        """
        quick function to get the site_labels as a dictionary
        """
        if self.molecular:
            sites = self.mol_sites
            names = [site.molecule.name for site in sites]
        else:
            sites = self.atom_sites
            names = [site.specie for site in sites]

        dicts = {}
        for name, site in zip(names, sites):
            label = str(site.wp.multiplicity) + site.wp.letter
            if name not in dicts.keys():
                dicts[name] = [label]
            else:
                dicts[name].append(label)
        return dicts


    def from_random(
        self,
        dim = 3,
        group=None,
        species=None,
        numIons=None,
        factor=1.1,
        thickness = None,
        area = None,
        lattice=None,
        sites = None,
        conventional = True,
        diag = False,
        t_factor = 1.0,
        max_count = 10,
        force_pass = False,
    ):
        if self.molecular:
            prototype = "molecular"
        else:
            prototype = "atomic"
        tm = Tol_matrix(prototype=prototype, factor=t_factor)

        count = 0
        quit = False

        while True:
            count += 1
            if self.molecular:
                if dim == 3:
                    struc = molecular_crystal(group, species, numIons, factor,
                    lattice=lattice, sites=sites, conventional=conventional, diag=diag, tm=tm)
                elif dim == 2:
                    struc = molecular_crystal_2D(group, species, numIons, factor,
                    thickness=thickness, sites=sites, conventional=conventional, tm=tm)
                elif dim == 1:
                    struc = molecular_crystal_1D(group, species, numIons, factor,
                    area=area, sites=sites, conventional=conventional, tm=tm)
            else:
                if dim == 3:
                    struc = random_crystal(group, species, numIons, factor,
                            lattice, sites, conventional, tm)
                elif dim == 2:
                    struc = random_crystal_2D(group, species, numIons, factor,
                            thickness, lattice, sites, conventional, tm)
                elif dim == 1:
                    struc = random_crystal_1D(group, species, numIons, factor,
                            area, lattice, sites, conventional, tm)
                else:
                    struc = random_cluster(group, species, numIons, factor,
                            lattice, sites, tm)
            if force_pass:
                quit = True
                break
            elif struc.valid:
                quit = True
                break

            if count >= max_count:
                raise RuntimeError("It takes long time to generate the structure, check inputs")

        if quit:
            self.valid = struc.valid
            self.dim = dim
            try:
                self.lattice = struc.lattice
                if self.molecular:
                    self.numMols = struc.numMols
                    self.molecules = struc.molecules
                    self.mol_sites = struc.mol_sites
                    self.diag = struc.diag
                else:
                    self.numIons = struc.numIons
                    self.species = struc.species
                    self.atom_sites = struc.atom_sites
                self.group = struc.group
                self.PBC = struc.PBC
                self.source = 'random'
                self.factor = struc.factor
                self._get_formula()
            except:
                pass


    def from_seed(self, seed, molecule=None, tol=1e-4, a_tol=5.0, relax_h=False, backend='pymatgen'):
        """
        Load the seed structure from Pymatgen/ASE/POSCAR/CIFs
        Internally they will be handled by Pymatgen
        """

        if self.molecular:
            pmol = pyxtal_molecule(molecule).mol
            struc = structure_from_ext(seed, pmol, relax_h=relax_h)
            if struc.match():
                self.mol_sites = [struc.make_mol_site()]
                self.group = Group(struc.wyc.number)
                self.lattice = struc.lattice
                self.molecules = [pyxtal_molecule(struc.molecule, symmetrize=False)]
                self.numMols = struc.numMols
                self.diag = struc.diag
                self.valid = True # Need to add a check function
            else:
                raise ValueError("Cannot extract the molecular crystal from cif")
        else:
            if isinstance(seed, dict):
                self.from_dict()
            elif isinstance(seed, Atoms): #ASE atoms
                from pymatgen.io.ase import AseAtomsAdaptor
                pmg_struc = AseAtomsAdaptor.get_structure(seed)
                self._from_pymatgen(pmg_struc, tol, a_tol)
            elif isinstance(seed, Structure): #Pymatgen
                self._from_pymatgen(seed, tol)
            elif isinstance(seed, str):
                if backend=='pymatgen':
                    pmg_struc = Structure.from_file(seed)
                    self._from_pymatgen(pmg_struc, tol, a_tol)
                else:
                    self.lattice, self.atom_sites = read_cif(seed)
                    self.group = Group(self.atom_sites[0].wp.number)
                    self.diag = self.atom_sites[0].diag
                    self.valid = True
        self.factor = 1.0
        self.source = 'Seed'
        self.dim = 3
        self.PBC = [1, 1, 1]
        self._get_formula()

    def _from_pymatgen(self, struc, tol=1e-3, a_tol=5.0):
        """
        Load structure from Pymatgen
        should not be used directly
        """
        from pyxtal.util import get_symmetrized_pmg
        #import pymatgen.analysis.structure_matcher as sm

        self.valid = True
        try:
            sym_struc, number = get_symmetrized_pmg(struc, tol, a_tol)
            #print(sym_struc)
            #import sys; sys.exit()
        except TypeError:
            print("Failed to load the Pymatgen structure")
        #    print(struc)
        #    self.valid = False

        if self.valid:
            d = sym_struc.composition.as_dict()
            species = [key for key in d.keys()]
            numIons = []
            for ele in species:
                numIons.append(int(d[ele]))
            self.numIons = numIons
            self.species = species
            self.group = Group(number)
            matrix, ltype = sym_struc.lattice.matrix, self.group.lattice_type
            self.lattice = Lattice.from_matrix(matrix, ltype=ltype)
            atom_sites = []
            for i, site in enumerate(sym_struc.equivalent_sites):
                pos = site[0].frac_coords
                wp = Wyckoff_position.from_group_and_index(number, sym_struc.wyckoff_symbols[i])
                specie = site[0].specie.number
                pos1 = search_matched_position(self.group, wp, pos)
                if pos1 is not None:
                    atom_sites.append(atom_site(wp, pos1, specie))
                else:
                    break

            if len(atom_sites) != len(sym_struc.equivalent_sites):
                raise RuntimeError("Cannot extract the right mapping from spglib")
            else:
                self.atom_sites = atom_sites
            #import pymatgen.analysis.structure_matcher as sm
            #self.dim = 3
            #self.PBC = [1, 1, 1]
            #pmg1 = self.to_pymatgen()
            #if not sm.StructureMatcher().fit(struc, pmg1):
            #    raise RuntimeError("The structure is inconsistent after conversion")

    def check_short_distances(self, r=0.7, exclude_H = True):
        """
        A function to check short distance pairs
        Mainly used for debug, powered by pymatgen

        Args:
            r: the given cutoff distances
            exclude_H: whether or not exclude the H atoms

        Returns:
            list of pairs within the cutoff
        """
        if self.dim > 0:
            pairs = []
            pmg_struc = self.to_pymatgen()
            if exclude_H:
                pmg_struc.remove_species('H')
            res = pmg_struc.get_all_neighbors(r)
            for i, neighs in enumerate(res):
                for n in neighs:
                    pairs.append([pmg_struc.sites[i].specie, n.specie, n.nn_distance])
        else:
            raise NotImplementedError("Does not support cluster for now")
        return pairs

    def check_short_distances_by_dict(self, dicts):
        """
        A function to check short distance pairs
        Mainly used for debug, powered by pymatgen

        Args:
            dicts: e.g., {"H-H": 1.0, "O-O": 2.0}

        Returns:
            N_pairs: number of atomic pairs within the cutoff
        """
        if self.dim > 0:
            N_pairs = 0
            r_cut = max([dicts[key] for key in dicts.keys()])
            pmg_struc = self.to_pymatgen()
            res = pmg_struc.get_all_neighbors(r_cut)
            for i, neighs in enumerate(res):
                ele1 = pmg_struc.sites[i].specie.value
                for n in neighs:
                    ele2 = n.specie.value
                    key1 = ele1 + '-' + ele2
                    key2 = ele2 + '-' + ele1
                    if key1 in dicts.keys() and n.nn_distance < dicts[key1]:
                        N_pairs += 1
                    elif key1 != key2 and key2 in dicts.keys() and n.nn_distance < dicts[key2]:
                        N_pairs += 1
        else:
            raise NotImplementedError("Does not support cluster for now")
        return N_pairs

    def to_file(self, filename=None, fmt=None, permission='w', sym_num=None):
        """
        Creates a file with the given filename and file type to store the structure.
        By default, creates cif files for crystals and xyz files for clusters.
        For other formats, Pymatgen is used

        Args:
            filename: the file path
            fmt: the file type (`cif`, `xyz`, etc.)
            permission: `w` or `a+`

        Returns:
            Nothing. Creates a file at the specified path
        """
        if self.valid:
            if fmt is None:
                if self.dim == 0:
                    fmt = 'xyz'
                else:
                    fmt = 'cif'

            if fmt == "cif":
                if self.dim == 3:
                    return write_cif(self, filename, "from_pyxtal", permission, sym_num=sym_num)
                else:
                    pmg_struc = self.to_pymatgen()
                    if self.molecular:
                        pmg_struc.sort()
                return pmg_struc.to(fmt=fmt, filename=filename)
            else:
                pmg_struc = self.to_pymatgen()
                if self.molecular:
                    pmg_struc.sort()
                return pmg_struc.to(fmt=fmt, filename=filename)
        else:
            raise RuntimeError("Cannot create file: structure did not generate")

    def supergroup(self, G=None, group_type='t', d_tol=1.0):
        """
        generate a structure with lower symmetry

        Args:
            G: super space group number (list of integers)
            group_type: `t`, `k` or `t+k`
            d_tol: maximum tolerance

        Returns:
            a list of pyxtal structures with minimum super group symmetries
        """

        from pyxtal.supergroup import supergroup

        my_super = supergroup(self, G=G, group_type=group_type)
        solutions = my_super.search_supergroup(d_tol=d_tol)
        return my_super.make_supergroup(solutions)

    def subgroup(self, permutations=None, H=None, eps=0.05, idx=None, group_type='t', max_cell=4):
        """
        generate a structure with lower symmetry

        Args:
            permutations: e.g., {"Si": "C"}
            H: space group number (int)
            eps: pertubation term (float)
            idx: list
            group_type: `t`, `k` or `t+k`
            max_cell: maximum cell reconstruction (float)

        Returns:
            a list of pyxtal structures with lower symmetries
        """

        #randomly choose a subgroup from the available list
        idx, sites, t_types, k_types = self._get_subgroup_ids(H, group_type, idx, max_cell)

        valid_splitters = []
        bad_splitters = []
        for id in idx:
            gtype = (t_types+k_types)[id]
            if gtype == 'k':
                id -= len(t_types)
            splitter = wyckoff_split(G=self.group.number, wp1=sites, idx=id, group_type=gtype)

            if not splitter.error:
                if permutations is None:
                    if splitter.valid_split:
                        special = False
                        if self.molecular:
                            for i in range(len(self.mol_sites)):
                                for ops in splitter.H_orbits[i]:
                                    if len(ops) < len(splitter.H[0]):
                                        special = True
                                        break
                        if not special:
                            valid_splitters.append(splitter)
                        else:
                            bad_splitters.append(splitter)
                    else:
                        bad_splitters.append(splitter)
                else:
                    # apply permuation
                    if len(splitter.H_orbits) == 1:
                        if len(splitter.H_orbits[0]) > 1:
                            valid_splitters.append(splitter)
                        else:
                            bad_splitters.append(splitter)
                    else:
                        valid_splitters.append(splitter)

        if len(valid_splitters) == 0:
            #print("try do one more step")
            new_strucs = []
            for splitter in bad_splitters:
                trail_struc = self._subgroup_by_splitter(splitter, eps=eps)
                new_strucs.extend(trail_struc.subgroup(permutations, group_type=group_type))
            return new_strucs
        else:
            #print(len(valid_splitters), "valid_splitters are present")
            new_strucs = []
            for splitter in valid_splitters:
                if permutations is None:
                    new_struc = self._subgroup_by_splitter(splitter, eps=eps)
                else:
                    new_struc = self._apply_substitution(splitter, permutations)
                new_strucs.append(new_struc)
            return new_strucs


    def subgroup_once(self, eps=0.1, H=None, permutations=None, group_type='t', max_cell=4, mut_lat=True):
        """
        generate a structure with lower symmetry (for atomic crystals only)

        Args:
            permutations: e.g., {"Si": "C"}
            H: space group number (int)
            idx: list
            group_type: `t` or `k`
            max_cell: maximum cell reconstruction (float)

        Returns:
            a list of pyxtal structures with lower symmetries
        """
        idx, sites, t_types, k_types = self._get_subgroup_ids(H, group_type, None, max_cell)

        # Try 100 times to see if a valid split can be found
        count = 0
        while count < 100:
            id = choice(idx)
            gtype = (t_types+k_types)[id]
            if gtype == 'k':
                id -= len(t_types)
            #print(self.group.number, sites, id, gtype)
            splitter = wyckoff_split(G=self.group.number, wp1=sites, idx=id, group_type=gtype)
            if not splitter.error:
                if permutations is not None:
                    if len(splitter.H_orbits) == 1:
                        if len(splitter.H_orbits[0]) > 1:
                            return self._apply_substitution(splitter, permutations)
                        else:
                            #print("try to find the next subgroup")
                            trail_struc = self._subgroup_by_splitter(splitter, eps=eps, mut_lat=mut_lat)
                            multiple = sum(trail_struc.numIons)/sum(self.numIons)
                            max_cell = max([1, max_cell/multiple])
                            ans = trail_struc.subgroup_once(eps, H, permutations, group_type, max_cell)
                            if ans.group.number > 1:
                                return ans
                    else:
                        return self._apply_substitution(splitter, permutations)
                else:
                    if splitter.valid_split:
                        special = False
                        if self.molecular:
                            for i in range(len(self.mol_sites)):
                                for ops in splitter.H_orbits[i]:
                                    if len(ops) < len(splitter.H[0]):
                                        special = True
                                        break
                        if not special:
                            return self._subgroup_by_splitter(splitter, eps=eps, mut_lat=mut_lat)
                    else:
                        #print("try to find the next subgroup")
                        trail_struc = self._subgroup_by_splitter(splitter, eps=eps, mut_lat=mut_lat)
                        multiple = sum(trail_struc.numIons)/sum(self.numIons)
                        max_cell = max([1, max_cell/multiple])
                        ans = trail_struc.subgroup_once(eps, H, None, group_type, max_cell)
                        if ans.group.number > 1:
                            return ans
            count += 1
        raise RuntimeError("Cannot find the splitter")

    def _apply_substitution(self, splitter, permutations):
        """
        dummy function to apply the substitution
        """
        try:
            new_struc = self._subgroup_by_splitter(splitter)
        except:
            print(self)
            print(splitter)
            print(len(splitter.H_orbits), len(splitter.G2_orbits), len(self.atom_sites))
            self._subgroup_by_splitter(splitter)

        site_ids = []
        for site_id, site in enumerate(new_struc.atom_sites):
            if site.specie in permutations.keys():
                site_ids.append(site_id)
        if len(site_ids) > 1:
            N = choice(range(1, len(site_ids)))
        else:
            N = 1
        sub_ids = sample(site_ids, N)
        for sub_id in sub_ids:
            key = new_struc.atom_sites[sub_id].specie
            new_struc.atom_sites[sub_id].specie = permutations[key]
        new_struc._get_formula()
        return new_struc

    def _get_subgroup_ids(self, H, group_type, idx, max_cell):
        """
        generate the subgroup dictionary
        """
        t_types = []
        k_types = []
        if group_type == 't':
            dicts = self.group.get_max_t_subgroup()#['subgroup']
            t_types = ['t']*len(dicts['subgroup'])
        elif group_type == 'k':
            dicts = self.group.get_max_k_subgroup()#['subgroup']
            k_types = ['k']*len(dicts['subgroup'])
        else:
            dicts = self.group.get_max_t_subgroup()#['subgroup']
            dict2 = self.group.get_max_k_subgroup()#['subgroup']
            t_types = ['t']*len(dicts['subgroup'])
            k_types = ['k']*len(dict2['subgroup'])
            for key in dicts.keys():
                dicts[key].extend(dict2[key])

        Hs = dicts['subgroup']
        trans = dicts['transformation']

        if idx is None:
            idx = []
            if not self.molecular:
                for i, tran in enumerate(trans):
                    if np.linalg.det(tran[:3,:3])<=max_cell:
                        idx.append(i)
            else:
                # for molecular crystals, assume the cell does not change
                for i, tran in enumerate(trans):
                    good = True
                    # QZ: This loop needs a generalization!
                    if abs(np.linalg.det(tran[:3,:3])-1)>1e-3:
                        good = False
                    elif self.group.number in [7, 14, 15] and self.diag and Hs[i]==4:
                        good = False
                    elif self.group.number in [31] and Hs[i]==7:
                        good = False
                    if good:
                        idx.append(i)
        else:
            for id in idx:
                if id >= len(Hs):
                    raise ValueError("The idx exceeds the number of possible splits")

        if H is not None:
            idx = [id for id in idx if Hs[id] == H]

        if len(idx) == 0:
            raise RuntimeError("Cannot find the splitter")

        if self.molecular:
            struc_sites = self.mol_sites
        else:
            struc_sites = self.atom_sites

        sites = [str(site.wp.multiplicity)+site.wp.letter for site in struc_sites]

        return idx, sites, t_types, k_types

    def _subgroup_by_splitter(self, splitter, eps=0.05, mut_lat=True):
        """
        transform the crystal to subgroup symmetry from a splitter object

        Args:
            splitter: wyckoff splitter object
            eps (float): maximum atomic displacement in Angstrom
            mut_lat (bool): whether or not mutate the lattice
        """
        lat1 = np.dot(splitter.R[:3,:3].T, self.lattice.matrix)
        multiples = np.linalg.det(splitter.R[:3,:3])
        new_struc = self.copy()
        new_struc.group = splitter.H
        lattice = Lattice.from_matrix(lat1, ltype=new_struc.group.lattice_type)
        if mut_lat:
            lattice=lattice.mutate(degree=eps, frozen=True)

        h = splitter.H.number
        split_sites = []
        if self.molecular:
            # below only works when the cell does not change
            for i, site in enumerate(self.mol_sites):
                pos = site.position
                mol = site.molecule
                ori = site.orientation
                coord0 = mol.mol.cart_coords.dot(ori.matrix.T)
                coord0 = np.dot(coord0, splitter.R[:3,:3])

                wp1 = site.wp
                ori.reset_matrix(np.eye(3))
                id = 0
                for ops1, ops2 in zip(splitter.G2_orbits[i], splitter.H_orbits[i]):
                    #reset molecule
                    rot = wp1.generators_m[id].affine_matrix[:3,:3].T
                    coord1 = np.dot(coord0, rot)
                    _mol = mol.copy()
                    _mol.reset_positions(coord1)

                    pos0 = apply_ops(pos, ops1)[0]
                    pos0 -= np.floor(pos0)
                    dis = (np.random.sample(3) - 0.5).dot(self.lattice.matrix)
                    dis /= np.linalg.norm(dis)
                    pos0 += eps*dis*(np.random.random()-0.5)
                    wp, _ = Wyckoff_position.from_symops(ops2, h, permutation=False)
                    if h in [7, 14] and self.group.number == 31:
                        diag = True
                    else:
                        diag = self.diag
                    split_sites.append(mol_site(_mol, pos0, ori, wp, lattice, diag))
                    id += wp.multiplicity
            new_struc.mol_sites = split_sites
            new_struc.numMols = [int(multiples*numMol) for numMol in self.numMols]

        else:
            for i, site in enumerate(self.atom_sites):
                pos = site.position
                for ops1, ops2 in zip(splitter.G2_orbits[i], splitter.H_orbits[i]):
                    pos0 = apply_ops(pos, ops1)[0]
                    pos0 -= np.floor(pos0)
                    dis = (np.random.sample(3) - 0.5).dot(self.lattice.matrix)
                    dis /= np.linalg.norm(dis)
                    pos0 += np.dot(eps*dis*(np.random.random()-0.5), self.lattice.inv_matrix)
                    wp, _ = Wyckoff_position.from_symops(ops2, h, permutation=False)
                    split_sites.append(atom_site(wp, pos0, site.specie))

            new_struc.atom_sites = split_sites
            new_struc.numIons = [int(multiples*numIon) for numIon in self.numIons]
        new_struc.lattice = lattice
        new_struc.source = 'subgroup'

        return new_struc

    def apply_perturbation(self, d_lat=0.05, d_coor=0.05, d_rot=1):
        """
        perturb the structure without breaking the symmetry

        Args:
            d_coor: magnitude of perturbation on atomic coordinates (in A)
            d_lat: magnitude of perturbation on lattice (in percentage)
        """

        self.lattice = self.lattice.mutate(degree=d_lat)

        if self.molecular:
            for site in self.mol_sites:
                site.perturbate(lattice=self.lattice.matrix, trans=d_coor, rot=d_rot)
        else:
            for site in self.atom_sites:
                site.perturbate(lattice=self.lattice.matrix, magnitude=d_coor)

        self.source = 'Perturbation'

    def copy(self):
        """
        simply copy the structure
        """
        return deepcopy(self)

    def _get_coords_and_species(self, absolute=False, unitcell=True):
        """
        extract the coordinates and species information

        Args:
            abosulte: if True, return the cartesian coords otherwise fractional

        Returns:
            total_coords (N*3 numpy array) and the list of species
        """
        species = []
        total_coords = None
        if self.molecular:
            for site in self.mol_sites:
                coords, site_species = site.get_coords_and_species(absolute, unitcell=unitcell)
                species.extend(site_species)
                if total_coords is None:
                    total_coords = coords
                else:
                    total_coords = np.append(total_coords, coords, axis=0)
        else:
            for site in self.atom_sites:
                species.extend([site.specie]*site.multiplicity)
                if total_coords is None:
                    total_coords = site.coords
                else:
                    total_coords = np.append(total_coords, site.coords, axis=0)

            if absolute:
                total_coords = total_coords.dot(self.lattice.matrix)

        return total_coords, species

    def _get_formula(self):
        """
        A quick function to get the formula.
        """

        formula = ""
        if self.molecular:
            numspecies = self.numMols
            species = [str(mol) for mol in self.molecules]
        else:
            specie_list = []
            for site in self.atom_sites:
                specie_list.extend([site.specie]*site.wp.multiplicity)
            species = list(set(specie_list))
            numIons = np.zeros(len(species), dtype=int)
            for i, sp in enumerate(species):
                numIons[i] = specie_list.count(sp)
            self.numIons = numIons
            self.species = species
            numspecies = self.numIons
        for i, s in zip(numspecies, species):
            formula += "{:s}{:d}".format(s, int(i))
        self.formula = formula

    def to_ase(self, resort=True):
        """
        export to ase Atoms object.
        """
        if self.valid:
            if self.dim > 0:
                lattice = self.lattice.copy()
                if self.molecular:
                    coords, species = self._get_coords_and_species(True)
                    latt, coords = lattice.add_vacuum(coords, frac=False, PBC=self.PBC)
                    atoms = Atoms(species, positions=coords, cell=latt, pbc=self.PBC)
                else:
                    coords, species = self._get_coords_and_species()
                    latt, coords = lattice.add_vacuum(coords, PBC=self.PBC)
                    atoms = Atoms(species, scaled_positions=coords, cell=latt, pbc=self.PBC)
                if resort:
                    permutation = np.argsort(atoms.numbers)
                    atoms = atoms[permutation]
                return atoms

            else:
                coords, species = self._get_coords_and_species(True)
                return Atoms(species, positions=coords)
        else:
            raise RuntimeError("No valid structure can be converted to ase.")

    def to_pymatgen(self, resort=True):
        """
        export to Pymatgen structure object.
        """

        if self.valid:
            if self.dim > 0:
                lattice = self.lattice.copy()
                coords, species = self._get_coords_and_species()
                if resort:
                    permutation = sorted(range(len(species)),key=species.__getitem__)
                    #permutation = np.argsort(species)
                    species = [species[id] for id in permutation]
                    coords = coords[permutation]
                # Add space above and below a 2D or 1D crystals
                latt, coords = lattice.add_vacuum(coords, PBC=self.PBC)
                return Structure(latt, species, coords)
            else:
                # Clusters are handled as large molecules
                coords, species = self._get_coords_and_species(True)
                return Molecule(species, coords)
        else:
            raise RuntimeError("No valid structure can be converted to pymatgen.")

    def get_XRD(self, **kwargs):
        """
        compute the PXRD object.

        ** kwargs include
            - wavelength (1.54184)
            - thetas [0, 180]
            - preferred_orientation: False
            - march_parameter: None
        """

        return XRD(self.to_ase(), **kwargs)

    def show(self, **kwargs):
        """
        display the crystal structure
        """
        if self.molecular:
            return display_molecular(self, **kwargs)
        else:
            return display_atomic(self, **kwargs)

    def optimize_lattice(self, iterations=3):
        """
        optimize the lattice if the cell has a bad inclination angles
        """
        #if self.molecular:
        count = 0
        for i in range(iterations):
            lattice, trans, opt = self.lattice.optimize()
            #print(self.lattice, "->", lattice)
            if opt:
                if self.molecular:
                    sites = self.mol_sites
                else:
                    sites = self.atom_sites

                for j, site in enumerate(sites):
                    count += 1
                    pos_abs = np.dot(site.position, self.lattice.matrix)
                    pos_frac = pos_abs.dot(lattice.inv_matrix)
                    pos_frac -= np.floor(pos_frac)
                    if self.molecular:
                        site.lattice = lattice
                    # for P21/c, Pc, C2/c, check if opt the inclination angle
                    ops = site.wp.ops.copy()
                    diag = False
                    if self.group.number in [7, 14, 15]:
                        for k, op in enumerate(ops):
                            vec = op.translation_vector.dot(trans)
                            vec -= np.floor(vec)
                            op1 = op.from_rotation_and_translation(op.rotation_matrix, vec)
                            ops[k] = op1
                        wp, perm = Wyckoff_position.from_symops(ops, self.group.number)

                        if not isinstance(perm, list):
                            diag = True
                        else:
                            diag = False
                            pos_frac = pos_frac[perm]

                        if self.molecular:
                            mol = site.molecule
                            ori = site.orientation
                            sites[j] = mol_site(mol, pos_frac, ori, wp, lattice, diag)
                        else:
                            sites[j] = atom_site(wp, pos_frac, site.specie, diag)
                        #print(sites[j].wp)
                    #site.update()

                self.lattice = lattice
                self.diag = diag
            else:
                break

#    def save(self, filename=None):
#        """
#        Save the structure
#        Args:
#            filename: the file to save txt information
#        """
#        dict0 = self.save_dict(db_filename)
#        with open(filename, "w") as fp:
#            json.dump(dict0, fp)
#
#        print("save the GP model to", filename, "and database to", db_filename)
#
#    def load(self, filename=None):
#        """
#        load the structure
#        Args:
#            filename: the file to save txt information
#        """
#        #print(filename)
#        with open(filename, "r") as fp:
#            dict0 = json.load(fp)
#        self.load_from_dict(dict0, N_max=N_max, device=device)
#        self.fit(opt=opt)
#        print("load the GP model from ", filename)
#
    def save_dict(self):
        """
        save the model as a dictionary
        """
        sites = []
        if self.molecular:
            for site in self.mol_sites:
                sites.append(site.save_dict())
        else:
            for site in self.atom_sites:
                sites.append(site.save_dict())

        dict0 = {"lattice": self.lattice.matrix,
                 "sites": sites,
                 "group": self.group.number,
                 "molecular": self.molecular,
                 "numIons": self.numIons,
                 "numMols": self.numMols,
                 "factor": self.factor,
                 "PBC": self.PBC,
                 "formula": self.formula,
                 "source": self.source,
                 "dim": self.dim,
                 "valid": self.valid,
                }

        return dict0

    def load_dict(self, dict0):
        """
        load the structure from a dictionary
        """
        self.group = Group(dict0["group"])
        self.lattice = Lattice.from_matrix(dict0["lattice"], ltype=self.group.lattice_type)
        self.molecular = dict0["molecular"]
        self.factor = dict0["factor"]
        self.source = dict0["source"]
        self.dim = dict0["dim"]
        self.PBC = dict0["PBC"]
        self.numIons = dict0["numIons"]
        self.numMols = dict0["numMols"]
        self.valid = dict0["valid"]
        self.formula = dict0["formula"]
        sites = []
        if dict0["molecular"]:
            for site in dict0["sites"]:
                sites.append(mol_site.load_dict(site))
            self.mol_sites = sites
        else:
            for site in dict0["sites"]:
                sites.append(atom_site.load_dict(site))
            self.atom_sites = sites

    def get_alternatives(self, include_self=True):
        """
        get alternative structure representations

        Args:
            include_self (bool): return the original structure
        Return:
            list of structures
        """
        if include_self:
            new_strucs = [self]
        else:
            new_strucs = []

        # the list of wyckoff indices in the original structure
        # e.g. [0, 2, 2, 4] -> [a, c, c, e]
        # ids = [len(self.group)-1-site.wp.index for site in self.atom_sites]

        wyc_sets = self.group.get_alternatives()
        No = len(wyc_sets['No.'])
        if No > 1:
            # skip the first setting since it is identity
            for no in range(1,No):
                new_struc, ids = self._get_alternative(wyc_sets, no)
                new_strucs.append(new_struc)
        return new_strucs

    def _get_alternative(self, wyc_set, index):
        """
        get alternative structure representations

        Args:
            tran: affine matrix
            index: the list of transformed wps

        Returns:
            a new pyxtal structure after transformation
        """
        new_struc = self.copy()

        # xyz_string like 'x+1/4,y+1/4,z+1/4'
        xyz_string = wyc_set['Coset Representative'][index]
        op = get_inverse(SymmOp.from_xyz_string(xyz_string))
        #op = SymmOp.from_xyz_string(xyz_string)

        ids = []
        for i, site in enumerate(new_struc.atom_sites):
            id = len(self.group) - site.wp.index - 1
            letter = wyc_set['Transformed WP'][index].split()[id]
            ids.append(letters.index(letter))
            wp = Wyckoff_position.from_group_and_index(self.group.number, letter)
            pos = op.operate(site.position)
            pos1 = search_matched_position(self.group, wp, pos)
            if pos1 is not None:
                new_struc.atom_sites[i] = atom_site(wp, pos1, site.specie)
            else:
                print(pos)
                print(wp)
                raise RuntimeError("Cannot find the right pos")

        # switch lattice
        R = op.affine_matrix[:3,:3] #rotation
        matrix = np.dot(R, self.lattice.matrix)
        new_struc.lattice = Lattice.from_matrix(matrix, ltype=self.group.lattice_type)
        new_struc.source = "Alt. Wyckoff Set: " + xyz_string
        return new_struc, ids
