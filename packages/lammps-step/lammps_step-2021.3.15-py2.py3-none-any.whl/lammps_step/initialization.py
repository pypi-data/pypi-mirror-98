# -*- coding: utf-8 -*-

"""A single-point initialization in LAMMPS"""

import seamm_ff_util
import lammps_step
import logging
import seamm
import seamm_util
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __
import pprint

logger = logging.getLogger('lammps')
job = printing.getPrinter()
printer = printing.getPrinter('lammps')

msm_pair_styles = ['born', 'buck', '', 'lj/charmm', 'lj/cut']

thermo_variables = [
    'step', 'elapsed', 'elaplong', 'dt', 'time', 'cpu', 'tpcpu', 'spcpu',
    'cpuremain', 'part', 'timeremain', 'atoms', 'temp', 'press', 'pe', 'ke',
    'etotal', 'enthalpy', 'evdwl', 'ecoul', 'epair', 'ebond', 'eangle',
    'edihed', 'eimp', 'emol', 'elong', 'etail', 'vol', 'density', 'lx', 'ly',
    'lz', 'xlo', 'xhi', 'ylo', 'yhi', 'zlo', 'zhi', 'xy', 'xz', 'yz', 'xlat',
    'ylat', 'zlat', 'bonds', 'angles', 'dihedrals', 'impropers', 'pxx', 'pyy',
    'pzz', 'pxy', 'pxz', 'pyz', 'fmax', 'fnorm', 'nbuild', 'ndanger', 'cella',
    'cellb', 'cellc', 'cellalpha', 'cellbeta', 'cellgamma'
]


