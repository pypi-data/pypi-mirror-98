"""
Module for storing and accessing symmetry group information, including a Group class and
a Wyckoff_Position class. These classes are used for generation of random structures.
"""
# Imports
# ------------------------------
# Standard Libraries
import numpy as np
from pkg_resources import resource_filename
from copy import deepcopy
import random
import itertools
import re

# External Libraries
from pymatgen.symmetry.analyzer import generate_full_symmops
from pandas import read_csv
from monty.serialization import loadfn

# PyXtal imports
from pyxtal.msg import printx
from pyxtal.operations import (
    SymmOp,
    apply_ops,
    get_inverse_ops,
    filtered_coords_euclidean,
    distance_matrix,
    OperationAnalyzer,
)
from pyxtal.database.element import Element
from pyxtal.database.hall import hall_from_hm
from pyxtal.constants import letters
# ------------------------------ Constants ---------------------------------------

wyckoff_df = read_csv(resource_filename("pyxtal", "database/wyckoff_list.csv"))
wyckoff_symmetry_df = read_csv(
    resource_filename("pyxtal", "database/wyckoff_symmetry.csv")
)
wyckoff_generators_df = read_csv(
    resource_filename("pyxtal", "database/wyckoff_generators.csv")
)
layer_df = read_csv(resource_filename("pyxtal", "database/layer.csv"))
layer_symmetry_df = read_csv(resource_filename("pyxtal", "database/layer_symmetry.csv"))
layer_generators_df = read_csv(
    resource_filename("pyxtal", "database/layer_generators.csv")
)
rod_df = read_csv(resource_filename("pyxtal", "database/rod.csv"))
rod_symmetry_df = read_csv(resource_filename("pyxtal", "database/rod_symmetry.csv"))
rod_generators_df = read_csv(resource_filename("pyxtal", "database/rod_generators.csv"))
point_df = read_csv(resource_filename("pyxtal", "database/point.csv"))
point_symmetry_df = read_csv(resource_filename("pyxtal", "database/point_symmetry.csv"))
point_generators_df = read_csv(
    resource_filename("pyxtal", "database/point_generators.csv")
)
symbols = loadfn(resource_filename("pyxtal", "database/symbols.json"))

t_subgroup = loadfn(resource_filename("pyxtal",'database/t_subgroup.json'))
k_subgroup = loadfn(resource_filename("pyxtal",'database/k_subgroup.json'))
wyc_sets = loadfn(resource_filename("pyxtal",'database/wyckoff_sets.json'))

t2h = SymmOp.from_rotation_and_translation([[1, -0.5, 0], [0, np.sqrt(3) / 2, 0], [0, 0, 1]], [0, 0, 0])
Identity = SymmOp.from_xyz_string("x,y,z")
Inversion = SymmOp.from_xyz_string("-x,-y,-z")
op_o = SymmOp.from_xyz_string("0,0,0")
op_x = SymmOp.from_xyz_string("x,0,0")
op_y = SymmOp.from_xyz_string("0,y,0")
op_z = SymmOp.from_xyz_string("0,0,z")

# --------------------------- Group class -----------------------------
class Group:
    """
    Class for storing a set of Wyckoff positions for a symmetry group. See the documentation
    for details about settings.

    Examples
    --------
    >>> from pyxtal.symmetry import Group
    >>> g = Group(64)
    >>> g
    -- Spacegroup --# 64 (Cmce)--
    16g	site symm: 1
    8f	site symm: m..
    8e	site symm: .2.
    8d	site symm: 2..
    8c	site symm: -1
    4b	site symm: 2/m..
    4a	site symm: 2/m..

    one can access data with its attributes such as `symbol`, `number` and `Wyckoff_positions`

    >>> g.symbol
    'Cmce'
    >>> g.number
    64
    >>> g.Wyckoff_positions[0]
    Wyckoff position 16g in space group 64 with site symmetry 1
    x, y, z
    -x, -y+1/2, z+1/2
    -x, y+1/2, -z+1/2
    x, -y, -z
    -x, -y, -z
    x, y+1/2, -z+1/2
    x, -y+1/2, z+1/2
    -x, y, z
    x+1/2, y+1/2, z
    -x+1/2, -y+1, z+1/2
    -x+1/2, y+1, -z+1/2
    x+1/2, -y+1/2, -z
    -x+1/2, -y+1/2, -z
    x+1/2, y+1, -z+1/2
    x+1/2, -y+1, z+1/2
    -x+1/2, y+1/2, z

    We also provide several utilities functions, e.g.,
    one can search the possible wyckoff_combinations by a formula

    >>> g.list_wyckoff_combinations([4, 2])
    (None, False)
    >>> g.list_wyckoff_combinations([4, 8])
    ([[['4a'], ['8c']],
    [['4a'], ['8d']],
    [['4a'], ['8e']],
    [['4a'], ['8f']],
    [['4b'], ['8c']],
    [['4b'], ['8d']],
    [['4b'], ['8e']],
    [['4b'], ['8f']]],
    [False, True, True, True, False, True, True, True])

    or search the subgroup information

    >>> g.get_max_t_subgroup()['subgroup']
    [12, 14, 15, 20, 36, 39, 41]

    Args:
        group: the group symbol or international number
        dim: the periodic dimension of the group
    """

    def __init__(self, group, dim=3):
        
        self.dim = dim
        names = ['Point', 'Rod', 'Layer', 'Space']
        self.header = "-- " + names[dim] + 'group --'
        self.symbol, self.number = get_symbol_and_number(group, dim)
        self.PBC, self.lattice_type = get_pbc_and_lattice(self.number, dim)
        self.alias = None
        # Wyckoff positions, site_symmetry, generators, inverse
        # QZ: check if we can just use the get_wyckoff_symmetry function
        if dim == 3:
            if self.number in [7, 14, 15]:
                self.alias = self.symbol.replace("c","n")
            self.wyckoffs = get_wyckoffs(self.number) 
            self.w_symm = get_wyckoff_symmetry(self.number)
            self.wyckoff_generators = get_wyckoff_generators(self.number)
            self.w_symm_m = get_wyckoff_symmetry(self.number, molecular=True)
            self.wyckoff_generators_m = get_wyckoff_generators(self.number, molecular=True) 
            self.hall_number = hall_from_hm(self.number)
            self.point_group = get_point_group(self.number)
        elif dim == 2:
            self.wyckoffs = get_layer(self.number)
            self.w_symm = get_layer_symmetry(self.number)
            self.wyckoff_generators = get_layer_generators(self.number)
            self.w_symm_m = get_layer_symmetry(self.number, molecular=True)
            self.wyckoff_generators_m = get_layer_generators(self.number, molecular=True)
        elif dim == 1:
            self.wyckoffs = get_rod(self.number)
            self.w_symm = get_rod_symmetry(self.number)
            self.wyckoff_generators = get_rod_generators(self.number)
            self.w_symm_m = get_rod_symmetry(self.number, molecular=True)
            self.wyckoff_generators_m = get_rod_generators(self.number, molecular=True)
        elif dim == 0:
            self.wyckoffs = get_point(self.number)
            self.w_symm = get_point_symmetry(self.number)
            self.wyckoff_generators = get_point_generators(self.number)
            self.w_symm_m = self.w_symm
            self.wyckoff_generators_m = self.wyckoff_generators

        self.inverse_generators = get_inverse_ops(self.wyckoff_generators)
        self.inverse_generators_m = get_inverse_ops(self.wyckoff_generators_m)

        wpdicts = [
            {
                "index": i,
                "letter": letter_from_index(i, self.wyckoffs, dim=self.dim),
                "ops": self.wyckoffs[i],
                "multiplicity": len(self.wyckoffs[i]),
                "symmetry": self.w_symm[i],
                "symmetry_m": self.w_symm_m[i],
                "generators": self.wyckoff_generators[i],
                "generators_m": self.wyckoff_generators_m[i],
                "inverse_generators": self.inverse_generators[i],
                "inverse_generators_m": self.inverse_generators_m[i],
                "PBC": self.PBC,
                "dim": self.dim,
                "number": self.number,
                "symbol": self.symbol,
            }
            for i in range(len(self.wyckoffs))
        ]

        # A list of Wyckoff_position objects, sorted by descending multiplicity
        self.Wyckoff_positions = [Wyckoff_position.from_dict(wpdict) for wpdict in wpdicts]

        # A 2D list of Wyckoff_position objects, grouped and sorted by multiplicity
        self.wyckoffs_organized = organized_wyckoffs(self)


    def __str__(self):
        try:
            return self.string
        except:
            s = self.header
            s += "# " + str(self.number) + " (" + self.symbol + ")--"

            for wp in self.Wyckoff_positions:
                ops = ss_string_from_ops(wp.symmetry_m[0], self.number, dim=self.dim)
                s += ("\n" + str(wp.multiplicity) + wp.letter + "\tsite symm: " + ops)
            self.string = s

            return self.string

    def __repr__(self):
        return str(self)

    def __iter__(self):
        yield from self.Wyckoff_positions

    def __getitem__(self, index):
        return self.get_wyckoff_position(index)

    def __len__(self):
        return len(self.wyckoffs)

    def get_site_dof(self, sites):
        """
        compute the degree of freedom for each site
        Args:
            sites: list, e.g. ['4a', '8b'] or ['a', 'b']

        Returns:
            True or False
        """
        dof = np.zeros(len(sites))
        for i, site in enumerate(sites):
            if len(site) > 1:
                site = site[-1]
            id = len(self) - letters.index(site) - 1
            string = self[id].ops[0].as_xyz_string()
            dof[i] = len(set(re.sub('[^a-z]+', '', string)))

        return dof

    def is_valid_combination(self, sites):
        """
        check if the solutions are valid
        e.g., if a special WP with zero freedom (0,0,0) cannot be occupied twice

        Args:
            sites: list, e.g. ['4a', '8b'] or ['a', 'b']

        Returns:
            True or False
        """
        # remove the multiplicity:
        for i, site in enumerate(sites):
            if len(site) > 1:
                sites[i] = site[-1]
        
        for wp in self:
            letter = wp.letter
            if sites.count(letter)>1:
                freedom = np.trace(wp.ops[0].rotation_matrix) > 0
                if not freedom:
                    return False
        return True


    def list_wyckoff_combinations(self, numIons, quick=False):
        """
        List all possible wyckoff combinations for the given formula
        Note this is really design for a light weight calculation
        if the solution space is big, set quick as True

        Args:
            numIons: [12, 8]
            quick: Boolean, quickly generate some solutions

        Returns:
            Combinations: list of possible sites
            has_freedom: list of boolean numbers
        """

        numIons = np.array(numIons)

        basis = [] # [8, 4, 4]
        letters = [] # ['c', 'b', 'a']
        freedoms = [] # [False, False, False]

        # obtain the basis
        for i, wp in enumerate(self):
            mul = wp.multiplicity
            letter = wp.letter
            freedom = np.trace(wp.ops[0].rotation_matrix) > 0
            if mul <= max(numIons):
                if quick:
                    if mul in basis and freedom:
                        pass
                    #elif mul in basis and basis.count(mul) >= 3:
                    #    pass
                    else:
                        basis.append(mul)
                        letters.append(letter)
                        freedoms.append(freedom)
                else:
                    basis.append(mul)
                    letters.append(letter)
                    freedoms.append(freedom)

        basis = np.array(basis)

        # quickly exit
        if np.min(numIons) < np.min(basis):
            #print(numIons, basis)
            return None, False
        # odd and even
        elif np.mod(numIons, 2).sum()>0 and np.mod(basis, 2).sum()==0:
            #print("odd-even", numIons, basis)
            return None, False
        
        # obtain the maximum numbers for each basis
        max_solutions = np.floor(numIons[:,None]/basis)
        # reset the maximum to 1 if there is no freedom
        for i in range(len(freedoms)):
            if not freedoms[i]:
                max_solutions[:,i] = 1
        
        # find the integer solutions
        max_arrays = max_solutions.flatten()
        lists = []
        for a in max_arrays:
            d = int(a) + 1
            lists.append(list(range(d)))
        if len(lists) > 20:
            raise RuntimeError("Solution space is big, rerun it by setting quick as True")

        solutions = np.array(list(itertools.product(*lists)))
        big_basis = np.tile(basis, len(numIons))
        
        for i in range(len(numIons)):
            N = solutions[:,i*len(basis):(i+1)*len(basis)].dot(basis)
            solutions = solutions[N == numIons[i]]
            if len(solutions) == 0:
                #print("No solution is available")
                return None, False

        # convert the results to list
        combinations = []
        has_freedom = []
        for solution in solutions:
            res = solution.reshape([len(numIons), len(basis)])
            _com = []
            _free = []
            for i, numIon in enumerate(numIons):
                tmp = []
                bad_resolution = False
                frozen = []
                for j, b in enumerate(basis):
                    if not freedoms[j] and (res[:, j]).sum() > 1:
                        bad_resolution = True
                        break
                    else:
                        if res[i, j] > 0:
                            symbols = [str(b) + letters[j]] * res[i,j]
                            tmp.extend(symbols)
                            frozen.extend([freedoms[j]])
                if not bad_resolution:
                    _com.append(tmp)
                    _free.extend(frozen)
                       
            if len(_com) == len(numIons):
                combinations.append(_com)
                if True in _free:
                    has_freedom.append(True)
                else:
                    has_freedom.append(False)
 
        if len(combinations) == 0:
            #print("No solution is available")
            return None, False
        else:
            return combinations, has_freedom

    def get_wyckoff_position(self, index):
        """
        Returns a single Wyckoff_position object
        
        Args:
            index: the index of the Wyckoff position within the group
                The largest position is always 0

        Returns: a Wyckoff_position object
        """
        if type(index) == str:
            # Extract letter from number-letter combinations ("4d"->"d")
            for c in index:
                if c.isalpha():
                    letter = c
                    break
            index = index_from_letter(letter, self.wyckoffs, dim=self.dim)
        return self.Wyckoff_positions[index]

    def get_wyckoff_symmetry(self, index, molecular=False):
        """
        Returns the site symmetry symbol for the Wyckoff position

        Args:
            index: the index of the Wyckoff position within the group
                The largest position is always 0
            molecular: whether to use the Euclidean operations or not (for hexagonal groups)

        Returns: a Hermann-Mauguin style string for the site symmetry
        """
        if type(index) == str:
            # Extract letter from number-letter combinations ("4d"->"d")
            for c in index:
                if c.isalpha():
                    letter = c
                    break
            index = index_from_letter(letter, self.wyckoffs, dim=self.dim)
        if molecular:
            ops = self.w_symm_m[index][0]
        else:
            ops = self.w_symm[index][0]
        return ss_string_from_ops(ops, self.number, dim=self.dim)

    def get_max_t_subgroup(self):
        """
        Returns the maximal t-subgroups as a dictionary
        """
        if self.dim == 3:
            return t_subgroup[str(self.number)]
        else:
            raise NotImplementedError("Now we only support the subgroups for space group")
    
    def get_alternatives(self):
        """
        Get the alternative settings as a dictionary
        """
        if self.dim == 3:
            return wyc_sets[str(self.number)]
        else:
            raise NotImplementedError("Now we only support the subgroups for space group")

    def get_max_k_subgroup(self):
        """
        Returns the maximal k-subgroups as a dictionary
        """
        if self.dim == 3:
            return k_subgroup[str(self.number)]
        else:
            raise NotImplementedError("Now we only support the subgroups for space group")

    def get_max_t_subgroup(self):
        """
        Returns the maximal t-subgroups as a dictionary
        """
        if self.dim == 3:
            return t_subgroup[str(self.number)]
        else:
            raise NotImplementedError("Now we only support the subgroups for space group")
 
    def get_min_supergroup(self, group_type='t', G=None):
        """
        Returns the minimal supergroups as a dictionary
        """
        if self.dim == 3:
            dicts = {'supergroup': [],
                     'transformation': [],
                     'relations': [],
                     'idx': [],
                    }
            if G is None:
                sgs = range(1,231)
            else:
                sgs = G

            for sg in sgs:
                subgroups = None
                if group_type == 't':
                    if sg>self.number:
                        subgroups = Group(sg).get_max_t_subgroup()
                else:
                    g1 = Group(sg)
                    if g1.point_group == self.point_group:
                        subgroups = Group(sg).get_max_k_subgroup()
                if subgroups is not None:
                    for i, sub in enumerate(subgroups['subgroup']): 
                        if sub == self.number:
                            trans = subgroups['transformation'][i]
                            relation = subgroups['relations'][i]
                            dicts['supergroup'].append(sg)
                            dicts['transformation'].append(trans)
                            dicts['relations'].append(relation)
                            dicts['idx'].append(i)
            return dicts
        else:
            raise NotImplementedError("Now we only support the supergroups for space group")

    def get_max_subgroup_numbers(self):
        """
        Returns the minimal supergroups as a dictionary
        """
        groups = []
        if self.dim == 3:
            k = k_subgroup[str(self.number)]['subgroup']
            t = t_subgroup[str(self.number)]['subgroup']
            return k+t
        else:
            raise NotImplementedError("Now we only support the supergroups for space group")


    @classmethod
    def list_groups(cls, dim=3):
        """
        Function for quick print of groups and symbols
    
        Args:
            group: the group symbol or international number
            dim: the periodic dimension of the group
        """
    
        import pandas as pd
    
        keys = {
            3: "space_group",
            2: "layer_group",
            1: "rod_group",
            0: "point_group",
        }
        data = symbols[keys[dim]]
        df = pd.DataFrame(index=range(1, len(data) + 1), data=data, columns=[keys[dim]])
        pd.set_option("display.max_rows", len(df))
        print(df)

