#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module provides collection
of routines for potential calculations
"""
from math import pi

import numpy as np
from scipy.special import erf


N_AVO = 6.02214179e+23
E_CHARGE = 4.803e-10
E_CHARGE_2 = 23.068809e-20
# CK = N_AVO * E_CHARGE ** 2 * 0.01
CK = 60.2214179*23.068809


def compute_gauss_pot_kspace(kgrid,  r_smear=1.25):
    r"""
        Generates Coulomb potential of gaussian smeared density

        .. math::
            u_{l,\alpha}(k) = CK*\frac{4\pi}{k^2} e^{-l^2k^2/4}

        Args:
            kgrid: kspace grid
            r_smear: smear_factor (l) for gaussian charge

        Returns:
            :math:`u(i)` - 1D numpy array of potential

        """
    l2 = r_smear**2
    k2 = kgrid**2
    v = 4.0 * pi * CK * np.exp(-l2 * k2 / 4) / k2

    return v


def compute_gauss_pot_rspace(rgrid,  r_smear=1.25):
    r"""
         Generates Coulomb potential of gaussian smeared density

         .. math::
             u_{l,\alpha}(k) = CK\frac{erf(r/l)}{r}

         Args:
             rgrid: rspace grid
             r_smear: smear_factor (l) for gaussian charge

         Returns:
             :math:`u(i)` - 1D numpy array of potential

         """
    v = CK*erf(rgrid/r_smear)/rgrid

    return v


def compute_compl_gauss_pot_rspace(rgrid,  r_smear=1.25):
    r"""
         Generates Coulomb potential difference generated
          by point charge and gaussian smeared density

         .. math::
             u_{l,\alpha}(k) = CK(\frac{1}{r} - \frac{erf(r/l)}{r})

         Args:
             rgrid: rspace grid
             r_smear: smear_factor (l) for gaussian charge

         Returns:
             :math:`u(i)` - 1D numpy array of potential

         """
    v = CK*(1/rgrid - erf(rgrid/r_smear)/rgrid)

    return v


def compute_long_range_coul_pot(qs, qv, kgrid, r_smear=1.25):

    # matrix of solute-solvent charges
    zab = float(qs)*qv

    v = compute_gauss_pot_kspace(kgrid)
    ul = np.multiply.outer(zab, v)

    return ul


def compute_short_range_coul_pot(qs, qv, rgrid, r_smear=1.25):

    # matrix of solute-solvent charges
    zab = float(qs)*qv

    v = compute_compl_gauss_pot_rspace(rgrid)
    ul = np.multiply.outer(zab, v)

    return ul


