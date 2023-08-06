#!/usr/bin/python
# -*- coding: utf-8 -*-
import click

from cdft1d.cdft import rism_solver
from cdft1d.input import read_parameters, read_sites


@click.command()
@click.argument('input_file')

def rism(input_file):
    parameters = read_parameters(input_file)
    sites = read_sites(input_file,section_tag='<solute>')

    name     = sites.name[0]
    sigma    = sites.sigma[0]
    eps      = sites.eps[0]
    charge   = sites.charge[0]

    rism_solver(name, charge, sigma, eps, **parameters)


if __name__ == '__main__':
    rism()