# --------------------------- Wyckoff Position class  -----------------------------

class Wyckoff_position:
    """
    Class for a single Wyckoff position within a symmetry group

    Examples
    --------
    >>> from pyxtal.symmetry import Wyckoff_position as wp
    >>> wp.from_group_and_index(19, 0)
    Wyckoff position 4a in space group 19 with site symmetry 1
    x, y, z
    -x+1/2, -y, z+1/2
    -x, y+1/2, -z+1/2
    x+1/2, -y+1/2, -z

    """

    def from_dict(dictionary):
        """
        Constructs a Wyckoff_position object using a dictionary. Used mainly by the
        Wyckoff class for constructing a list of Wyckoff_position objects at once
        """
        wp = Wyckoff_position()
        for key in dictionary:
            setattr(wp, key, dictionary[key])
        #wp.get_site_symmetry()
        return wp

    def __str__(self):
        if self.dim not in list(range(4)):
            return "invalid crystal dimension. Must be a number between 0 and 3."
        s = "Wyckoff position " + str(self.multiplicity) + self.letter + " in "
        if self.dim == 3:
            s += "space "
        elif self.dim == 2:
            s += "layer "
        elif self.dim == 1:
            s += "Rod "
        elif self.dim == 0:
            s += "Point group " + self.symbol
        if self.dim != 0:
            s += "group " + str(self.number)
        #s += " with site symmetry " + self.site_symm
        s += " with site symmetry " + ss_string_from_ops(
                self.symmetry_m[0], self.number, dim=self.dim
        )
        for op in self.ops:
            s += "\n" + op.as_xyz_string()
        self.string = s
        return self.string

    def __repr__(self):
        return str(self)

    def diagonalize_symops(self):
        """
        Obtain the symmetry in n representation for P21/c, Pc, C2/c
        """
        ops = Group(self.number)[self.index]
        if self.number in [7, 14, 15]:
            trans = np.array([[1,0,0],[0,1,0],[1,0,1]])
            for j, op in enumerate(ops):
                vec = op.translation_vector.dot(trans)
                vec -= np.floor(vec) 
                op1 = op.from_rotation_and_translation(op.rotation_matrix, vec)
                self.ops[j] = op1    

    def equivalent_set(self, index):
        """
        Transform the wp to another equivalent set.
        Needs to update both wp and positions

        Args:
            transformation: index
        """
        if self.index > 0:
            G = Group(self.number)
            if len(G[index]) != len(G[self.index]):
                msg = "Spg {:d}, Invalid switch in Wyckoff Position\n".format(self.number)
                msg += str(self)
                msg += "\n"+str(G[index])
                raise ValueError(msg)
            else:
                return G[index]
        return self


    def swap_axis(self, swap_id):
        """
        swap the axis may result in a new wp
        """
        if self.index > 0:
            perm_id = None
            _ops = [self.ops[0]]
            trans = [np.zeros(3)]
            if self.symbol[0] == "F":
                trans.append(np.array([0,0.5,0.5]))
                trans.append(np.array([0.5,0,0.5]))
                trans.append(np.array([0.5,0.5,0]))
            elif self.symbol[0] == "I":
                trans.append(np.array([0.5,0.5,0.5]))
            elif self.symbol[0] == "A":
                trans.append(np.array([0,0.5,0.5]))
            elif self.symbol[0] == "B":
                trans.append(np.array([0.5,0,0.5]))
            elif self.symbol[0] == "C":
                trans.append(np.array([0.5,0.5,0]))

            op_perm = swap_xyz_ops(_ops, swap_id)[0]
            for id, ops in enumerate(Group(self.number)):
                if len(ops) == len(self.ops):
                    for i, tran in enumerate(trans):
                        if i > 0:
                            # apply tran
                            op = op_translation(op_perm, tran)
                        else:
                            op = op_perm
                        #print(id, op.as_xyz_string(),tran)
                        if are_equivalent_ops(op, ops[0]):
                            perm_id = id
                            return Group(self.number)[id], tran
            if perm_id is None:
                raise ValueError("cannot swap", swap_id, self)
        return self, np.zeros(3)

    def from_symops(ops, group=None, permutation=True):
        """
        search Wyckoff Position by symmetry operations
        Now only supports space group symmetry

        Args:
            ops: a list of symmetry operations
            group: the space group number

        Returns:
            `Wyckoff_position`

        """
        if isinstance(ops[0], str):
            str1 = ops
        else:
            str1 = [op.as_xyz_string() for op in ops]

        str1 = [st.replace("-1/2","+1/2") for st in str1]

        N_sym = len(str1)
        # sometimes, we allow the permutation
        if permutation:
            permutations = [[0,1,2],[1,0,2],[2,1,0],[0,2,1]]
        else:
            permutations = [[0,1,2]]

        if group is None:
            groups = range(1,231)
        else:
            groups = [group]

        for i in groups:
            for wyc in Group(i):
                if len(wyc) == N_sym:
                    # Try permutation first
                    str2 = [op.as_xyz_string() for op in wyc.ops]
                    for perm in permutations:
                        str_perm = swap_xyz_string(str1, perm)
                        # Compare the pure rotation and then 
                        if set(str_perm) == set(str2):
                            return wyc, perm

                    # Try monoclinic space groups (P21/n, Pn, C2/n) 
                    if i in [7, 14, 15]:
                        trans = np.array([[1,0,0],[0,1,0],[1,0,1]])
                        str3 = []
                        for j, op in enumerate(wyc.ops):
                            vec = op.translation_vector.dot(trans)
                            vec -= np.floor(vec) 
                            op3 = op.from_rotation_and_translation(op.rotation_matrix, vec)
                            str3.append(op3.as_xyz_string().replace("-1/2","+1/2"))
                            #wyc.ops[j] = op3
                        if set(str3) == set(str1):
                            return wyc, trans
                elif len(wyc) < N_sym:
                    continue #break since it won'


        return None, None


    def from_group_and_index(group, index, dim=3, PBC=None):
        """
        Creates a Wyckoff_position using the space group number and index
        
        Args:
            group: the international number of the symmetry group
            index: the index or letter of the Wyckoff position within the group.
                0 is always the general position, and larger indeces represent positions
                with lower multiplicity. Alternatively, index can be the Wyckoff letter
                ("4a" or "6f")
            dim: the periodic dimension of the crystal
            PBC: the periodic boundary conditions
        """
        wp = Wyckoff_position()
        wp.dim = dim
        wp.number = group
        wp.PBC = PBC
        use_letter = False

        if np.issubdtype(type(index), np.integer):
            wp.index = index
        elif type(index) == str:
            use_letter = True
            # Extract letter from number-letter combinations ("4d"->"d")
            for c in index:
                if c.isalpha():
                    index = c
                    break

        if dim == 3:
            if wp.PBC is None:
                wp.PBC = [1, 1, 1]

            ops_all = get_wyckoffs(wp.number)
            if use_letter:
                wp.index = index_from_letter(index, ops_all, dim=dim)
                wp.letter = index
            else:
                wp.letter = letter_from_index(wp.index, ops_all, dim=dim)
            wp.ops = ops_all[wp.index]

            wp.multiplicity = len(wp.ops)
            wp.symmetry = get_wyckoff_symmetry(wp.number)[wp.index]
            wp.symmetry_m = get_wyckoff_symmetry(wp.number, molecular=True)[wp.index]
            wp.generators = get_wyckoff_generators(wp.number)[wp.index]
            wp.generators_m = get_wyckoff_generators(wp.number, molecular=True)[wp.index]
            wp.inverse_generators = get_inverse_ops(wp.generators)
            wp.inverse_generators_m = get_inverse_ops(wp.generators)

        elif dim == 2:
            if wp.PBC is None:
                wp.PBC = [1, 1, 0]

            ops_all = get_layer(wp.number)
            if use_letter:
                wp.index = index_from_letter(index, ops_all, dim=dim)
                wp.letter = index
            else:
                wp.letter = letter_from_index(wp.index, ops_all, dim=dim)
            wp.ops = ops_all[wp.index]

            wp.multiplicity = len(wp.ops)
            wp.symmetry = get_layer_symmetry(wp.number)[wp.index]
            wp.symmetry_m = get_layer_symmetry(wp.number, molecular=True)[wp.index]
            wp.generators = get_layer_generators(wp.number)[wp.index]
            wp.generators_m = get_layer_generators(wp.number, molecular=True)[wp.index]
            wp.inverse_generators = get_inverse_ops(wp.generators)
            wp.inverse_generators_m = get_inverse_ops(wp.generators)

        elif dim == 1:
            if wp.PBC is None:
                wp.PBC = [0, 0, 1]

            ops_all = get_rod(wp.number)
            if use_letter:
                wp.index = index_from_letter(index, ops_all, dim=dim)
                wp.letter = index
            else:
                wp.letter = letter_from_index(wp.index, ops_all, dim=dim)
            wp.ops = ops_all[wp.index]

            wp.multiplicity = len(wp.ops)
            wp.symmetry = get_rod_symmetry(wp.number)[wp.index]
            wp.symmetry_m = get_rod_symmetry(wp.number, molecular=True)[wp.index]
            wp.generators = get_rod_generators(wp.number)[wp.index]
            wp.generators_m = get_rod_generators(wp.number, molecular=True)[wp.index]
            wp.inverse_generators = get_inverse_ops(wp.generators)
            wp.inverse_generators_m = get_inverse_ops(wp.generators)

        elif dim == 0:
            # Generate a Group and retrieve Wyckoff position from it
            g = Group(group, dim=0)
            wp = g[index]
        #wp.get_site_symmetry()
        wp.symbol, _ = get_symbol_and_number(wp.number, wp.dim)
        return wp

    def wyckoff_from_generating_op(gen_op, gen_pos):
        """
        Given a general position and generating operation (ex: "x,0,0"), returns a
        Wyckoff_position object.
        
        Args:
            gen_op: a SymmOp into which the generating coordinate will be plugged
            gen_pos: a list of SymmOps representing the general position

        Returns:
            a list of SymmOps
        """

        def is_valid_generator(op):
            m = op.affine_matrix
            # Check for x,y+ax,z+bx+cy format
            # Make sure y, z are not referred to before second and third slots, respectively
            if (np.array([m[0][1], m[0][2], m[1][2]]) != 0.0).any():
                if (np.array([m[2][0], m[2][1], m[1][0]]) != 0.0).any():
                    return False
            for i in range(0, 3):
                # Check for translation
                if m[i][i] != 0 and m[i][3] != 0:
                    return False
                # Check that x, y, z are present in desired spot and positive
                if np.linalg.norm(m[:, i]) > 0:
                    if m[i][i] == 0:
                        return False
            return True

        def filter_zeroes(op):
            m = op.affine_matrix
            m2 = m
            for i, x in enumerate(m):
                for j, y in enumerate(x):
                    if np.isclose(y, 0, atol=1e-3):
                        m2[i][j] = 0
            return SymmOp(m2)

        # new_ops = [filter_zeroes(op*gen_op) for op in gen_pos]
        new_ops = [
            filter_zeroes(SymmOp(np.dot(op.affine_matrix, gen_op.affine_matrix)))
            for op in gen_pos
        ]

        # Remove redundant ops
        op_list = []
        for op1 in new_ops:
            passed = True
            for op2 in op_list:
                if np.allclose(op1.affine_matrix, op2.affine_matrix):
                    passed = False
                    break
            if passed is True:
                op_list.append(op1)

        # Check for identity op
        if Identity in op_list:
            index = op_list.index(Identity)
            op2 = op_list[0]
            op_list[index] = op2
            op_list[0] = Identity
            return op_list

        # Check for generating op
        found = False
        for op in op_list:
            if is_valid_generator(op):
                # Place generating op at beginning of list
                index = op_list.index(op)
                op2 = op_list[0]
                op_list[index] = op2
                op_list[0] = op
                found = True
                break
        if found is False:
            printx("Error: Could not find generating op.", priority=0)
            printx("gen_op: ")
            printx(str(gen_op))
            printx("gen_pos: ")
            printx(str(gen_pos))
            return op_list

        # Make sure first op is normalized
        m = op_list[0].affine_matrix
        x_factor = 1
        y_factor = 1
        z_factor = 1
        if m[0][0] != 0:
            if m[0][0] != 1:
                x_factor = m[0][0]
        if m[1][1] != 0:
            if m[1][1] != 1:
                y_factor = m[1][1]
        if m[2][2] != 0:
            if m[2][2] != 1:
                z_factor = m[2][2]
        new_list = []
        for op in op_list:
            m = op.affine_matrix
            m2 = m
            m2[:, 0] = m2[:, 0] / x_factor
            m2[:, 1] = m2[:, 1] / y_factor
            m2[:, 2] = m2[:, 2] / z_factor
            new_list.append(SymmOp(m2))

        return new_list

    def symmetry_from_wyckoff(wp, gen_pos):
        symm = []
        for op in wp:
            symm.append(site_symm(op, gen_pos))
        return symm

    def __iter__(self):
        yield from self.ops

    def __getitem__(self, index):
        return self.ops[index]

    def __len__(self):
        return self.multiplicity

    def get_site_symmetry(self):
        self.site_symm = ss_string_from_ops(self.symmetry_m[0], self.number, dim=self.dim)

    def gen_pos(self):
        """
        Returns the general Wyckoff position
        """
        return self.Wyckoff_positions[0]


