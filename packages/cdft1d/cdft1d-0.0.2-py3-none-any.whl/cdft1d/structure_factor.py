#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module provides collection
of routines related to structure factor
"""
import math
import logging
from collections import namedtuple

import numpy as np

logging.basicConfig(level=logging.INFO)

Grid = namedtuple('grid',['ng', 'ds', 'kind'])
StructureFactor = namedtuple('structure_factor', 'grid sk')


class LocalStore:
    file_name = None
    sk = None
    kgrid = None


def load_structure_factor(file_name=None):
    r"""
    Load kspace representation of the structure factor
    from the external file

    Args:
        file_name: name of the external file

    Returns:
        :math:`k(i)` - 1D numpy array of grid points in reciprocal k-space

    """

    if file_name is None:
        if LocalStore.file_name is None:
            raise ValueError
    elif LocalStore.file_name == file_name:
        logging.info("already exists")
    else:
        LocalStore.file_name = file_name
        LocalStore.sk, LocalStore.kgrid = read_structure_factor(file_name)

    return LocalStore.sk, LocalStore.kgrid


def read_structure_factor(file_name):
    r"""
    Read kspace representation of the structure factor
    from the external file

    """

    with open(file_name) as fp:
        lines = list(fp)

    # structure matrix size nv(nv+1)/2
    # nv is number of solvent sites
    nd = len(lines[0].split()) - 1
    nv = (math.sqrt(1+8*nd) - 1)/2
    if nv.is_integer():
        nv = int(nv)
    else:
        raise ValueError

    ngrid = len(lines)

    logging.debug(f'{ngrid=}')
    logging.debug(f'{nd=}')
    logging.debug(f'{nv=}')

    sk = np.zeros(shape=(nv, nv, ngrid),dtype=np.double)
    kgrid = np.zeros(shape=ngrid)

    for ig, line in enumerate(lines):
        row = list(map(float,line.split()))
        kgrid[ig] = row[0]
        n = 1
        for i in range(nv):
            for j in range (i, nv):
                sk[i, j, ig] = row[n]
                sk[j, i, ig] = row[n]
                n = n + 1

    return sk, kgrid

def compute_prod_structure_factor(c):
    r"""
    Compute product S*c
    """
    pass
    # np.einsum('ijk,jm', A, B)

if __name__ == '__main__':

    # sk, kgrid = load_structure_factor()
    sk, kgrid = load_structure_factor("../data/sk.data")
    nv = sk.shape[1]
    ng = sk.shape[2]
    c = np.ones([nv,ng])
    c[0,:] = kgrid
    c[1,:] = kgrid**2
    print(c)
    skc = np.einsum('ijk,jk->ik', sk, c)
    print(skc.shape)
    skc1 = np.zeros([nv,ng])
    for i in range(nv):
        for j in range(nv):
            for k in range(ng):
                skc1[i,k] = skc1[i,k] + sk[i,j,k]*c[j,k]

    np.testing.assert_array_equal(skc, skc1)