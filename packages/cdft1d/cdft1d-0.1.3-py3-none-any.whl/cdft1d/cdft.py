#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module provides collection
of routines for potential calculations
"""

from types import SimpleNamespace

import numpy as np

from cdft1d.coulomb import compute_short_range_coul_pot, compute_long_range_coul_pot
from cdft1d.input import get_solvent_model, read_parameters
from cdft1d.lj import compute_lj_potential
from cdft1d.plot import simple_plot, simple_2_plot
from cdft1d.rad_fft import fft_rgrid_iv, fft_kgrid_to_rgrid, fft_kgrid_iv, RadFFT
from cdft1d.structure_factor import load_structure_factor

from cdft1d.diis import Diis, diis_session
from timeit import timeit

kb=8.31441e-3

DEFAULT_PARAMS = {'temp': 500,
                  'solvent': '2site',
                  'diis_iterations': 2,
                  'tol': 1.0E-9,
                  'max_iter': 4}

HEADER = """
==================================
1D RISM PROGRAM

Marat Valiev and Gennady Chuev
==================================
"""

def rism_solver(name, q, sigma, eps, **kwargs):


    params = {**DEFAULT_PARAMS, **kwargs}

    print(HEADER)
    print('System parameters:')
    for k, v in params.items():
        print('  ', k,v)
    print('')
    print('Solute parameters:')
    print(F'   {name} charge={q} sigma={sigma} epsion={eps}')

    temp  = int(params['temp'])
    ndiis = int(params['diis_iterations'])
    solvent_model = params['solvent']
    tol = float(params['tol'])
    max_iter = int(params['max_iter'])

    beta = 1.0/(kb*temp)

    qs = q
    sig_s = sigma
    eps_s = eps

    # load solvent model
    solvent_model = get_solvent_model(solvent_model)

    dr    = solvent_model.dr
    ngrid = solvent_model.ngrid
    sig_v = solvent_model.sigma
    eps_v = solvent_model.eps
    qv    = solvent_model.charge
    s_k   = solvent_model.s_k

    rgrid = fft_rgrid_iv(dr, ngrid)
    kgrid = fft_kgrid_iv(dr, ngrid)

    # initialize fft
    ifft = RadFFT(dr, ngrid)

    # calculate lj potential
    v_lj_r    = compute_lj_potential(sig_s, eps_s, sig_v, eps_v, rgrid)

    # coulomb long and short range
    vl_k     = compute_long_range_coul_pot(qs, qv, kgrid)
    v_rcoul_r = compute_short_range_coul_pot(qs, qv, rgrid)

    # total short range potential
    vs_r = v_rcoul_r + v_lj_r

    # compute long range part of h as -beta S*v_l
    hl_k = -beta*np.einsum('abn,bn->an', s_k, vl_k)
    hl_r = np.apply_along_axis(ifft.to_rspace, 1, hl_k)

    diis_update = diis_session()

    # initial guess for gamma
    g_r = np.zeros(s_k[0].shape)
    print('')
    print("Entering self-consistent cycle")
    print(f"{'iter':<5} {'error':<10.6}")
    i_out = 0
    for it in range(max_iter):

        c_r = np.exp(-beta*vs_r + g_r ) - g_r - 1.0
        c_k = np.apply_along_axis(ifft.to_kspace, 1, c_r)

        h_k = np.einsum('abn,bn->an', s_k, c_k)
        h_r = np.apply_along_axis(ifft.to_rspace, 1, h_k)

        # new guess for gamma
        gn_r = hl_r + h_r - c_r

        # compute error
        dg_r = gn_r - g_r
        err = np.sum(dg_r**2)
        err = np.sqrt(err/gn_r.size)
        if (it - i_out) == 10:
            print(f"{it:<5} {err:<10.6}")
            # print(it, err)
            i_out = it

        if err < tol:
            print('Converged!')
            break

        g_r = diis_update(2,gn_r, dg_r)

    result = SimpleNamespace()
    result.err = err

    cdft_write_rdf(name, solvent_model.name, rgrid, h_r+hl_r )
    return result


def cdft_write_rdf(solute_name, solvent_name, rgrid, h_r):
    print("\nGenerating RDFs")
    for i in range(len(solvent_name)):
        prefix = f'{solute_name}{solvent_name[i]}'
        rdf_file_name = f'{solute_name}{solvent_name[i]}.rdf'
        print(F"{rdf_file_name}")
        with open(rdf_file_name,'w') as fp:
            fp.write(f"{'# r':<10} {'g(r)':<10}\n")

            for j in range(len(rgrid)):
                r = rgrid[j]
                rdf = h_r[i, j] - h_r[i, 0]
                fp.write(f"{r:<10.4} {rdf:<10.4}\n")


def rism_solver1(q, sigma, eps, **kwargs):

    params = {**DEFAULT_PARAMS, **kwargs}

    temp  = int(params['temp'])
    ndiis = int(params['diis_iterations'])
    solvent_model = params['solvent']
    tol = float(params['tol'])
    max_iter = int(params['max_iter'])

    beta = 1.0/(kb*temp)

    qs = q
    sig_s = sigma
    eps_s = eps

    # load solvent model
    solvent_model = get_solvent_model(solvent_model)

    dr    = solvent_model.dr
    ngrid = solvent_model.ngrid
    sig_v = solvent_model.sigma
    eps_v = solvent_model.eps
    qv    = solvent_model.charge
    s_k   = solvent_model.s_k

    rgrid = fft_rgrid_iv(dr, ngrid)
    kgrid = fft_kgrid_iv(dr, ngrid)

    # initialize fft
    ifft = RadFFT(dr, ngrid)

    # calculate lj potential
    v_lj_r    = compute_lj_potential(sig_s, eps_s, sig_v, eps_v, rgrid)

    # coulomb long and short range
    vl_k     = compute_long_range_coul_pot(qs, qv, kgrid)
    v_rcoul_r = compute_short_range_coul_pot(qs, qv, rgrid)

    # total short range potential
    vs_r = v_rcoul_r + v_lj_r

    # compute long range part of h as -beta S*v_l
    hl_k = -beta*np.einsum('abn,bn->an', s_k, vl_k)
    hl_r = np.apply_along_axis(ifft.to_rspace, 1, hl_k)

    diis_update = diis_session()

    # initial guess for gamma
    g_r = np.zeros(s_k[0].shape)

    for it in range(max_iter):

        gn_r = rism_update(beta,g_r,vs_r, hl_r, s_k, ifft)

        # compute error
        dg_r = gn_r - g_r
        err = np.sum(dg_r**2)
        err = np.sqrt(err/gn_r.size)
        print(err)
        if err < tol:
            print('Converged!')
            break

        g_r = diis_update(2,gn_r, dg_r)

    result = SimpleNamespace()
    result.err = err
    return result

def rism_update(beta, g_r, vs_r, hl_r, s_k, ifft):

    c_r = np.exp(-beta*vs_r + g_r ) - g_r - 1.0
    c_k = np.apply_along_axis(ifft.to_kspace, 1, c_r)

    h_k = np.einsum('abn,bn->an', s_k, c_k)
    h_r = np.apply_along_axis(ifft.to_rspace, 1, h_k)

    g_new_r = hl_r + h_r - c_r
    return g_new_r

if __name__ == '__main__':

    # t = timeit(stmt=rism_solver,number=1)
    # print(f'{t=}')
    # t = timeit(stmt=rism_solver1,number=1)
    # print(f'{t=}')

    params = read_parameters('../data/input.dat')

    result = rism_solver('Na',1.0, 2.16, 1.4755, **params)

    # print(f'{result.err=}')
    #
    # result = rism_solver('Na', 1.0, 2.16, 1.4755, **params)
    #
    # print(f'{result.err=}')
    #
    # # rism_solver1()