# --------------------------- Wyckoff Position selection  -----------------------------

def choose_wyckoff(group, number=None, site=None, dim=3):
    """
    Choose a Wyckoff position to fill based on the current number of atoms
    needed to be placed within a unit cell
    Rules:
        0) use the pre-assigned list if this is provided
        1) The new position's multiplicity is equal/less than (number).
        2) We prefer positions with large multiplicity.

    Args:
        group: a pyxtal.symmetry.Group object
        number: the number of atoms still needed in the unit cell
        site: the pre-assigned Wyckoff sites (e.g., 4a)

    Returns:
        Wyckoff position. If no position is found, returns False
    """

    if site is not None:
        return Wyckoff_position.from_group_and_index(group.number, site, dim)
    else:
        wyckoffs_organized = group.wyckoffs_organized

        if random.uniform(0, 1) > 0.5:  # choose from high to low
            for wyckoff in wyckoffs_organized:
                if len(wyckoff[0]) <= number:
                    return random.choice(wyckoff)
            return False
        else:
            good_wyckoff = []
            for wyckoff in wyckoffs_organized:
                if len(wyckoff[0]) <= number:
                    for w in wyckoff:
                        good_wyckoff.append(w)
            if len(good_wyckoff) > 0:
                return random.choice(good_wyckoff)
            else:
                return False

