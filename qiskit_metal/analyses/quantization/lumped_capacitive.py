# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""Handles the capacitive simulation of a transmon pocket model.

Convert capacitance matrices extracted from Q3D into Hamiltonian parameters
using the Duffing model. Typical input is the capacitance matrix calculated from Q3D.

Each function prints out the parameters and outputs a dictionary.
"""
# pylint: disable=invalid-name

import io
import re
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt
from pint import UnitRegistry

__all__ = [
    'Ic_from_Lj', 'Ic_from_Ej', 'Cs_from_Ec', 'transmon_props', 'chi',
    'extract_transmon_coupled_Noscillator', 'levels_vs_ng_real_units',
    'get_C_and_Ic', 'cos_to_mega_and_delta', 'chargeline_T1',
    'readin_q3d_matrix', 'readin_q3d_matrix_m', 'load_q3d_capacitance_matrix',
    'df_cmat_style_print', 'move_index_to', 'df_reorder_matrix_basis'
]

# define constants
e = 1.60217657e-19  # electron charge
h = 6.62606957e-34  # Plank's
hbar = 1.0545718E-34  # Plank's reduced
phinot = 2.067 * 1E-15  # magnetic flux quantum
phi0 = phinot / (2 * np.pi)  # reduced magnetic flux quantum

# TODO: Move to a more generic file


def Ic_from_Lj(Lj: float) -> float:
    """Critical current In SI units.

    Args:
        Lj (float): In Henries

    Returns:
        float: In Amps
    """
    return phi0 / Lj


def Ic_from_Ej(Ej: float) -> float:
    """Critical current In SI units.

    Args:
        Ej (float): In Joules

    Returns:
        float: In Amps
    """
    return Ej / phi0


def Cs_from_Ec(Ec: float) -> float:
    """Get total shunt capacitance from charging energy In SI units.

    Args:
        Ec (float): In Joules

    Returns:
        float: In farads
    """
    return e**2 / (2 * Ec)


def transmon_props(Ic: float, Cq: float):
    """Properties of a transmon qubit.

    Calculate LJ, EJ, EC, wq, eps from Ic,Cq.

    Arguments:
        Ic (float): Junction Ic (in A)
        Cq (float): Junction capacitance (in F)

    Returns:
        tuple: [LJ, EJ, Zqp, EC, wq, wq0, eps1] -- Inductange
    """

    LJ = phi0 / Ic
    EJ = phi0**2 / LJ / hbar
    Zqp = np.sqrt(LJ / Cq)
    EC = e**2 / 2 / Cq / hbar
    wq0 = 1 / np.sqrt(LJ * Cq)
    wq = 1 / np.sqrt(LJ * Cq) - EC

    # charge dispersion
    eps1 = EC * 2**9 * (2/np.sqrt(np.pi)) * \
        (EJ/2/EC)**(1.25) * np.exp(-np.sqrt(8*EJ/EC))

    return LJ, EJ, Zqp, EC, wq, wq0, eps1


# TODO: Move to a more generic file


def chi(g: float, wr: float, w01: float, w12: float):
    r"""
    Calculate the dispersive shift $\chi$, where $2*\chi$ is
    the `|0> --> |1>` splitting).

    Accounts for push on the i-th transmon level due to the j-th transmon level,
    mediated by cavity.

    All args need to be in the same units.

    Arguments:
        g (float): Qubit-cavity linear coupling.
        wr (float): Frequency of resonator.
        w01 (float): Qubit 01 transition frequency
        w12 (float): Qubit 12 transition frequency

    Returns:
        float: Calculated chi value
    """

    # Push on the i-th transmon level due to the j-th transmon level
    # mediated by cavity

    # shift of the zero state
    # In this case i=0 and j=1.
    chibus_0 = -2 * g**2 * w01 / (w01**2 - wr**2)  # Koch Eq. (3.10)

    # shift of the 1 state
    # the g of the levels scales rougly as sqrt(n), so the 2 for the 2 / (w12 - wr)
    chibus_1 = g**2 * (1 / (w01 - wr) - 2 / (w12 - wr) + 1 / (w01 + wr) - 2 /
                       (w12 + wr))

    return (chibus_1 - chibus_0) / 2  # Koch Eq. (3.9)


def extract_transmon_coupled_Noscillator(capMatrix,
                                         Ic: float,
                                         CJ: float,
                                         N: int,
                                         fb: List[float],
                                         fr: float,
                                         res_L4_corr: float = None,
                                         g_scale: float = 1.0,
                                         print_info: bool = False):
    """Primary analysis function called by the user for lumped-element mode
    (LOM) analysis. Uses a Maxwell capacitance matrix generated by a capacitave
    extractor, such as Q3D. Additionally takes more values to determine many
    parameters of the Hamiltonian of the system.

    The capMatrix can be imported using `readin_q3d_matrix`

    Calculate the χ The full dispersive splitting using analytical
    approximations, i.e., return the `|0> --> |1>` splitting.

    Args:
        capMatrix (np.ndarray): Order of the capacitance matrix must be
          bus1...busN-1, ground, Qubit_pad1, Qubit_pad2, readout. (in F)
          If not in the correct order, use df_reorder_matrix_basis() to put
          it in the proper order. It is advised that the user follow a naming scheme
          in QiskitMetal or Q3D which results in the necessary order by default (eg. alphabetical)
        Ic (float): Junction Ic (in A)
        Cj (float): Junction capacitance (in F)
        N (int): Coupling pads (1 readout, N-1 bus)
        fb (float): Coupling bus and readout frequencies (in GHz).
                    fb can be a list with the order the order they appear in the capMatrix.
        fr (float): Coupling bus and readout frequencies (in GHz).
                    fr can be a list with the order the order they appear in the capMatrix.
        res_L4_corr (list): Correction factor is the resonators are L/4
          if none it ignores, otherwise this is a list of length N
          in the form [1,0,1,...].  Defaults to None.
        g_scale (float): Scale factor
        print_info (bool): Print transmon and coupling properties. Defaults to False.

    Returns:
        dict: `ham_dict` is a dictionary of all the calculated values

    Raises:
        ValueError: If N is not positive
        ValueError: If the capacitance matrix is the wrong size
    """

    # Error checks
    if N < 0:
        raise ValueError('N must positive')
    if len(capMatrix) != (N + 3):
        raise ValueError('Capacitance matrix is not the right size')

    # make list of angular frequencies of resonators
    wr = np.zeros(N)  # angular freq of resonators (GHz-rad)
    for ii in range(N):
        if ii == 0:  # readout resonator
            wr[ii] = 2 * np.pi * fr * 1e9
        else:
            if isinstance(fb, (int, float)):  # just a single one
                wr[ii] = 2 * np.pi * fb * 1e9
            else:
                wr[ii] = 2 * np.pi * fb[ii - 1] * 1e9  # offset index by

    ########################################################
    #### Transmission line properties

    # Initial values
    Zbus = 50
    Cr = 0.5 * np.pi / (wr * Zbus)
    Lr = 1 / wr**2 / Cr

    # L/4 resonators have an effective capacitance that is
    # half the L/2 case (and likewise the Lr is twice) at the
    # same resonance frequency
    # DCM (I think from numerics)
    if not res_L4_corr is None:
        for i in range(len(res_L4_corr)):
            if res_L4_corr[i]:
                Cr[i] /= 2.0
                Lr[i] *= 2.0

    ########################################################
    # Capacitance matrix parsing

    ground_index = max([0, N - 1])
    qubit_index = [ground_index + 1, ground_index + 2]
    bus_index = np.zeros(N, dtype=int)
    for ii in range(N):
        if ii == 0:
            bus_index[ii] = len(capMatrix) - 1
        else:
            bus_index[ii] = ii - 1

    # Cg list of qubit pads to ground
    Cg = [
        -capMatrix[qubit_index[0], ground_index],
        -capMatrix[qubit_index[1], ground_index]
    ]

    # Cs qubit pads to each other
    Cs = -capMatrix[qubit_index[0], qubit_index[1]]

    # Cbus (qubit pads to coupling pads)
    # index is ordered as [readout,bus1,...]
    Cbus = np.zeros([2, N])
    for ii in range(2):
        for jj in range(N):
            Cbus[ii, jj] = -capMatrix[qubit_index[ii], bus_index[jj]]

    # crosspad capacitance
    Cbusbus = np.zeros([N, N])
    for ii in range(N):
        for jj in range(N):
            if ii != jj:
                Cbusbus[ii, jj] = -capMatrix[bus_index[ii], bus_index[jj]]

    # sum of capacitances from each pad to ground
    # this assumes the bus couplers are at "ground"
    C1S = Cg[0] + np.sum(Cbus[0,])
    C2S = Cg[1] + np.sum(Cbus[1,])

    # total capacitance between pads
    tCSq = Cs + C1S * C2S / (C1S + C2S)  # Key equation

    # total capacitance of each pad to ground?
    # Note the + in the squared term below !!!
    tCSbus = np.zeros(N)
    for ii in range(N):
        tCSbus[ii] = Cr[ii] - (Cbus[0, ii]+Cbus[1, ii])**2 / \
            (C1S+C2S) + np.sum(Cbus[:, ii]) + np.sum(Cbusbus[ii, :])

    # qubit to coupling pad capacitance
    tCqbus = (C2S * Cbus[0,] - Cbus[1,] * C1S) / (C1S + C2S)

    # coupling pad to coupling pad capacitance
    tCqbusbus = np.zeros([N, N])
    for ii in range(N):
        for jj in range(N):
            tCqbusbus[ii, jj] = Cbusbus[ii, jj] + \
                (Cbus[0, ii]+Cbus[1, ii])*(Cbus[0, jj]+Cbus[1, jj])/(C1S+C2S)

    # voltage division ratio
    bbus = (C2S * Cbus[0,] - Cbus[1,] * C1S) / ((C1S + C2S) * Cs + C1S * C2S)

    # total qubit capacitance (including junction capacitance)
    Cq = tCSq + CJ

    ########################################################
    ##### Transmon qubit & bus quantum properties

    # get transmon properties given Ic and Cq
    LJ, EJ, Zqp, EC, wq, wq0, eps1 = transmon_props(Ic, Cq)

    # get numerical properties
    fq, alpha, disp, tphi_ms = levels_vs_ng_real_units(Cq / 1e-15,
                                                       Ic / 1e-9,
                                                       N=51)
    wq = 2 * np.pi * fq * 1e9

    # effective impedances of the coupling pads (?)
    Zbus = np.sqrt(Lr / tCSbus)

    # matrix of the qubit and couplings with a single ground node
    #    Cm = np.zeros([N+1,N+1])

    #    Cm = np.array([[Cq, -tCqr1, -tCqr2],
    #        [-tCqr1, tCSr1, -tCr1r2],
    #        [-tCqr2, -tCr1r2, tCSr2]])
    #
    #    Cminv = np.linalg.inv(Cm)
    #
    #    #readout g
    #    gr0 = 0.5*Cminv[0,1]/np.sqrt(Zqp*Zr1p)
    #    print('gr0 = %f [MHz]'%(gr0/2/np.pi/1e6))

    # g's from the qubit
    gqbus = 0.5 * wr * bbus * np.sqrt(Zbus / Zqp) * g_scale
    #gbus = bbus*wr*np.sqrt(Zbus)*e*(EJ/8/EC)**(1/4)/np.sqrt(hbar)
    gbus_in_MHz = gqbus / 1e6 / 2 / np.pi

    # g's between pads
    gbusbus = np.zeros([N, N])
    for ii in range(N):
        for jj in range(N):
            gbusbus[ii,
                    jj] = (0.01) * tCqbusbus[ii, jj] / (tCSbus[ii] * tCSbus[jj])

    ########################################################
    ##### Purcell, Qs, dissipative

    # guesses for the Q's
    Qreadout = 1e4
    Qcouplingbus = 1e5
    Qbus = np.zeros(N)
    for ii in range(N):
        if ii == 0:
            Qbus[ii] = Qreadout
        else:
            Qbus[ii] = Qcouplingbus

    # loss tangent
    kbus = wr / Qbus

    # purcell due to each coupling bus
    T1bus = (wr**2 - wq**2)**2 / (4 * kbus * gqbus**2 * wq**2)

    # total T1
    if N > 0:
        T1 = 1 / (np.sum(1 / T1bus))
    else:
        T1 = 100

    ########################################################
    ##### Transmon properties and final summary

    # chi's
    #d = -EC
    d = alpha * 2 * np.pi * 1e6
    Chi_in_MHz = 2 * chi(gqbus, wr, wq,
                         d + wq) / 2 / np.pi / 1e6  # Total chi in MHz

    ham_dict = {}
    ham_dict['fQ'] = wq / 2 / np.pi / 1E9
    ham_dict['EC'] = EC / 2 / np.pi / 1E6
    ham_dict['EJ'] = EJ / 2 / np.pi / 1E9
    # correction to the anharmonicity (from eq 52 of solgun et al.)
    #ham_dict['alpha'] = ((wq0/wq)**2*ham_dict['EC'])
    ham_dict['alpha'] = alpha
    ham_dict['dispersion'] = disp / 1e3
    ham_dict['gbus'] = gbus_in_MHz
    ham_dict['chi_in_MHz'] = Chi_in_MHz

    if print_info:
        print(qubit_index, bus_index)
        print('Predicted Values')
        print('')
        print('Transmon Properties')
        print('f_Q %f [GHz]' % ham_dict['fQ'])
        print('EC %f [MHz]' % ham_dict['EC'])
        print('EJ %f [GHz]' % ham_dict['EJ'])
        print('alpha %f [MHz]' % ham_dict['alpha'])
        print('dispersion %f [KHz]' % ham_dict['dispersion'])
        print('Lq %f [nH]' % (phi0**2 / (hbar * EJ) / 1e-9))
        print('Cq %f [fF]' % (Cq / 1e-15))
        print('T1 %f [us]' % (T1 / (1e-6)))
        print('')

        print('**Coupling Properties**')
        for ii in range(N):
            print('\ntCqbus%d %f [fF]' % (ii + 1, tCqbus[ii] / (1e-15)))
            print('gbus%d_in_MHz %f [MHz]' % (ii + 1, ham_dict['gbus'][ii]))
            print('χ_bus%d %f [MHz]' % (ii + 1, Chi_in_MHz[ii]))
            print('1/T1bus%d %f [Hz]' % (ii + 1, 1 / T1bus[ii] / (2 * np.pi)))
            print('T1bus%d %f [us]' % (ii + 1, T1bus[ii] / (1e-6)))

        print('Bus-Bus Couplings')
        for ii in range(N):
            for jj in range(ii + 1, N):
                print('gbus%d_%d %f [MHz]' % (ii + 1, jj + 1, gbusbus[ii, jj] /
                                            (2 * np.pi * 1e6)))

    return ham_dict


def levels_vs_ng_real_units(Cq, IC, N=301, do_disp=0, do_plots=0):
    """This numerically computes the exact transmon levels given C and IC as a
    function of the ng ration -- it subtracts the vaccuum flucations so that
    the groud state is set to zero energy.

    Args:
        C (float): In fF
        Ic (float): In nA
        N (int): Number of charge values to use (needs to be odd)
        do_disp (int): Will print out the values
        do_plots (int): Will plot the data

    Returns:
        tuple: fqubitGHz, anharMHz, disp, tphi_ms

    Raises:
        ValueError: If the matrix is not Hermitian
    """
    C = Cq * 1e-15
    IC = IC * 1e-9
    Ec = e**2 / 2 / C

    nmax = 40
    dim = 2 * nmax + 1
    nmat = np.zeros([dim, dim])
    V = nmat
    charge = np.linspace(-1., 1., N)

    # KE
    for ii in range(dim):
        nmat[ii, ii] = ii - nmax

    # PE
    V = np.diag(-0.5 * np.ones([dim - 1]), 1)
    V = (V + np.transpose(np.conj(V)))

    varphi = hbar / 2 / e
    EJ = IC * varphi

    elvls = np.zeros([dim, N])

    for iindex in range(N):
        ng = charge[iindex]

        H = 4 * Ec * (nmat - ng * np.eye(dim))**2 + EJ * V

        if (not np.array_equal(H, np.transpose(np.conj(H)))):
            raise ValueError('Matrix is not Hermitian')

        [d, v] = np.linalg.eig(H)
        sortIX = np.argsort(d)
        sorted_d = d[sortIX]

        elvls[:, iindex] = (sorted_d - sorted_d[0])

    if do_plots:

        # plot using matplotlib (might need to clean this up)

        plt.figure()
        plt.subplot(1, 2, 1)
        plt.plot(charge,
                 elvls[0,] / h / 1e9,
                 'k',
                 charge,
                 elvls[1,] / h / 1e9,
                 'b',
                 charge,
                 elvls[2,] / h / 1e9,
                 'r',
                 charge,
                 elvls[3,] / h / 1e9,
                 'g',
                 LineWidth=2)
        plt.xlabel('Gate charge, n_g [2e]')
        plt.ylabel('Energy, E_n [GHz]')
        plt.subplot(1, 2, 2)
        plt.plot(charge, (-elvls[1, :] / h + elvls[1, 0] / h) / 1e3, 'k')
        plt.xlabel('Gate charge, n_g [2e]')
        plt.ylabel('Energy [kHz], ')
        plt.show()

        plt.figure(2)
        plt.subplot(1, 2, 1)
        plt.plot(
            charge, 1000 * (elvls[2,] / h / 1e9 - elvls[0,] / h / 1e9 -
                            2 * elvls[1,] / h / 1e9 - elvls[0,] / h / 1e9),
            charge, -charge * 0 - 1000 * Ec / h / 1e9)
        plt.xlabel('Gate charge, n_g [2e]')
        plt.ylabel('delta [MHZ] green theory, blue numerics ')
        plt.subplot(1, 2, 2)
        plt.plot(charge, elvls[1,] / h / 1e9 - elvls[0,] / h / 1e9, charge,
                 charge * 0 + (np.sqrt(8 * EJ * Ec) - Ec) / h / 1e9)
        plt.xlabel('Gate charge, n_g [2e]')
        plt.ylabel('F01 [GHZ] green theory, blue numerics ')
        plt.show()

    fqubitGHz = np.mean(elvls[1,] / h / 1e9)
    anharMHz = np.mean(1000 * (elvls[2,] / h / 1e9 - elvls[0,] / h / 1e9 -
                               2 * elvls[1,] / h / 1e9 - elvls[0,] / h / 1e9))

    disp = np.max(-elvls[1,] / h + elvls[1, 0] / h)
    tphi_ms = 2 / (2 * np.pi * disp * np.pi * 1e-4 * 1e-3)

    if do_disp:
        print('Mean Frequency %f [GHz]' % fqubitGHz)
        print('Anharmonicity %f [MHz]' % anharMHz)
        print('EC %f [GHz]' % (Ec / h / 1e9))
        print('Charge Dispersion %f [kHz]' % (disp / 1e3))
        print('Dephasing Time %f [ms]' % tphi_ms)

    return fqubitGHz, anharMHz, disp, tphi_ms


def get_C_and_Ic(Cin_est, Icin_est, f01, f02on2):
    """Get the capacitance and critical current for a transmon of a certain
    frequency and anharmonicity.

    Args:
        Cin_est (float): Initial guess for capacitance (in fF)
        Icin_est (float): Initial guess for critical current (in nA)
        f01 (float): Transmon frequency (in GHz)
        f02on2 (float): 02/2 frequency (in GHz)

    Returns:
        tuple: [C,Ic] from levels_vs_ng_real_units that gives the
        specified frequency and anharmonicity
    """

    xrr = opt.minimize(lambda x: cos_to_mega_and_delta(x[0], x[1], f01, f02on2),
                       [Cin_est, Icin_est],
                       tol=1e-4,
                       options={
                           'maxiter': 100,
                           'disp': True
                       })

    return xrr.x


########################################################################
# Utility functions for reporting and loading - Zlatko


# Cost function for calculating C and IC
# given a C and IC calculate f and f02/2 from 'levels_vs_ng_real_units'
# and least square with measured f01,f02on2
def cos_to_mega_and_delta(Cin, ICin, f01, f02on2):
    """Cost function for calculating C and IC given a C and IC calculate f and
    f02/2 from 'levels_vs_ng_real_units' and least square with measured
    f01,f02on2.

    Args:
        Cin (float): Cin
        ICin (float): ICin
        f01 (float): f01
        f02on2 (float): f02on2

    Returns:
        float: Calculated value
    """
    fqubitGHz, anharMHz, disp, tphi_ms = levels_vs_ng_real_units(Cin,
                                                                 ICin,
                                                                 N=51)

    return ((fqubitGHz - f01)**2 +
            (fqubitGHz + anharMHz / 2. / 1e3 - f02on2)**2)**0.5


# TODO: Move to a more generic file


def chargeline_T1(Ccharge, Cq, f01):
    """Calculate the charge line `T1`.

    Args:
        Cchare (float): Ccharge
        Cq (float): Cq
        f01 (float): f01

    Returns:
        float: Calculated chargeline T1
    """

    return Cq / (Ccharge**2 * 50. * (2 * np.pi * f01)**2)


# TODO: Move to a more generic file


def readin_q3d_matrix(path: str, delim_whitespace=True):
    """Read in the txt file created from q3d export as CSV and output the
    capacitance matrix file exported by Ansys Q3D.

    When exporting pick "save as type: data table"

    Args:
        path (str): Path to file

    Returns:
        tuple: df_cmat, units, design_variation, df_cond

    Example file:

    ::

        DesignVariation:$BBoxL='650um' $boxH='750um' $boxL='2mm' $QubitGap='30um' $QubitH='90um' $QubitL='450um' Lj_1='13nH'
        Setup1:LastAdaptive
        Problem Type:C
        C Units:farad, G Units:mSie
        Reduce Matrix:Original
        Frequency: 5.5E+09 Hz

        Capacitance Matrix
            ground_plane        Q1_bus_Q0_connector_pad Q1_bus_Q2_connector_pad Q1_pad_bot      Q1_pad_top1     Q1_readout_connector_pad
        ground_plane    2.8829E-13      -3.254E-14      -3.1978E-14     -4.0063E-14     -4.3842E-14     -3.0053E-14
        Q1_bus_Q0_connector_pad -3.254E-14      4.7257E-14      -2.2765E-16     -1.269E-14      -1.3351E-15     -1.451E-16
        Q1_bus_Q2_connector_pad -3.1978E-14     -2.2765E-16     4.5327E-14      -1.218E-15      -1.1552E-14     -5.0414E-17
        Q1_pad_bot      -4.0063E-14     -1.269E-14      -1.218E-15      9.5831E-14      -3.2415E-14     -8.3665E-15
        Q1_pad_top1     -4.3842E-14     -1.3351E-15     -1.1552E-14     -3.2415E-14     9.132E-14       -1.0199E-15
        Q1_readout_connector_pad        -3.0053E-14     -1.451E-16      -5.0414E-17     -8.3665E-15     -1.0199E-15     3.9884E-14

        Conductance Matrix
            ground_plane        Q1_bus_Q0_connector_pad Q1_bus_Q2_connector_pad Q1_pad_bot      Q1_pad_top1     Q1_readout_connector_pad
        ground_plane    0       0       0       0       0       0
        Q1_bus_Q0_connector_pad 0       0       0       0       0       0
        Q1_bus_Q2_connector_pad 0       0       0       0       0       0
        Q1_pad_bot      0       0       0       0       0       0
        Q1_pad_top1     0       0       0       0       0       0
        Q1_readout_connector_pad        0       0       0       0       0       0
    """

    text = Path(path).read_text()

    s1 = text.split('Capacitance Matrix')
    assert len(s1) == 2, "Copuld not split text to `Capacitance Matrix`"

    s2 = s1[1].split('Conductance Matrix')

    df_cmat = pd.read_csv(io.StringIO(s2[0].strip()),
                          delim_whitespace=delim_whitespace,
                          skipinitialspace=True,
                          index_col=0)
    if len(s2) > 1:
        df_cond = pd.read_csv(io.StringIO(s2[1].strip()),
                              delim_whitespace=delim_whitespace,
                              skipinitialspace=True,
                              index_col=0)
    else:
        df_cond = None

    if delim_whitespace == False and len(df_cmat.columns):
        df_cmat = df_cmat.drop(df_cmat.columns[-1], axis=1)

    units = re.findall(r'C Units:(.*?),', text)[0]
    design_variation = re.findall(r'DesignVariation:(.*?)\n', text)
    if len(design_variation) == 0:
        design_variation = re.findall(r'Design Variation:(.*?)\n', text)
        if design_variation:
            design_variation = design_variation[0]
        else:
            design_variation = ''
    else:
        design_variation = design_variation[0]

    return df_cmat, units, design_variation, df_cond


def readin_q3d_matrix_m(path: str) -> pd.DataFrame:
    """Read in Q3D cap matrix from a .m file exported by Ansys Q3d.

    Args:
        path (str): Path to .m file

    Returns:
        pd.DataFrame of cap matrix, with no names of columns.
    """
    text = Path(path).read_text()
    match = re.findall(r'capMatrix (.*?)]', text, re.DOTALL)
    if match:
        match = match[0].strip('= [').strip(']').strip('\n')
        dfC = pd.read_csv(io.StringIO(match),
                          skipinitialspace=True,
                          header=None)
    return dfC


# TODO: Move to a more generic file


def load_q3d_capacitance_matrix(path, user_units='fF', _disp=True):
    """Load Q3D capcitance file exported as Maxwell matrix. Do not export
    conductance. Units are read in automatically and converted to user units.

    Arguments:
        path (str): Path to file.
        user_units (str): Units.  Defaults to 'fF'.
        _disp (bool): whehter or not to display messages.  Defaults to True.

    Returns:
        tupe: df_cmat, user_units, design_variation, df_cond
    """
    df_cmat, Cunits, design_variation, df_cond = readin_q3d_matrix(path)

    # Unit convert
    ureg = UnitRegistry()
    q = ureg.parse_expression(Cunits).to(user_units)
    df_cmat = df_cmat * q.magnitude  # scale to user units

    # Report
    if _disp:
        print(
            "Imported capacitance matrix with UNITS: [%s] now converted to USER UNITS:[%s] from file:\n\t%s"
            % (Cunits, user_units, path))
        df_cmat_style_print(df_cmat)

    return df_cmat, user_units, design_variation, df_cond


def df_cmat_style_print(df_cmat: pd.DataFrame):
    """Display the dataframe in the cmat style.

    Args:
        df_cmat (dataframe): Dataframe to display
    """
    from IPython.display import display
    display(df_cmat.style.format("{:.2f}").bar(color='#5fba7d', width=100))


########################################################################
# Utility functions - Zlatko


def move_index_to(i_from: List[int], i_to: List[int], len_):
    """Utility function to swap index.

    Arguments:
        i_from (int): Data frame to swap index
        i_to (int): Data frame to index
        len_ (int): Length of array

    Returns:
        list: list of indecies, such as  array([1, 2, 3, 4, 0, 5])
    """
    idxs = np.arange(0, len_)
    idxs = np.delete(idxs, i_from)
    return np.insert(idxs, i_to, i_from)


# TODO: Move to a more generic file


def df_reorder_matrix_basis(df, i_from, i_to):
    """Data frame handle reording of matrix basis.

    Arguments:
        df (DataFrame): Data frame to swap
        i_from (int): Index to move from
        i_to (int): Index to move to

    Returns:
        DataFrame: The changed index DataFrame
    """
    arr = df.values
    idx = move_index_to(i_from, i_to, len(arr))
    arr = arr[np.ix_(idx, idx)]
    # Maybe make copy
    return pd.DataFrame(arr, columns=df.columns[idx], index=df.index[idx])
