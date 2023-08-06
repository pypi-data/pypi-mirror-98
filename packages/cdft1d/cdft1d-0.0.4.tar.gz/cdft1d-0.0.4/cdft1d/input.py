#!/usr/bin/python
# -*- coding: utf-8 -*-
from pathlib import Path
from types import SimpleNamespace
import numpy as np

from cdft1d.structure_factor import load_structure_factor

THIS_DIR = Path(__file__).resolve().parent
PROJ_DIR = THIS_DIR.parent
DATA_DIR = THIS_DIR / 'data'


def parse_input(filepath):

    file = Path(filepath)
    # file = DATA_DIR / 'input.dat'

    sites = read_sites(file,section_tag='<solute>')
    simulation = read_simulation(file)

    print(sites)

def get_solvent_model(model):

    file = F'{model}.smdl'
    try:
        grid = read_grid(file)
    except FileNotFoundError:
        file = DATA_DIR / F'{model}.smdl'
        grid = read_grid(file)

    sites = read_sites(file)

    nv = len(sites.name)
    ngrid = grid.ngrid

    structure_factor = read_structure_factor(nv, ngrid, file)

    solvent_model = sites
    solvent_model.s_k = structure_factor.s_k
    solvent_model.dr = grid.dr
    solvent_model.ngrid = ngrid
    solvent_model.nsites = nv

    return solvent_model


def iter_lines(fp):
    for line in fp:
        record = line.rsplit('#')[0].strip()
        if record == '':
            continue
        else:
            yield record


def read_grid(filename):
    grid = SimpleNamespace(dr=None, ngrid=None)
    with open(filename, 'r') as fp:
        find_section('<grid>', fp)
        for line in iter_lines(fp):
            if line.startswith('<'):
                break
            key, value = line.split()
            if key in {'dr'}:
                grid.dr = float(value)
            elif key in {'ngrid'}:
                grid.ngrid = int(value)

        return grid


def read_parameters(filename):

    parameters = {}

    with open(filename, 'r') as fp:
        find_section('<simulation>', fp)
        for line in iter_lines(fp):
            if line.startswith('<'):
                break
            key, value = line.split()
            parameters[key] = value
        return parameters

def read_simulation(filename):

    simulation = SimpleNamespace(solvent=None, temp=300, tol=1.0E-9)

    with open(filename, 'r') as fp:
        find_section('<simulation>', fp)
        for line in iter_lines(fp):
            if line.startswith('<'):
                break
            key, value = line.split()
            if key in {'solvent'}:
                simulation.solvent = value
            elif key in {'temp'}:
                simulation.temp = int(value)
            elif key in {'tol'}:
                simulation.tol = float(value)

        return simulation


def read_sites(filename, section_tag='<sites>'):
    sites = SimpleNamespace(name=[], charge=[], sigma=[], eps=[])

    name_list   = []
    sigma_list  = []
    eps_list    = []
    charge_list = []

    with open(filename, 'r') as fp:
        find_section(section_tag, fp)
        for line in iter_lines(fp):
            if line.startswith('<'):
                break
            name, sigma, eps, charge = line.split()
            name_list.append(name)
            sigma_list.append(float(sigma))
            eps_list.append(float(eps))
            charge_list.append(float(charge))

    return SimpleNamespace(
        name=np.array(name_list),
        sigma=np.array(sigma_list),
        eps=np.array(eps_list),
        charge=np.array(charge_list)
        )




def read_structure_factor(nv, ngrid, filename):
    structure_factor = SimpleNamespace(s_k=None, kgrid=None)
    with open(filename, 'r') as fp:
        find_section('<structure_factor>', fp)
        kgrid = np.zeros(shape=ngrid)
        s_k = np.zeros(shape=(nv, nv, ngrid), dtype=np.double)

        for ig, line in enumerate(iter_lines(fp)):
            if line.startswith('<'):
                break
            row = list(map(float, line.split()))
            kgrid[ig] = row[0]
            n = 1
            for i in range(nv):
                for j in range(i, nv):
                    s_k[i, j, ig] = row[n]
                    s_k[j, i, ig] = row[n]
                    n = n + 1

        structure_factor.s_k = s_k
        structure_factor.kgrid = kgrid

        return structure_factor


def find_section(section, fp):
    for line in fp:
        if line.strip() == section:
            return


if __name__ == '__main__':
    file_name = '../data/solvent.data'
    print(read_parameters('../data/input.dat'))