def choose_wyckoff_molecular(group, number, site, orientations, general_site=True, dim=3):
    """
    Choose a Wyckoff position to fill based on the current number of molecules
    needed to be placed within a unit cell

    Rules:

        1) The new position's multiplicity is equal/less than (number).
        2) We prefer positions with large multiplicity.
        3) The site must admit valid orientations for the desired molecule.

    Args:
        group: a pyxtal.symmetry.Group object
        number: the number of molecules still needed in the unit cell
        orientations: the valid orientations for a given molecule. Obtained
            from get_sg_orientations, which is called within molecular_crystal

    Returns:
        Wyckoff position. If no position is found, returns False
    """
    wyckoffs = group.wyckoffs_organized

    if site is not None:
        return Wyckoff_position.from_group_and_index(group.number, site, dim)

    elif general_site or np.random.random() > 0.5:  # choose from high to low
        for j, wyckoff in enumerate(wyckoffs):
            if len(wyckoff[0]) <= number:
                good_wyckoff = []
                for k, w in enumerate(wyckoff):
                    if orientations[j][k] != []:
                        good_wyckoff.append(w)
                if len(good_wyckoff) > 0:
                    return random.choice(good_wyckoff)
        return False
    else:
        good_wyckoff = []
        for j, wyckoff in enumerate(wyckoffs):
            if len(wyckoff[0]) <= number:
                for k, w in enumerate(wyckoff):
                    if orientations[j][k] != []:
                        good_wyckoff.append(w)
        if len(good_wyckoff) > 0:
            return random.choice(good_wyckoff)
        else:
            return False

# -------------------- quick utilities for symmetry conversion ----------------
def swap_xyz_string(xyzs, permutation):
    """
    Permutate the xyz string operation

    Args:
        xyzs: e.g. ['x', 'y+1/2', '-z']
        permuation: list, e.g., [0, 2, 1]

    Returns:
        the new xyz string after transformation
    """
    if permutation == [0,1,2]:
        return xyzs
    else:
        new = []
        for xyz in xyzs:
            tmp = xyz.replace(" ","").split(',')
            tmp = [tmp[it] for it in permutation]
            if permutation == [1,0,2]: #a,b
                tmp[0] = tmp[0].replace('y','x')
                tmp[1] = tmp[1].replace('x','y')
            elif permutation == [2,1,0]: #a,c
                tmp[0] = tmp[0].replace('z','x')
                tmp[2] = tmp[2].replace('x','z')
            elif permutation == [0,2,1]: #b,c
                tmp[1] = tmp[1].replace('z','y')
                tmp[2] = tmp[2].replace('y','z')
            elif permutation == [1,2,0]: #b,c
                tmp[0] = tmp[0].replace('y','x')
                tmp[1] = tmp[1].replace('z','y')
                tmp[2] = tmp[2].replace('x','z')
            elif permutation == [2,0,1]: #b,c
                tmp[0] = tmp[0].replace('z','x')
                tmp[1] = tmp[1].replace('x','y')
                tmp[2] = tmp[2].replace('y','z')
            new.append(tmp[0] + ", " + tmp[1] + ", " + tmp[2])

        return new

def swap_xyz_ops(ops, permutation):
    """
    change the symmetry operation by swaping the axes

    Args: 
        ops: SymmOp object
        permutation: list, e.g. [0, 1, 2]

    Returns:
        the new xyz string after transformation
    """
    if permutation == [0,1,2]:
        return ops
    else:
        new = []
        for op in ops:
            m = op.affine_matrix.copy()
            m[:3,:] = m[permutation, :]
            for row in range(3):
                # [0, y+1/2, 1/2] -> (0, y, 1/2)
                if np.abs(m[row,:3]).sum()>0:
                    m[row, 3] = 0
            m[:3,:3] = m[:3, permutation]
            new.append(SymmOp(m))
        return new

def op_transform(ops, affine_matrix):
    """
    x, y, z -> x+1/2, y+1/2, z
    0, 1/2, z -> 1/2, 0, z

    Args: 
        ops: SymmOp object
        permutation: list, e.g. [0, 1, 2]

    Returns:
        the new SymmOp object
    """
    matrix2 = affine_matrix.dot(ops.affine_matrix)
    return SymmOp(matrix2)

def op_translation(op, tran):
    m = op.affine_matrix.copy()
    m[:3,3] += tran
    for row in range(3):
        # [0, y+1/2, 1/2] -> (0, y, 1/2)
        if np.abs(m[row,:3]).sum()>0:
            m[row, 3] = 0
    return SymmOp(m)

def are_equivalent_ops(op1, op2, tol=1e-2):
    """
    check if two ops are equivalent
    """
    diff = op1.affine_matrix - op2.affine_matrix
    diff[:,3] -= np.round(diff[:,3])
    diff = np.abs(diff.flatten())
    if np.sum(diff) < tol:
        return True
    else:
        return False
        


# TODO: Use Group object instead of organized array
def letter_from_index(index, group, dim=3):
    """
    Given a Wyckoff position's index within a spacegroup, return its number
    and letter e.g. '4a'

    Args:
        index: a single integer describing the WP's index within the
            spacegroup (0 is the general position)
        group: an unorganized Wyckoff position array or Group object (preferred)
        dim: the periodicity dimension of the symmetry group. Used for consideration
            of "o" Wyckoff positions in point groups. Not used if group is a Group
   
    Returns:
        the Wyckoff letter corresponding to the Wyckoff position (for example,
        for position 4a, the function would return 'a')
    """
    letters1 = letters
    # See whether the group has an "o" Wyckoff position
    checko = False
    if type(group) == Group and group.dim == 0:
        checko = True
    elif dim == 0:
        checko = True
    if checko is True:
        if len(group[-1]) == 1 and group[-1][0] == SymmOp.from_xyz_string("0,0,0"):
            # o comes before a
            letters1 = "o" + letters
    length = len(group)
    return letters1[length - 1 - index]


def index_from_letter(letter, group, dim=3):
    """
    Given the Wyckoff letter, returns the index of a Wyckoff position within
    the spacegroup

    Args:
        letter: The wyckoff letter
        group: an unorganized Wyckoff position array or Group object (preferred)
        dim: the periodicity dimension of the symmetry group. Used for consideration
            of "o" Wyckoff positions in point groups. Not used if group is a Group

    Returns:
        a single index specifying the location of the Wyckoff position within
        the spacegroup (0 is the general position)
    """
    letters1 = letters
    # See whether the group has an "o" Wyckoff position
    checko = False
    if type(group) == Group and group.dim == 0:
        checko = True
    elif dim == 0:
        checko = True
    if checko is True:
        if len(group[-1]) == 1 and group[-1][0] == SymmOp.from_xyz_string("0,0,0"):
            # o comes before a
            letters1 = "o" + letters
    length = len(group)
    return length - 1 - letters1.index(letter)


def jk_from_i(i, olist):
    """
    Given an organized list (Wyckoff positions or orientations), determine the
    two indices which correspond to a single index for an unorganized list.
    Used mainly for organized Wyckoff position lists, but can be used for other
    lists organized in a similar way

    Args:
        i: a single index corresponding to the item's location in the
            unorganized list
        olist: the organized list

    Returns:
        [j, k]: two indices corresponding to the item's location in the
            organized list
    """
    num = -1
    found = False
    for j, a in enumerate(olist):
        for k, b in enumerate(a):
            num += 1
            if num == i:
                return [j, k]
    printx(
        "Error: Incorrect Wyckoff position list or index passed to jk_from_i",
        priority=1,
    )
    return None


def i_from_jk(j, k, olist):
    """
    Inverse operation of jk_from_i: gives one list index from 2

    Args:
        j, k: indices corresponding to the location of an element in the
            organized list
        olist: the organized list of Wyckoff positions or molecular orientations

    Returns:
        i: one index corresponding to the item's location in the
            unorganized list    
    """
    num = -1
    for x, a in enumerate(olist):
        for y, b in enumerate(a):
            num += 1
            if x == j and y == k:
                return num
    printx(
        "Error: Incorrect Wyckoff position list or index passed to jk_from_i",
        priority=1,
    )
    return None


