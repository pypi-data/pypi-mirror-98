# -*- coding: utf-8 -*-

"""Main module."""

import lammps_step


class MinimizationStep(object):
    my_description = {
        'description': 'Minimization',
        'group': 'Calculations',
        'name': 'Minimization'
    }

    def __init__(self, flowchart=None, gui=None):
        """Initialize this helper class, which is used by
        the application via stevedore to get information about
        and create node objects for the flowchart
        """
        pass

    def description(self):
        """Return a description of what this extension does
        """
        return MinimizationStep.my_description

    def create_node(self, flowchart=None, **kwargs):
        """Return the new node object"""
        return lammps_step.Minimization(flowchart=flowchart, **kwargs)

    def create_tk_node(self, canvas=None, **kwargs):
        """Return the graphical Tk node object"""
        return lammps_step.TkMinimization(canvas=canvas, **kwargs)