class Initialization(seamm.Node):

    def __init__(self, flowchart=None, title='Initialization', extension=None):
        """Initialize the node"""

        logger.debug('Creating Initialization {}'.format(self))

        super().__init__(flowchart=flowchart, title=title, extension=extension)

        self.description = []
        self.parameters = lammps_step.InitializationParameters()

    @property
    def header(self):
        """A printable header for this section of output"""
        return (
            'Step {}: {}'.format(
                '.'.join(str(e) for e in self._id), self.title
            )
        )

    @property
    def version(self):
        """The semantic version of this module.
        """
        return lammps_step.__version__

    @property
    def git_revision(self):
        """The git version of this module.
        """
        return lammps_step.__git_revision__

    @property
    def kspace_methods(self):
        """The list of avilable methods"""
        return list(lammps_step.kspace_methods)

    def description_text(self, P=None):
        """Return a short description of this step.

        Return a nicely formatted string describing what this step will
        do.

        Keyword arguments:
            P: a dictionary of parameter values, which may be variables
                or final values. If None, then the parameters values will
                be used as is.
        """

        if not P:
            P = self.parameters.values_to_dict()

        text = 'Initialize the calculation with a cutoff of {cutoff} Å'
        if P['shift_nonbond']:
            text += ', shifting the nonbond energies to 0 at the cutoff'
        text += '. If the system is periodic'
        if P['kspace_method'][0] == '$':
            text += " use the variable '{method}' to determine whether "
            text += "and how to accelerate the k-space summations."
        elif P['kspace_method'] == 'none':
            text += ' no k-space acceleration method will be used.'
        elif P['kspace_method'] == 'automatic':
            text += ' the best k-space acceleration method for the '
            text += ' molecular system will be chosen.'
        else:
            text += ' the {method} for k-space acceleration will be used.'

        if P['kspace_method'] != 'none':
            text += ' The accuracy goal is {kspace_accuracy}.'

        return self.header + '\n' + __(text, **P, indent=4 * ' ').__str__()

    def get_input(self, extras=None):
        """Get the input for the initialization of LAMMPS"""

        self.description = []
        self.description.append('   ' + self.header)

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Fix some things
        P['cutoff'] = P['cutoff'].to('angstrom').magnitude

        # Get the system
        system_db = self.get_variable('_system_db')
        configuration = system_db.system.configuration

        # See what type of forcefield we have amd handle it
        ff = self.get_variable('_forcefield')
        if ff == 'OpenKIM':
            lammps_step.set_lammps_unit_system('metal')
            return self.OpenKIM_input()

        # Valence forcefield...
        ffname = ff.current_forcefield
        n_atoms = configuration.n_atoms

        # And atom-type if necessary
        key = f'atom_types_{ffname}'
        if key not in configuration.atoms:
            smiles = configuration.to_smiles(hydrogens=True)
            logger.debug('Atom typing -- smiles = ' + smiles)
            ff_assigner = seamm_ff_util.FFAssigner(ff)
            atom_types = ff_assigner.assign(smiles, add_hydrogens=False)

            logger.info('Atom types: ' + ', '.join(atom_types))

            configuration.atoms.add_attribute(
                key, coltype='str', values=atom_types
            )

            printer.important(
                __(
                    f"Assigned the atom types for forcefield '{ffname}' to "
                    "the system",
                    indent=self.indent + '    '
                )
            )

            # Now get the charges if forcefield has them.
            terms = ff.terms
            if 'bond charge increment' in terms:
                logger.debug('Getting the charges for the system')
                neighbors = configuration.bonded_neighbors(as_indices=True)

                charges = []
                total_q = 0.0
                for i in range(configuration.n_atoms):
                    itype = atom_types[i]
                    parameters = ff.charges(itype)[3]
                    q = float(parameters['Q'])
                    for j in neighbors[i]:
                        jtype = atom_types[j]
                        parameters = ff.bond_increments(itype, jtype)[3]
                        q += float(parameters['deltaij'])
                    charges.append(q)
                    total_q += q
                if abs(total_q) > 0.0001:
                    logger.warning(f'Total charge is not zero: {total_q:.4f}')
                    logger.info(
                        'Charges from increments and charges:\n' +
                        pprint.pformat(charges)
                    )
                else:
                    logger.debug(
                        'Charges from increments:\n' + pprint.pformat(charges)
                    )

                key = f'charges_{ffname}'
                if key not in configuration.atoms:
                    configuration.atoms.add_attribute(key, coltype='float')
                charge_column = configuration.atoms.get_column(key)
                charge_column[0:] = charges
                logger.debug(f"Set column '{key}' to the charges")

        # Get the energy expression.
        eex = ff.energy_expression(configuration, style='LAMMPS')
        logger.debug('energy expression:\n' + pprint.pformat(eex))

        # Determine if we have any charges, and if so, if they are sparse
        key = f'charges_{ffname}'
        if key in configuration.atoms:
            charges = [*configuration.atoms[key]]
            n_charged_atoms = 0
            smallq = float(P['kspace_smallq'])
            for charge in charges:
                if abs(charge) > smallq:
                    n_charged_atoms += 1
            fraction_charged_atoms = n_charged_atoms / n_atoms
        else:
            n_charged_atoms = 0

        lines = []
        lines.append('')
        lines.append('#     initialization of LAMMPS')
        lines.append('')
        lines.append('units               real')

        periodicity = configuration.periodicity
        if periodicity == 0:
            lines.append('boundary            s s s')
            string = 'Setup for a molecular (non-periodic) system.'
        elif periodicity == 3:
            lines.append('boundary            p p p')
            tail_correction = 'yes' if P['tail_correction'] and \
                              not P['shift_nonbond'] else 'no'
            string = 'Setup for a periodic (crystalline or fluid) system.'
        else:
            raise RuntimeError(
                'The LAMMPS step can only handle 0-'
                ' or 3-D periodicity at the moment!'
            )

        lines.append('atom_style          full')
        lines.append('newton              on')
        if n_atoms < 20:
            # LAMMPS has problems with bins for small systems
            lines.append('neighbor            2.0 nsq')
        lines.append('')
        lines.append('#    define the style of forcefield')
        lines.append('')

        terms = ff.ff['terms']

        logging.debug(
            'LAMMPS initialization, terms = \n' + pprint.pformat(terms)
        )

        # control of nonbonds
        nonbond_term = None
        if 'pair' in terms:
            if len(terms['pair']) != 1:
                raise RuntimeError('Cannot handle multiple nonbond terms yet!')
            nonbond_term = terms['pair'][0]

        if nonbond_term is None:
            pprint.pprint(terms)
            raise RuntimeError("Cannot find nonbond term in forcefield!")

        if nonbond_term == 'nonbond(9-6)':
            pair_style_base = 'lj/class2'
            mixing = 'sixthpower'
        elif nonbond_term == 'nonbond(12-6)':
            pair_style_base = 'lj/cut'
            # What type of mixing rule?
            modifiers = ff.ff['modifiers']['nonbond(12-6)']
            mixing = ''
            for section in modifiers:
                for item in modifiers[section]:
                    if 'combination' in item:
                        if mixing == '':
                            mixing = item.split()[1]
                        if mixing != item.split()[1]:
                            raise RuntimeError(
                                'Conflicting combination rules in '
                                "nonbond(12-6) section '" + section + "'"
                            )
            if mixing == "":
                mixing = 'geometric'
        else:
            raise RuntimeError(
                "Can't handle nonbond term {} yet!".format(nonbond_term)
            )

        shift = 'yes' if P['shift_nonbond'] else 'no'
        if P['kspace_method'] == 'automatic':
            if periodicity == 3:
                kspace_style = ''
                if n_charged_atoms == 0:
                    pair_style = pair_style_base
                    string += (
                        ' The nonbonded interactions will be evaluated using '
                        'a cutoff of {cutoff} Å. Since there are no charges '
                        'on the atoms, no long-range coulomb method will be '
                        'used.'
                    )
                else:
                    string += (
                        ' The nonbonded interactions will be evaluated using '
                        'a cutoff of {cutoff} Å, with the long-range terms '
                    )
                    pair_style = pair_style_base + '/coul/long'
                    if n_atoms < P['ewald_atom_cutoff']:
                        kspace_style = 'ewald {}'.format(P['kspace_accuracy'])
                        string += (
                            'using the Ewald summation method with '
                            'an accuracy of {kspace_accuracy}.'
                        )
                    elif fraction_charged_atoms < \
                            P['charged_atom_fraction_cutoff']:
                        kspace_style = 'pppm/cg {} {}'.format(
                            P['kspace_accuracy'],
                            P['charged_atom_fraction_cutoff']
                        )
                        string += (
                            'using the PPPM method optimized for few '
                            'atoms with charges, with '
                            'an accuracy of {kspace_accuracy}.'
                        )
                    else:
                        kspace_style = 'pppm {}'.format(P['kspace_accuracy'])
                        string += (
                            'using the PPPM method with '
                            'an accuracy of {kspace_accuracy}.'
                        )
                lines.append(
                    'pair_style          {} {}'.format(
                        pair_style, P['cutoff']
                    )
                )
                lines.append(
                    'pair_modify         mix ' + mixing +
                    ' tail {} shift {}'.format(tail_correction, shift)
                )
                if shift:
                    string += (
                        ' The van der Waals terms will be shifted '
                        'to zero energy at the cutoff distance.'
                    )
                if tail_correction:
                    string += (
                        ' A long-range correction for the '
                        'van der Waals terms will be added.'
                    )
                if kspace_style != '':
                    lines.append('kspace_style        ' + kspace_style)
            else:
                kspace_style = ''
                if n_charged_atoms == 0:
                    pair_style = pair_style_base
                    string += (
                        ' The nonbonded interactions will be evaluated using '
                        'a simple cutoff of {cutoff} Å. Since there are no '
                        'charges on the atoms, no long-range coulomb method '
                        'will be used.'
                    )
                elif (
                    n_atoms > P['msm_atom_cutoff'] and
                    pair_style_base in msm_pair_styles
                ):
                    pair_style = pair_style_base + '/coul/msm'
                    string += (
                        'The nonbonded interactions will be handled with '
                        ' a cutoff of {cutoff} Å.'
                    )
                    if fraction_charged_atoms < \
                       P['charged_atom_fraction_cutoff']:
                        kspace_style = (
                            'msm/cg {kspace_accuracy} {kspace_smallq}'
                        )
                        string += (
                            ' The MSM method will be used to handle '
                            'the longer range coulombic interactions, using '
                            'the approach tuned for systems with few charges.'
                            'The accuracy goal is {kspace_accuracy}.'
                        )
                    else:
                        kspace_style = 'msm {kspace_accuracy}'
                        string += (
                            ' The MSM method will be used to handle '
                            'the longer range coulombic interactions.'
                            'The accuracy goal is {kspace_accuracy}.'
                        )
                else:
                    pair_style = pair_style_base + '/coul/cut'
                    string += (
                        'The nonbonded interactions will be handled with '
                        ' a simple cutoff of {cutoff} Å.'
                    )
                if shift:
                    string += (
                        ' The van der Waals terms will be shifted '
                        'to zero energy at the cutoff distance.'
                    )
                lines.append(
                    'pair_style          {} {}'.format(
                        pair_style, P['cutoff']
                    )
                )
                lines.append(
                    'pair_modify         mix ' + mixing +
                    ' shift {}'.format(shift)
                )
                if kspace_style != '':
                    lines.append(
                        'kspace_style        ' + kspace_style.format(**P)
                    )
            self.description.append(__(string, indent=7 * ' ', **P))
        else:
            if periodicity == 3:
                kspace_style = ''
                if n_charged_atoms == 0 or P['kspace_style'] == 'none':
                    pair_style = pair_style_base
                elif fraction_charged_atoms < \
                        P['charged_atom_fraction_cutoff']:
                    pair_style = pair_style_base + '/coul/long'
                    kspace_style = (
                        lammps_step.kspace_methods[P['kspace_method']].format(
                            **P
                        )
                    )
                lines.append(
                    'pair_style          {} {}'.format(
                        pair_style, P['cutoff']
                    )
                )
                lines.append(
                    'pair_modify         mix ' + mixing +
                    ' tail {} shift {}'.format(tail_correction, shift)
                )
                if kspace_style != '':
                    lines.append('kspace_style        ' + kspace_style)
            else:
                if n_charged_atoms == 0:
                    pair_style = pair_style_base
                else:
                    pair_style = pair_style_base + '/coul/cut'
                lines.append(
                    'pair_style          {} {}'.format(
                        pair_style, P['cutoff']
                    )
                )
                lines.append(
                    'pair_modify         mix ' + mixing +
                    ' shift {}'.format(shift)
                )
                if 'msm' in lammps_step.kspace_methods[P['kspace_method']]:
                    kspace_style = (
                        lammps_step.kspace_methods[P['kspace_method']].format(
                            **P
                        )
                    )
                    lines.append('kspace_style        ' + kspace_style)

        if 'bond' in terms and eex['n_bonds'] > 0:
            if len(terms['bond']) == 1:
                bond_style = lammps_step.bond_style[terms['bond'][0]]
                lines.append('bond_style          ' + bond_style)
            else:
                line = 'bond_style          hybrid'
                for term in terms['bond']:
                    line += ' ' + lammps_step.bond_style[term]
                lines.append(line)
        if 'angle' in terms and eex['n_angles'] > 0:
            if len(terms['angle']) == 1:
                angle_style = lammps_step.angle_style[terms['angle'][0]]
                lines.append('angle_style         ' + angle_style)
            else:
                line = 'angle_style         hybrid'
                for term in terms['angle']:
                    line += ' ' + lammps_step.angle_style[term]
                lines.append(line)
        if 'torsion' in terms and eex['n_torsions'] > 0:
            if len(terms['torsion']) == 1:
                #  yapf: disable
                dihedral_style = lammps_step.dihedral_style[terms['torsion'][0]]  # noqa: E501
                #  yapf: enable
                lines.append('dihedral_style      ' + dihedral_style)
            else:
                line = 'dihedral_style      hybrid'
                for term in terms['torsion']:
                    line += ' ' + lammps_step.dihedral_style[term]
                lines.append(line)
        if 'out-of-plane' in terms and eex['n_oops'] > 0:
            if len(terms['out-of-plane']) == 1:
                improper_style = lammps_step.improper_style[
                    terms['out-of-plane'][0]]
                lines.append('improper_style      ' + improper_style)
            else:
                line = 'improper_style      hybrid'
                for term in terms['out-of-plane']:
                    line += ' ' + lammps_step.improper_style[term]
                lines.append(line)

        lines.append('')
        if extras is not None and 'read_data' in extras and \
                extras['read_data'] is True:

            lines.append('read_data           structure.dat')

        # Set up standard variables
        for variable in thermo_variables:
            lines.append(
                'variable            {var} equal {var}'.format(var=variable)
            )

        return (lines, eex)

    def OpenKIM_input(self):
        """Create the initialization input for a calculation using OpenKIM.
        """
        # Get the configuration
        system_db = self.get_variable('_system_db')
        configuration = system_db.system.configuration

        # Get the (simple) energy expression for these systems
        eex = self.OpenKIM_energy_expression()

        lines = []
        lines.append('')
        lines.append('#     initialization of LAMMPS')
        lines.append('')
        lines.append('newton              on')
        lines.append('')
        potential = self.get_variable('_OpenKIM_Potential')
        lines.append(
            f'kim_init            {potential} metal '
            'unit_conversion_mode'
        )
        lines.append('')
        periodicity = configuration.periodicity
        if periodicity == 0:
            lines.append('boundary            s s s')
            string = 'Setup for a molecular (non-periodic) system.'
        elif periodicity == 3:
            lines.append('boundary            p p p')
            string = 'Setup for a periodic (crystalline or fluid) system.'
        else:
            raise RuntimeError(
                'The LAMMPS step can only handle 0-'
                ' or 3-D periodicity at the moment!'
            )
        lines.append('')
        lines.append('read_data           structure.dat')
        lines.append('')
        lines.append(f'kim_interactions    {" ".join(eex["atom types"])}')

        # Set up standard variables
        for variable in thermo_variables:
            lines.append(
                'variable            {var} equal {var}'.format(var=variable)
            )

        self.description.append(__(string, indent=self.indent + 4 * ' '))

        return (lines, eex)

    def OpenKIM_energy_expression(self):
        """Create the (simple) energy expression for OpenKIM models.
        """
        eex = {}
        eex['terms'] = {'OpenKIM': []}

        # Get the configuration
        system_db = self.get_variable('_system_db')
        configuration = system_db.system.configuration
        atoms = configuration.atoms

        # The elements (1-based!) Probably not used...
        elements = atoms.symbols
        eex['elements'] = ['']
        eex['elements'].extend(elements)

        # The periodicity & cell parameters
        periodicity = eex['periodicity'] = configuration.periodicity
        if periodicity == 3:
            eex['cell'] = configuration.cell.parameters

        result = eex['atoms'] = []
        atom_types = eex['atom types'] = []
        masses = eex['masses'] = []

        coordinates = atoms.get_coordinates(fractionals=False)
        for element, xyz in zip(elements, coordinates):
            if element in atom_types:
                index = atom_types.index(element) + 1
            else:
                atom_types.append(element)
                index = len(atom_types)
                masses.append(
                    (
                        seamm_util.element_data[element]['atomic weight'],
                        element
                    )
                )
            x, y, z = xyz
            result.append((x, y, z, index))

        eex['n_atoms'] = len(result)
        eex['n_atom_types'] = len(atom_types)

        return eex
