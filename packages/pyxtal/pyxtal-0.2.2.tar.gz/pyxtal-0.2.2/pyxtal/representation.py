"""
structure representation
"""

from rdkit.Chem.rdMolTransforms import CanonicalizeConformer
from rdkit import Chem
from operator import itemgetter

def ig(x):
    return itemgetter(x)

def cleaner(list_to_clean):
    """
    Remove duplicate torsion definion from a list of atom ind. tuples.
    """
    for_remove = []
    for x in reversed(range(len(list_to_clean))):
        for y in reversed(range(x)):
            ix1, ix2 = ig(1)(list_to_clean[x]), ig(2)(list_to_clean[x])
            iy1, iy2 = ig(1)(list_to_clean[y]), ig(2)(list_to_clean[y])
            if (ix1 == iy1 and ix2 == iy2) or (ix1 == iy2 and ix2 == iy1):
                for_remove.append(y)
    clean_list = [v for i, v in enumerate(list_to_clean)
                  if i not in set(for_remove)]
    return clean_list

def find_id_from_smile(smile):
    """
    Find the positions of rotatable bonds in the molecule.
    """
    smarts_torsion="[*]~[!$(*#*)&!D1]-&!@[!$(*#*)&!D1]~[*]"
    mol = Chem.MolFromSmiles(smiles)
    pattern_tor = Chem.MolFromSmarts(smarts_torsion)
    torsion = list(mol.GetSubstructMatches(pattern_tor))

    pattern_custom = Chem.MolFromSmarts(filter_smarts_torsion)
    custom = list(mol.GetSubstructMatches(pattern_custom))
    to_del_bef_custom = []

    for x in reversed(range(len(torsion))):
        for y in reversed(range(len(custom))):
            ix1, ix2 = ig(1)(torsion[x]), ig(2)(torsion[x])
            iy1, iy2 = ig(1)(custom[y]), ig(2)(custom[y])
            if (ix1 == iy1 and ix2 == iy2) or (ix1 == iy2 and
                                               ix2 == iy1):
                to_del_bef_custom.append(x)

    custom_torsion = copy(torsion)
    custom_torsion = [v for i, v in enumerate(custom_torsion)
                      if i not in set(to_del_bef_custom)]
    torsion = custom_torsion
    return cleaner(torsion)

# Standard Libraries
class representation():
    """
    Class for handling molecular crystal representation
    
    Args: 
        xtal: pyxtal object
    """

    def __init__(self, xtal):

        self.struc = xtal
        self.rep_cell = xtal.lattice.get_para(degree=True)
        self.rep_molecule = []
        for mol_site in xtal.mol_sites:
            rep = list(mol_site.position) 
            rep += list(mol_site.)

            self.rep_molecule.append(rep)

    def to_vector(self):


    def to_pyxtal(self):
        """
        rebuild the pyxtal from the 1D representation
        """
        new_struc = self.struc.copy()
        lattice = new_struc.lattice
        diag = new_struc.diag
        ori = 
        for i, site in enumerate(new_struc.mol_sites()):
            pos0 = np.array(self.rep_molecule[i][:3])
            ori = 
            
            mol_site(_mol, pos0, ori, wp, lattice, diag)


    def fit():

# zmatrix2xyz
# xyz2zmatrix
# compute rotation: https://github.com/charnley/rmsd