def ss_string_from_ops(ops, number, dim=3, complete=True):
    """
    Print the Hermann-Mauguin symbol for a site symmetry group, using a list of
    SymmOps as input. Note that the symbol does not necessarily refer to the
    x,y,z axes. For information on reading these symbols, see:
    http://en.wikipedia.org/wiki/Hermann-Mauguin_notation#Point_groups

    Args:
        ops: a list of SymmOp objects representing the site symmetry
        number: International number of the symmetry group. Used to determine which
            axes to show. For example, a 3-fold rotation in a cubic system is
            written as ".3.", whereas a 3-fold rotation in a trigonal system is
            written as "3.."
        dim: the dimension of the crystal. Also used to determine notation type
        complete: whether or not all symmetry operations in the group
            are present. If False, we generate the rest

    Returns:
        a string representing the site symmetry. Ex: ``2mm``
    """
    # TODO: Automatically detect which symm_type to use based on ops
    # Determine which notation to use
    symm_type = "high"
    if dim == 3:
        if number >= 1 and number <= 74:
            # Triclinic, monoclinic, orthorhombic
            symm_type = "low"
        elif number >= 75 and number <= 194:
            # Trigonal, Hexagonal, Tetragonal
            symm_type = "medium"
        elif number >= 195 and number <= 230:
            # cubic
            symm_type = "high"
    if dim == 2:
        if number >= 1 and number <= 48:
            # Triclinic, monoclinic, orthorhombic
            symm_type = "low"
        elif number >= 49 and number <= 80:
            # Trigonal, Hexagonal, Tetragonal
            symm_type = "medium"
    if dim == 1:
        if number >= 1 and number <= 22:
            # Triclinic, monoclinic, orthorhombic
            symm_type = "low"
        elif number >= 23 and number <= 75:
            # Trigonal, Hexagonal, Tetragonal
            symm_type = "medium"

    # TODO: replace sg with number, add dim variable
    # Return the symbol for a single axis
    # Will be called later in the function
    def get_symbol(opas, order, has_reflection):
        # ops: a list of Symmetry operations about the axis
        # order: highest order of any symmetry operation about the axis
        # has_reflection: whether or not the axis has mirror symmetry
        if has_reflection is True:
            # rotations have priority
            for opa in opas:
                if opa.order == order and opa.type == "rotation":
                    return str(opa.rotation_order) + "/m"
            for opa in opas:
                if (
                    opa.order == order
                    and opa.type == "rotoinversion"
                    and opa.order != 2
                ):
                    return "-" + str(opa.rotation_order)
            return "m"
        elif has_reflection is False:
            # rotoinversion has priority
            for opa in opas:
                if opa.order == order and opa.type == "rotoinversion":
                    return "-" + str(opa.rotation_order)
            for opa in opas:
                if opa.order == order and opa.type == "rotation":
                    return str(opa.rotation_order)
            return "."

    # Given a list of single-axis symbols, return the one with highest symmetry
    # Will be called later in the function
    def get_highest_symbol(symbols):
        symbol_list = [
            ".",
            "2",
            "m",
            "-2",
            "2/m",
            "3",
            "4",
            "-4",
            "4/m",
            "-3",
            "6",
            "-6",
            "6/m",
        ]
        max_index = 0
        use_list = True
        for j, symbol in enumerate(symbols):
            if symbol in symbol_list:
                i = symbol_list.index(symbol)
            else:
                use_list = False
                num_str = "".join(c for c in symbol if c.isdigit())
                i1 = int(num_str)
                if "m" in symbol or "-" in symbol:
                    if i1 % 2 == 0:
                        i = i1
                    elif i1 % 2 == 1:
                        i = i1 * 2
                else:
                    i = i1
            if i > max_index:
                max_j = j
                max_index = i
        if use_list is True:
            return symbol_list[max_index]
        else:
            return symbols[max_j]

    # Return whether or not two axes are symmetrically equivalent
    # It is assumed that both axes possess the same symbol
    # Will be called within combine_axes
    def are_symmetrically_equivalent(index1, index2):
        axis1 = axes[index1]
        axis2 = axes[index2]
        condition1 = False
        condition2 = False
        # Check for an operation mapping one axis onto the other
        for op in ops:
            if condition1 is False or condition2 is False:
                new1 = op.operate(axis1)
                new2 = op.operate(axis2)
                if np.isclose(abs(np.dot(new1, axis2)), 1):
                    condition1 = True
                if np.isclose(abs(np.dot(new2, axis1)), 1):
                    condition2 = True
        if condition1 is True and condition2 is True:
            return True
        else:
            return False

    # Given a list of axis indices, return the combined symbol
    # Axes may or may not be symmetrically equivalent, but must be of the same
    # type (x/y/z, face-diagonal, body-diagonal)
    # Will be called for mid- and high-symmetry crystallographic point groups
    def combine_axes(indices):
        symbols = {}
        for index in deepcopy(indices):
            symbol = get_symbol(params[index], orders[index], reflections[index])
            if symbol == ".":
                indices.remove(index)
            else:
                symbols[index] = symbol
        if indices == []:
            return "."
        # Remove redundant axes
        for i in deepcopy(indices):
            for j in deepcopy(indices):
                if j > i:
                    if symbols[i] == symbols[j]:
                        if are_symmetrically_equivalent(i, j):
                            if j in indices:
                                indices.remove(j)
        # Combine symbols for non-equivalent axes
        new_symbols = []
        for i in indices:
            new_symbols.append(symbols[i])
        symbol = ""
        while new_symbols != []:
            highest = get_highest_symbol(new_symbols)
            symbol += highest
            new_symbols.remove(highest)
        if symbol == "":
            printx("Error: could not combine site symmetry axes.", priority=1)
            return
        else:
            return symbol

    # Generate needed ops
    if complete is False:
        ops = generate_full_symmops(ops, 1e-3)
    # Get OperationAnalyzer object for all ops
    opas = []
    for op in ops:
        opas.append(OperationAnalyzer(op))
    # Store the symmetry of each axis
    params = [[], [], [], [], [], [], [], [], [], [], [], [], []]
    has_inversion = False
    # Store possible symmetry axes for crystallographic point groups
    axes = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 0],
        [0, 1, 1],
        [1, 0, 1],
        [1, -1, 0],
        [0, 1, -1],
        [1, 0, -1],
        [1, 1, 1],
        [-1, 1, 1],
        [1, -1, 1],
        [1, 1, -1],
    ]
    for i, axis in enumerate(axes):
        axes[i] = axis / np.linalg.norm(axis)
    for opa in opas:
        if opa.type != "identity" and opa.type != "inversion":
            found = False
            for i, axis in enumerate(axes):
                if np.isclose(abs(np.dot(opa.axis, axis)), 1):
                    found = True
                    params[i].append(opa)
            # Store uncommon axes for trigonal and hexagonal lattices
            if found is False:
                axes.append(opa.axis)
                # Check that new axis is not symmetrically equivalent to others
                unique = True
                for i, axis in enumerate(axes):
                    if i != len(axes) - 1:
                        if are_symmetrically_equivalent(i, len(axes) - 1):
                            unique = False
                if unique is True:
                    params.append([opa])
                elif unique is False:
                    axes.pop()
        elif opa.type == "inversion":
            has_inversion = True
    # Determine how many high-symmetry axes are present
    n_axes = 0
    # Store the order of each axis
    orders = []
    # Store whether or not each axis has reflection symmetry
    reflections = []
    for axis in params:
        order = 1
        high_symm = False
        has_reflection = False
        for opa in axis:
            if opa.order >= 3:
                high_symm = True
            if opa.order > order:
                order = opa.order
            if opa.order == 2 and opa.type == "rotoinversion":
                has_reflection = True
        orders.append(order)
        if high_symm == True:
            n_axes += 1
        reflections.append(has_reflection)
    # Triclinic, monoclinic, orthorhombic
    # Positions in symbol refer to x,y,z axes respectively
    if symm_type == "low":
        symbol = (
            get_symbol(params[0], orders[0], reflections[0])
            + get_symbol(params[1], orders[1], reflections[1])
            + get_symbol(params[2], orders[2], reflections[2])
        )
        if symbol != "...":
            return symbol
        elif symbol == "...":
            if has_inversion is True:
                return "-1"
            else:
                return "1"
    # Trigonal, Hexagonal, Tetragonal
    elif symm_type == "medium":
        # 1st symbol: z axis
        s1 = get_symbol(params[2], orders[2], reflections[2])
        # 2nd symbol: x or y axes (whichever have higher symmetry)
        s2 = combine_axes([0, 1])
        # 3rd symbol: face-diagonal axes (whichever have highest symmetry)
        s3 = combine_axes(list(range(3, len(axes))))
        symbol = s1 + " " + s2 + " " + s3
        if symbol != ". . .":
            return symbol
        elif symbol == ". . .":
            if has_inversion is True:
                return "-1"
            else:
                return "1"
    # Cubic
    elif symm_type == "high":
        pass
        # 1st symbol: x, y, and/or z axes (whichever have highest symmetry)
        s1 = combine_axes([0, 1, 2])
        # 2nd symbol: body-diagonal axes (whichever has highest symmetry)
        s2 = combine_axes([9, 10, 11, 12])
        # 3rd symbol: face-diagonal axes (whichever have highest symmetry)
        s3 = combine_axes([3, 4, 5, 6, 7, 8])
        symbol = s1 + " " + s2 + " " + s3
        if symbol != ". . .":
            return symbol
        elif symbol == ". . .":
            if has_inversion is True:
                return "-1"
            else:
                return "1"
    else:
        printx("Error: invalid spacegroup number", priority=1)
        return


def organized_wyckoffs(group):
    """
    Takes a Group object or unorganized list of Wyckoff positions and returns
    a 2D list of Wyckoff positions organized by multiplicity.

    Args:
        group: a pyxtal.symmetry.Group object
    
    Returns:
        a 2D list of Wyckoff_position objects if group is a Group object.
        a 3D list of SymmOp objects if group is a 2D list of SymmOps
    """
    if type(group) == Group:
        wyckoffs = group.Wyckoff_positions
    else:
        wyckoffs = group
    wyckoffs_organized = [[]]  # 2D Array of WP's organized by multiplicity
    old = len(wyckoffs[0])
    for wp in wyckoffs:
        mult = len(wp)
        if mult != old:
            wyckoffs_organized.append([])
            old = mult
        wyckoffs_organized[-1].append(wp)
    return wyckoffs_organized


def symmetry_element_from_axis(axis):
    """
    Given an axis, returns a SymmOp representing a symmetry element on the axis.
    For example, the symmetry element for the vector (0,0,2) would be (0,0,z).
    
    Args:
        axis: a 3-vector representing the symmetry element

    Returns:
        a SymmOp object of form (ax, bx, cx), (ay, by, cy), or (az, bz, cz)
    """
    if len(axis) != 3:
        return
    # Vector must be non-zero
    if axis.dot(axis) < 1e-6:
        return
    v = np.array(axis) / np.linalg.norm(axis)
    # Find largest component (x, y, or z)
    abs_vals = [abs(a) for a in v]
    f1 = max(abs_vals)
    index1 = list(abs_vals).index(f1)
    # Initialize an affine matrix
    m = np.eye(4)
    m[:3] = [0.0, 0.0, 0.0, 0.0]
    # Set values for affine matrix
    m[:3, index1] = v
    return SymmOp(m)


def get_wyckoffs(sg, organized=False, PBC=[1, 1, 1]):
    """
    Returns a list of Wyckoff positions for a given space group. Has option to
    organize the list based on multiplicity (this is used for
    random_crystal.wyckoffs) 
    
    For an unorganized list:

        - 1st index: index of WP in sg (0 is the WP with largest multiplicity)
        - 2nd index: a SymmOp object in the WP

    For an organized list:

        - 1st index: specifies multiplicity (0 is the largest multiplicity)
        - 2nd index: corresponds to a Wyckoff position within the group of equal multiplicity.
        - 3nd index: corresponds to a SymmOp object within the Wyckoff position

    You may switch between organized and unorganized lists using the methods
    i_from_jk and jk_from_i. For example, if a Wyckoff position is the [i]
    entry in an unorganized list, it will be the [j][k] entry in an organized
    list.

    Args:
        sg: the international spacegroup number
        organized: whether or not to organize the list based on multiplicity
        PBC: A periodic boundary condition list, where 1 means periodic, 0 means not periodic.
            Ex: [1,1,1] -> full 3d periodicity, [0,0,1] -> periodicity along the z axis
    
    Returns: 
        a list of Wyckoff positions, each of which is a list of SymmOp's
    """
    if PBC != [1, 1, 1]:
        coor = [0, 0, 0]
        for i, a in enumerate(PBC):
            if not a:
                coor[i] = 0.5
        coor = np.array(coor)

    wyckoff_strings = eval(wyckoff_df["0"][sg])
    wyckoffs = []
    for x in wyckoff_strings:
        if PBC != [1, 1, 1]:
            op = SymmOp.from_xyz_string(x[0])
            coor1 = op.operate(coor)
            invalid = False
            for i, a in enumerate(PBC):
                if not a:
                    if not abs(coor1[i] - 0.5) < 1e-2:
                        # invalid wyckoffs for layer group
                        invalid = True
            if invalid is False:
                wyckoffs.append([])
                for y in x:
                    wyckoffs[-1].append(SymmOp.from_xyz_string(y))
        else:
            wyckoffs.append([])
            for y in x:
                wyckoffs[-1].append(SymmOp.from_xyz_string(y))
    if organized:
        wyckoffs_organized = [[]]  # 2D Array of WP's organized by multiplicity
        old = len(wyckoffs[0])
        for wp in wyckoffs:
            mult = len(wp)
            if mult != old:
                wyckoffs_organized.append([])
                old = mult
            wyckoffs_organized[-1].append(wp)
        return wyckoffs_organized
    else:
        return wyckoffs


def get_layer(num, organized=False):
    """
    Returns a list of Wyckoff positions for a given 2D layer group. Has
    option to organize the list based on multiplicity (this is used for
    random_crystal_2D.wyckoffs) 
    
    For an unorganized list:

        - 1st index: index of WP in layer group (0 is the WP with largest multiplicity)
        - 2nd index: a SymmOp object in the WP

    For an organized list:

        - 1st index: specifies multiplicity (0 is the largest multiplicity)
        - 2nd index: corresponds to a Wyckoff position within the group of equal multiplicity.
        - 3nd index: corresponds to a SymmOp object within the Wyckoff position

    You may switch between organized and unorganized lists using the methods
    i_from_jk and jk_from_i. For example, if a Wyckoff position is the [i]
    entry in an unorganized list, it will be the [j][k] entry in an organized
    list.

    For layer groups with more than one possible origin, origin choice 2 is
    used.

    Args:
        num: the international layer group number
        organized: whether or not to organize the list based on multiplicity
    
    Returns: 
        a list of Wyckoff positions, each of which is a list of SymmOp's
    """
    wyckoff_strings = eval(layer_df["0"][num])
    wyckoffs = []
    for x in wyckoff_strings:
        wyckoffs.append([])
        for y in x:
            wyckoffs[-1].append(SymmOp.from_xyz_string(y))
    if organized:
        wyckoffs_organized = [[]]  # 2D Array of WP's organized by multiplicity
        old = len(wyckoffs[0])
        for wp in wyckoffs:
            mult = len(wp)
            if mult != old:
                wyckoffs_organized.append([])
                old = mult
            wyckoffs_organized[-1].append(wp)
        return wyckoffs_organized
    else:
        return wyckoffs


def get_rod(num, organized=False):
    """
    Returns a list of Wyckoff positions for a given 1D Rod group. Has option to
    organize the list based on multiplicity (this is used for
    random_crystal_1D.wyckoffs) 
    
    For an unorganized list:

        - 1st index: index of WP in layer group (0 is the WP with largest multiplicity)
        - 2nd index: a SymmOp object in the WP

    For an organized list:

        - 1st index: specifies multiplicity (0 is the largest multiplicity)
        - 2nd index: corresponds to a Wyckoff position within the group of equal multiplicity.
        - 3nd index: corresponds to a SymmOp object within the Wyckoff position

    You may switch between organized and unorganized lists using the methods
    i_from_jk and jk_from_i. For example, if a Wyckoff position is the [i]
    entry in an unorganized list, it will be the [j][k] entry in an organized
    list.

    For Rod groups with more than one possible setting, setting choice 1
    is used.

    Args:
        num: the international Rod group number
        organized: whether or not to organize the list based on multiplicity
    
    Returns: 
        a list of Wyckoff positions, each of which is a list of SymmOp's
    """
    wyckoff_strings = eval(rod_df["0"][num])
    wyckoffs = []
    for x in wyckoff_strings:
        wyckoffs.append([])
        for y in x:
            wyckoffs[-1].append(SymmOp.from_xyz_string(y))
    if organized:
        wyckoffs_organized = [[]]  # 2D Array of WP's organized by multiplicity
        old = len(wyckoffs[0])
        for wp in wyckoffs:
            mult = len(wp)
            if mult != old:
                wyckoffs_organized.append([])
                old = mult
            wyckoffs_organized[-1].append(wp)
        return wyckoffs_organized
    else:
        return wyckoffs


def get_point(num, organized=False):
    """
    Returns a list of Wyckoff positions for a given crystallographic point group.
    Has option to organize the list based on multiplicity.

    1st index: index of WP in layer group (0 is the WP with largest multiplicity)

    2nd index: a SymmOp object in the WP

    For point groups except T, Th, O, Td, and Oh, unique axis z is used.

    Args:
        num: the point group number (see bottom of source code for a list)
        organized: whether or not to organize the list based on multiplicity
        molecular: whether or not to convert to Euclidean reference frame
            (for hexagonal lattices: point groups 16-27)
    
    Returns: 
        a list of Wyckoff positions, each of which is a list of SymmOp's
    """
    wyckoff_strings = eval(point_df["0"][num])
    wyckoffs = []
    for x in wyckoff_strings:
        wyckoffs.append([])
        for y in x:
            op = SymmOp(y)
            wyckoffs[-1].append(op)
    if organized:
        wyckoffs_organized = [[]]  # 2D Array of WP's organized by multiplicity
        old = len(wyckoffs[0])
        for wp in wyckoffs:
            mult = len(wp)
            if mult != old:
                wyckoffs_organized.append([])
                old = mult
            wyckoffs_organized[-1].append(wp)
        return wyckoffs_organized
    else:
        return wyckoffs


def get_wyckoff_symmetry(sg, PBC=[1, 1, 1], molecular=False):
    #QZ: to get rid of something
    """
    Returns a list of Wyckoff position site symmetry for a given space group.
    1st index: index of WP in sg (0 is the WP with largest multiplicity)
    2nd index: a point within the WP
    3rd index: a site symmetry SymmOp of the point

    Args:
        sg: the international spacegroup number
        PBC: A periodic boundary condition list, Ex: [1,1,1] -> full 3d periodicity, [0,0,1] -> periodicity along the z axis
        molecular: whether or not to return the Euclidean point symmetry
            operations. If True, cuts off translational part of operation, and
            converts non-orthogonal operations (3-fold and 6-fold rotations)
            to (orthogonal) pure rotations. Should be used when dealing with
            molecular crystals

    Returns:
        a 3d list of SymmOp objects representing the site symmetry of each
        point in each Wyckoff position
    """
    if PBC != [1, 1, 1]:
        coor = [0, 0, 0]
        for i, a in enumerate(PBC):
            if not a:
                coor[i] = 0.5
        coor = np.array(coor)
    wyckoffs = get_wyckoffs(sg, PBC=PBC)


    symmetry_strings = eval(wyckoff_symmetry_df["0"][sg])
    symmetry = []
    convert = False
    if molecular and 143 <= sg <= 194: convert = True
    # Loop over Wyckoff positions
    for x, w in zip(symmetry_strings, wyckoffs):
        if PBC != [1, 1, 1]:
            op = w[0]
            coor1 = op.operate(coor)
            invalid = False
            for i, a in enumerate(PBC):
                if not a:
                    if not abs(coor1[i] - 0.5) < 1e-2:
                        invalid = True
            if not invalid:
                symmetry.append([])
                # Loop over points in WP
                for y in x:
                    symmetry[-1].append([])
                    # Loop over ops
                    for z in y:
                        op = SymmOp.from_xyz_string(z)
                        # Convert non-orthogonal trigonal/hexagonal operations
                        if convert: op = t2h * op * t2h.inverse
                        if not molecular:
                            symmetry[-1][-1].append(op)
                        else:
                            op = SymmOp.from_rotation_and_translation(
                                op.rotation_matrix, [0, 0, 0]
                            )
                            symmetry[-1][-1].append(op)
        else:
            symmetry.append([])
            # Loop over points in WP
            for y in x:
                symmetry[-1].append([])
                # Loop over ops
                for z in y:
                    op = SymmOp.from_xyz_string(z)
                    if convert:
                        # Convert non-orthogonal trigonal/hexagonal operations
                        op = t2h * op * t2h.inverse
                    if not molecular:
                        symmetry[-1][-1].append(op)
                    else:
                        op = SymmOp.from_rotation_and_translation(
                            op.rotation_matrix, [0, 0, 0]
                        )
                        symmetry[-1][-1].append(op)
    return symmetry


def get_layer_symmetry(num, molecular=False):
    """
    Returns a list of Wyckoff position site symmetry for a given space group.
    - 1st index: index of WP in group (0 is the WP with largest multiplicity)
    - 2nd index: a point within the WP
    - 3rd index: a site symmetry SymmOp of the point

    Args:
        num: the layer group number
        molecular: whether or not to return the Euclidean point symmetry
            operations. If True, cuts off translational part of operation, and
            converts non-orthogonal operations (3-fold and 6-fold rotations)
            to (orthogonal) pure rotations. Should be used when dealing with
            molecular crystals

    Returns:
        a 3d list of SymmOp objects representing the site symmetry of each
        point in each Wyckoff position
    """

    symmetry_strings = eval(layer_symmetry_df["0"][num])
    symmetry = []
    convert = False
    if molecular and num >= 65: convert = True
    # Loop over Wyckoff positions
    for x in symmetry_strings:
        symmetry.append([])
        # Loop over points in WP
        for y in x:
            symmetry[-1].append([])
            # Loop over ops
            for z in y:
                op = SymmOp.from_xyz_string(z)
                if convert:
                    # Convert non-orthogonal trigonal/hexagonal operations
                    op = t2h * op * t2h.inverse
                if not molecular:
                    symmetry[-1][-1].append(op)
                else:
                    op = SymmOp.from_rotation_and_translation(
                        op.rotation_matrix, [0, 0, 0]
                    )
                    symmetry[-1][-1].append(op)
    return symmetry


def get_rod_symmetry(num, molecular=False):
    """
    Returns a list of Wyckoff position site symmetry for a given Rod group.
    1st index: index of WP in group (0 is the WP with largest multiplicity)
    2nd index: a point within the WP
    3rd index: a site symmetry SymmOp of the point

    Args:
        num: the Rod group number
        molecular: whether or not to return the Euclidean point symmetry
            operations. If True, cuts off translational part of operation, and
            converts non-orthogonal operations (3-fold and 6-fold rotations)
            to (orthogonal) pure rotations. Should be used when dealing with
            molecular crystals

    Returns:
        a 3d list of SymmOp objects representing the site symmetry of each
        point in each Wyckoff position
    """

    symmetry_strings = eval(rod_symmetry_df["0"][num])
    symmetry = []
    convert = False
    if molecular and num >= 42: convert = True
    # Loop over Wyckoff positions
    for x in symmetry_strings:
        symmetry.append([])
        # Loop over points in WP
        for y in x:
            symmetry[-1].append([])
            # Loop over ops
            for z in y:
                op = SymmOp.from_xyz_string(z)
                    # Convert non-orthogonal trigonal/hexagonal operations
                if convert: op = t2h * op * t2h.inverse
                if not molecular:
                    symmetry[-1][-1].append(op)
                else:
                    op = SymmOp.from_rotation_and_translation(
                        op.rotation_matrix, [0, 0, 0]
                    )
                    symmetry[-1][-1].append(op)
    return symmetry


def get_point_symmetry(num):
    """
    Returns a list of Wyckoff position site symmetry for a given point group.
    1st index: index of WP in group (0 is the WP with largest multiplicity)
    2nd index: a point within the WP
    3rd index: a site symmetry SymmOp of the point

    Args:
        num: the point group number
        molecular: whether or not to convert to Euclidean reference frame
            (for hexagonal lattices: point groups 16-27)

    Returns:
        a 3d list of SymmOp objects representing the site symmetry of each
        point in each Wyckoff position
    """
    symmetry_strings = eval(point_symmetry_df["0"][num])
    symmetry = []
    # Loop over Wyckoff positions
    for wp in symmetry_strings:
        symmetry.append([])
        # Loop over points in WP
        for point in wp:
            symmetry[-1].append([])
            # Loop over ops
            for m in point:
                op = SymmOp(m)
                symmetry[-1][-1].append(op)
    return symmetry


def get_wyckoff_generators(sg, PBC=[1, 1, 1], molecular=False):
    """
    Returns a list of Wyckoff generators for a given space group.
    1st index: index of WP in sg (0 is the WP with largest multiplicity)
    2nd index: a generator for the WP
    This function is useful for rotating molecules based on Wyckoff position,
    since special Wyckoff positions only encode positional information, but not
    information about the orientation. The generators for each Wyckoff position
    form a subset of the spacegroup's general Wyckoff position.
    
    Args:
        sg: the international spacegroup number
        PBC: A periodic boundary condition list, where 1 means periodic, 0 means not periodic.
            Ex: [1,1,1] -> full 3d periodicity, [0,0,1] -> periodicity along the z axis
        molecular: whether or not to return the Euclidean point symmetry
            operations. If True, cuts off translational part of operation, and
            converts non-orthogonal operations (3-fold and 6-fold rotations)
            to (orthogonal) pure rotations. Should be used when dealing with
            molecular crystals
    
    Returns:
        a 2d list of SymmOp objects which can be used to generate a Wyckoff position given a
        single fractional (x,y,z) coordinate
    """
    if PBC != [1, 1, 1]:
        coor = [0, 0, 0]
        for i, a in enumerate(PBC):
            if not a:
                coor[i] = 0.5
        coor = np.array(coor)
    wyckoffs = get_wyckoffs(sg, PBC=PBC)

    P = SymmOp.from_rotation_and_translation(
        [[1, -0.5, 0], [0, np.sqrt(3) / 2, 0], [0, 0, 1]], [0, 0, 0]
    )
    generator_strings = eval(wyckoff_generators_df["0"][sg])
    generators = []
    convert = False
    if molecular:
        if sg >= 143 and sg <= 194:
            convert = True
    # Loop over Wyckoff positions
    for x, w in zip(generator_strings, wyckoffs):
        if PBC != [1, 1, 1]:
            op = w[0]
            coor1 = op.operate(coor)
            invalid = False
            for i, a in enumerate(PBC):
                if not a:
                    if not abs(coor1[i] - 0.5) < 1e-2:
                        invalid = True
            if invalid == False:
                generators.append([])
                # Loop over ops
                for y in x:
                    op = SymmOp.from_xyz_string(y)
                    if convert:
                        # Convert non-orthogonal trigonal/hexagonal operations
                        op = P * op * P.inverse
                    if not molecular:
                        generators[-1].append(op)
                    else:
                        op = SymmOp.from_rotation_and_translation(
                            op.rotation_matrix, [0, 0, 0]
                        )
                        generators[-1].append(op)
        else:
            generators.append([])
            for y in x:
                op = SymmOp.from_xyz_string(y)
                if convert:
                    # Convert non-orthogonal trigonal/hexagonal operations
                    op = P * op * P.inverse
                if not molecular:
                    generators[-1].append(op)
                else:
                    op = SymmOp.from_rotation_and_translation(
                        op.rotation_matrix, [0, 0, 0]
                    )
                    generators[-1].append(op)
    return generators


def get_layer_generators(num, molecular=False):
    """
    Returns a list of Wyckoff generators for a given layer group.
    1st index: index of WP in group (0 is the WP with largest multiplicity)
    2nd index: a generator for the WP
    This function is useful for rotating molecules based on Wyckoff position,
    since special Wyckoff positions only encode positional information, but not
    information about the orientation. The generators for each Wyckoff position
    form a subset of the group's general Wyckoff position.
    
    Args:
        num: the layer group number
        molecular: whether or not to return the Euclidean point symmetry
            operations. If True, cuts off translational part of operation, and
            converts non-orthogonal operations (3-fold and 6-fold rotations)
            to (orthogonal) pure rotations. Should be used when dealing with
            molecular crystals
    
    Returns:
        a 2d list of SymmOp objects which can be used to generate a Wyckoff position given a
        single fractional (x,y,z) coordinate
    """

    P = SymmOp.from_rotation_and_translation(
        [[1, -0.5, 0], [0, np.sqrt(3) / 2, 0], [0, 0, 1]], [0, 0, 0]
    )
    generator_strings = eval(layer_generators_df["0"][num])
    generators = []
    convert = False
    if molecular is True:
        if num >= 65:
            convert = True
    # Loop over Wyckoff positions
    for x in generator_strings:
        generators.append([])
        # Loop over ops
        for y in x:
            op = SymmOp.from_xyz_string(y)
            if convert is True:
                # Convert non-orthogonal trigonal/hexagonal operations
                op = P * op * P.inverse
            if molecular is False:
                generators[-1].append(op)
            elif molecular is True:
                op = SymmOp.from_rotation_and_translation(op.rotation_matrix, [0, 0, 0])
                generators[-1].append(op)
    return generators


def get_rod_generators(num, molecular=False):
    """
    Returns a list of Wyckoff generators for a given Rod group.
    1st index: index of WP in group (0 is the WP with largest multiplicity)
    2nd index: a generator for the WP
    This function is useful for rotating molecules based on Wyckoff position,
    since special Wyckoff positions only encode positional information, but not
    information about the orientation. The generators for each Wyckoff position
    form a subset of the group's general Wyckoff position.
    
    Args:
        num: the Rod group number
        molecular: whether or not to return the Euclidean point symmetry
            operations. If True, cuts off translational part of operation, and
            converts non-orthogonal operations (3-fold and 6-fold rotations)
            to (orthogonal) pure rotations. Should be used when dealing with
            molecular crystals
    
    Returns:
        a 2d list of SymmOp objects which can be used to generate a Wyckoff position given a
        single fractional (x,y,z) coordinate
    """

    P = SymmOp.from_rotation_and_translation(
        [[1, -0.5, 0], [0, np.sqrt(3) / 2, 0], [0, 0, 1]], [0, 0, 0]
    )
    generator_strings = eval(rod_generators_df["0"][num])
    generators = []
    convert = False
    if molecular is True:
        if num >= 42:
            convert = True
    # Loop over Wyckoff positions
    for x in generator_strings:
        generators.append([])
        # Loop over ops
        for y in x:
            op = SymmOp.from_xyz_string(y)
            if convert is True:
                # Convert non-orthogonal trigonal/hexagonal operations
                op = P * op * P.inverse
            if molecular is False:
                generators[-1].append(op)
            elif molecular is True:
                op = SymmOp.from_rotation_and_translation(op.rotation_matrix, [0, 0, 0])
                generators[-1].append(op)
    return generators


def get_point_generators(num):
    """
    Returns a list of Wyckoff generators for a given point group.
    1st index: index of WP in group (0 is the WP with largest multiplicity)
    2nd index: a generator for the WP
    This function is useful for rotating molecules based on Wyckoff position,
    since special Wyckoff positions only encode positional information, but not
    information about the orientation. The generators for each Wyckoff position
    form a subset of the group's general Wyckoff position.
    
    Args:
        num: the Rod group number
        molecular: whether or not to convert to Euclidean reference frame
            (for hexagonal lattices: point groups 16-27)
    
    Returns:
        a 2d list of SymmOp objects which can be used to generate a Wyckoff position given a
        single fractional (x,y,z) coordinate
    """
    generator_strings = eval(point_generators_df["0"][num])
    generators = []
    # Loop over Wyckoff positions
    for x in generator_strings:
        generators.append([])
        # Loop over ops
        for y in x:
            op = SymmOp(y)
            generators[-1].append(op)
    return generators


def general_position(number, dim=3):
    """
    Returns a Wyckoff_position object for the general Wyckoff position of the given
    group.

    Args:
        number: the international number of the group
        dim: the dimension of the group 3: space group, 2: layer group, 1: Rod group

    Returns:
        a Wyckoff_position object for the general position
    """
    return Wyckoff_position.from_group_and_index(number, 0, dim=dim)


def site_symm(point, gen_pos, tol=1e-3, lattice=np.eye(3), PBC=None):
    """
    Given a point and a general Wyckoff position, return the list of symmetry
    operations leaving the point (coordinate or SymmOp) invariant. The returned
    SymmOps are a subset of the general position. The site symmetry can be used
    for determining the Wyckoff position for a set of points, or for
    determining the valid orientations of a molecule within a given Wyckoff
    position.

    Args:
        point: a 1x3 coordinate or SymmOp object to find the symmetry of. If a
            SymmOp is given, the returned symmetries must also preserve the
            point's orientaion
        gen_pos: the general position of the spacegroup. Can be a Wyckoff_position
            object or list of SymmOp objects.
            Can be obtained using general_position()
        tol:
            the numberical tolerance for determining equivalent positions and
            orientations.
        lattice:
            a 3x3 matrix representing the lattice vectors of the unit cell
        PBC: A periodic boundary condition list, where 1 means periodic, 0 means not periodic.
            Ex: [1,1,1] -> full 3d periodicity, [0,0,1] -> periodicity along the z axis.
            Need not be defined here if gen_pos is a Wyckoff_position object.

    Returns:
        a list of SymmOp objects which leave the given point invariant
    """
    if PBC == None:
        if type(gen_pos) == Wyckoff_position:
            PBC = gen_pos.PBC
        else:
            PBC = [1, 1, 1]
    # Convert point into a SymmOp
    if type(point) != SymmOp:
        point = SymmOp.from_rotation_and_translation(
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]], np.array(point)
        )
    symmetry = []
    for op in gen_pos:
        is_symmetry = True
        # Calculate the effect of applying op to point
        difference = SymmOp((op * point).affine_matrix - point.affine_matrix)
        # Check that the rotation matrix is unaltered by op
        if not np.allclose(
            difference.rotation_matrix, np.zeros((3, 3)), rtol=1e-3, atol=1e-3
        ):
            is_symmetry = False
        # Check that the displacement is less than tol
        displacement = difference.translation_vector
        if distance(displacement, lattice, PBC=PBC) > tol:
            is_symmetry = False
        if is_symmetry:
            """The actual site symmetry's translation vector may vary from op by
            a factor of +1 or -1 (especially when op contains +-1/2).
            We record this to distinguish between special Wyckoff positions.
            As an example, consider the point (-x+1/2,-x,x+1/2) in position 16c
            of space group Ia-3(206). The site symmetry includes the operations
            (-z+1,x-1/2,-y+1/2) and (y+1/2,-z+1/2,-x+1). These operations are
            not listed in the general position, but correspond to the operations
            (-z,x+1/2,-y+1/2) and (y+1/2,-z+1/2,-x), respectively, just shifted
            by (+1,-1,0) and (0,0,+1), respectively.
            """
            el = SymmOp.from_rotation_and_translation(
                op.rotation_matrix, op.translation_vector - np.round(displacement)
            )
            symmetry.append(el)
    return symmetry

def check_wyckoff_position(points, group, tol=1e-3):
    """
    Given a list of points, returns a single index of a matching Wyckoff
    position in the space group. Checks the site symmetry of each supplied
    point against the site symmetry for each point in the Wyckoff position.
    Also returns a point which can be used to generate the rest using the
    Wyckoff position operators
    Args:
        points: a list of 3d coordinates or SymmOps to check
        group: a Group object
        tol: the max distance between equivalent points
    Returns:
        index, p: index is a single index for the Wyckoff position within
        the sg. If no matching WP is found, returns False. point is a
        coordinate taken from the list points. When plugged into the Wyckoff
        position, it will generate all the other points.
    """
    points = np.array(points)
    wyckoffs = group.wyckoffs
    w_symm_all = group.w_symm
    PBC = group.PBC
    # new method
    # Store the squared distance tolerance
    t = tol ** 2
    # Loop over Wyckoff positions
    for i, wp in enumerate(wyckoffs):
        # Check that length of points and wp are equal
        if len(wp) != len(points):
            continue
        failed = False

        # Search for a generating point
        for p in points:
            failed = False
            # Check that point works as x,y,z value for wp
            xyz = filtered_coords_euclidean(wp[0].operate(p) - p, PBC=PBC)

            if xyz.dot(xyz) > t:
                continue
            # Calculate distances between original and generated points
            pw = np.array([op.operate(p) for op in wp])
            dw = distance_matrix(points, pw, None, PBC=PBC, metric="sqeuclidean")

            # Check each row for a zero
            for row in dw:
                num = (row < t).sum()
                if num < 1:
                    failed = True
                    break

            if failed is True:
                continue
            # Check each column for a zero
            for column in dw.T:
                num = (column < t).sum()
                if num < 1:
                    failed = True
                    break

            # Calculate distance between original and generated points
            ps = np.array([op.operate(p) for op in w_symm_all[i][0]])
            ds = distance_matrix([p], ps, None, PBC=PBC, metric="sqeuclidean")
            # Check whether any generated points are too far away
            num = (ds > t).sum()
            if num > 0:
                failed = True

            if failed is True:
                continue
            return i, p
    return False, None

def get_symbol_and_number(input_group, dim=3):
    """
    Function for quick conversion between symbols and numbers

    Args:
        input_group: the group symbol or international number
        dim: the periodic dimension of the group
    """

    keys = {
        3: "space_group",
        2: "layer_group",
        1: "rod_group",
        0: "point_group",
    }

    found = False
    lists = symbols[keys[dim]]
    number = None
    symbol = None
    if dim not in [0, 1, 2, 3]:
        raise ValueError("Dimension ({:d}) should in [0, 1, 2, 3] ".format(dim))

    if type(input_group) == str:
        for i, _symbol in enumerate(lists):
            if _symbol == input_group:
                number = i + 1
                symbol = input_group
                return symbol, number
        msg = "({:s}) not found in {:s} ".format(input_group, keys[dim])
        raise ValueError(msg)
    else:
        valid, msg = check_symmetry_and_dim(input_group, dim)
        if not valid:
            raise ValueError(msg)
        else:
            number = input_group
            symbol = lists[number - 1]
            return symbol, number

def check_symmetry_and_dim(number, dim=3):
    """
    check if it is a valid number for the given symmetry
    
    Args:
        number: int
        dim: 0, 1, 2, 3
    """
    valid = True
    msg = 'This is a valid group number'

    numbers = [56, 75, 80, 230]
    if dim not in [0, 1, 2, 3]:
        msg = "invalid dimension {:d}".format()
        valid = False
    else:
        max_num = numbers[dim]
        if number not in range(1, max_num+1):
            valid = False
            msg = "invalid symmetry group {:d}".format(number)
            msg += " in dimension {:d}".format(dim)
    return valid, msg

def get_pbc_and_lattice(number, dim):
    if dim == 3:
        PBC = [1, 1, 1]
        if number <= 2:
            lattice_type = "triclinic"
        elif number <= 15:
            lattice_type = "monoclinic"
        elif number <= 74:
            lattice_type = "orthorhombic"
        elif number <= 142:
            lattice_type = "tetragonal"
        elif number <= 194:
            lattice_type = "hexagonal"
        elif number <= 230:
            lattice_type = "cubic"
    elif dim == 2:
        PBC = [1, 1, 0]
        if number <= 2:
            lattice_type = "triclinic"
        elif number <= 18:
            lattice_type = "monoclinic"
        elif number <= 48:
            lattice_type = "orthorhombic"
        elif number <= 64:
            lattice_type = "tetragonal"
        elif number <= 80:
            lattice_type = "hexagonal"
    elif dim == 1:
        PBC = [0, 0, 1]
        if number <= 2:
            lattice_type = "triclinic"
        elif number <= 12:
            lattice_type = "monoclinic"
        elif number <= 22:
            lattice_type = "orthorhombic"
        elif number <= 41:
            lattice_type = "tetragonal"
        elif number <= 75:
            lattice_type = "hexagonal"
    elif dim == 0:
        PBC = [0, 0, 0]
        # "C1", "Ci", "D2", "D2h", "T", "Th",
        # "O", "Td", "Oh", "I", "Ih",
        if number in [1, 2, 6, 8, 28, 29, 30, 31, 32, 55, 56]:
            lattice_type = "spherical"
        else:
            lattice_type = "ellipsoidal"
    return PBC, lattice_type

def search_matched_position(G, wp, pos):
    """
    search generator for a special Wyckoff position

    Args:
        G: space group number or Group object
        wp: Wyckoff object
        pos: initial xyz position

    Return:
        pos1: the position that matchs the standard setting
    """
    wp0 = G[0]
    match = False

    for op in wp0:
        pos1 = op.operate(pos)
        pos0 = wp[0].operate(pos1)
        diff = pos1 - pos0
        diff -= np.round(diff)
        diff = np.abs(diff)
        #print(wp.letter, pos1, pos0, diff)
        if diff.sum()<1e-2:
            pos1 -= np.floor(pos1)
            match = True
            break
    if match:
        return pos1
    else:
        return None

def search_matched_positions(G, wp, pos):
    """
    search generator for a special Wyckoff position

    Args:
        G: space group number or Group object
        wp: Wyckoff object
        pos: initial xyz position

    Return:
        pos1: the position that matchs the standard setting
    """
    wp0 = G[0]
    coords = []

    for op in wp0:
        pos1 = op.operate(pos)
        pos0 = wp[0].operate(pos1)
        diff = pos1 - pos0
        diff -= np.round(diff)
        diff = np.abs(diff)
        #print(wp.letter, pos1, pos0, diff)
        if diff.sum()<1e-2:
            pos1 -= np.floor(pos1)
            coords.append(pos1)
    return coords

def search_cloest_wp(G, wp, op, pos):
    """
    For a given position, search for the cloest wp which
    satisfies the desired symmetry relation
    e.g., for pos (0.1, 0.12, 0.2) and op (x, x, z)
    the closest match is (0.11, 0.11, 0.2)

    Args:
        G: space group number or Group object
        wp: Wyckoff object
        op: symmetry operation belonging to wp 
        pos: initial xyz position

    Return:
        pos1: the position that matchs symmetry operation
    """
    #G = Group(wp.number)
    if np.linalg.matrix_rank(op.rotation_matrix) == 0:
        # fixed point (e.g, 1/2, 1/2, 1/2)
        return op.translation_vector
    elif np.linalg.matrix_rank(op.rotation_matrix) == 3:
        # fully independent, e.g., (x,y,z), (-x,y,z)
        return pos
    else:
        # check if this is already matched
        coords = search_matched_positions(G, wp, pos)
        if len(coords)>0:
            diffs = []
            for coord in coords:
                tmp = op.operate(coord)
                diff1 = tmp - pos
                diff1 -= np.round(diff1)
                dist = np.linalg.norm(diff1) 
                if dist < 1e-3:
                    return tmp
                else:
                    diffs.append(dist)
            minID = np.argmin(diffs)
            return op.operate(coords[minID])

        # if not match, search for the closest solution
        else:
            wp0 = G[0]
            # extract all possible xyzs
            all_xyz = apply_ops(pos, wp0)[1:]
            dists = all_xyz - pos
            dists -= np.round(dists)
            ds = np.linalg.norm(dists, axis=1)
            ids = np.argsort(ds)
            for id in ids:
                d = all_xyz[id] - pos
                d -= np.round(d)
                res = pos + d/2
                if search_matched_position(G, wp, res) is not None:
                    #print(ds[id], pos, res)
                    return res
            return op.operate(pos)


def get_point_group(number):
    """
    return the point group for the given space group
    """

    if number == 1:
        return '1'
    elif number == 2:
        return '-1'
    elif 3 <= number <= 5:
        return '2'
    elif 6 <= number <= 9:
        return 'm'
    elif 10 <= number <= 15:
        return '2/m'
    elif 16 <= number <= 24:
        return '222'
    elif 25 <= number <= 46:
        return 'mm2'
    elif 47 <= number <= 74:
        return 'mmm'
    elif 75 <= number <= 80:
        return '4'
    elif 81 <= number <= 82:
        return '-4'
    elif 83 <= number <= 88:
        return '4/m'
    elif 89 <= number <= 98:
        return '422'
    elif 99 <= number <= 110:
        return '4mm'
    elif 111 <= number <= 122:
        return '-42m'
    elif 123 <= number <= 142:
        return '4/mmm'
    elif 143 <= number <= 146:
        return '3'
    elif 147 <= number <= 148:
        return '-3'
    elif 149 <= number <= 155:
        return '32'
    elif 156 <= number <= 161:
        return '3m'
    elif 162 <= number <= 167:
        return '-3m'
    elif 168 <= number <= 173:
        return '6'
    elif number == 174:
        return '-6'
    elif 175 <= number <= 176:
        return '6/m'
    elif 177 <= number <= 182:
        return '622'
    elif 183 <= number <= 186:
        return '6mm'
    elif 187 <= number <= 190:
        return '-6m2'
    elif 191 <= number <= 194:
        return '6/mmm'
    elif 195 <= number <= 199:
        return '23'
    elif 200 <= number <= 206:
        return 'm-3'
    elif 207 <= number <= 214:
        return '432'
    elif 215 <= number <= 220:
        return '-43m'
    elif 221 <= number <= 230:
        return 'm-3m'

