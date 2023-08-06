#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import proposal as pp
from tqdm import tqdm


def muons(energy, statistics, vcut, do_continuous_randomization, dist):

    sec_def = pp.SectorDefinition()
    sec_def.medium = pp.medium.StandardRock(1.0)
    sec_def.geometry = pp.geometry.Sphere(pp.Vector3D(), 1e20, 0)
    sec_def.particle_location = pp.ParticleLocation.inside_detector

    sec_def.scattering_model = pp.scattering.ScatteringModel.Highland
    sec_def.do_continuous_randomization = do_continuous_randomization

    sec_def.cut_settings.ecut = 0
    sec_def.cut_settings.vcut = vcut

    interpolation_def = pp.InterpolationDef()
    interpolation_def.path_to_tables = "~/.local/share/PROPOSAL/tables"
    interpolation_def.path_to_tables_readonly = "~/.local/share/PROPOSAL/tables"

    mu_def = pp.particle.MuMinusDef()
    prop = pp.Propagator(
            particle_def=mu_def,
            sector_defs=[sec_def],
            detector=pp.geometry.Sphere(pp.Vector3D(), 1e20, 0),
            interpolation_def=interpolation_def
    )

    mu = pp.particle.DynamicData(mu_def.particle_type)
    mu.position = pp.Vector3D(0, 0, 0)
    mu.direction = pp.Vector3D(0, 0, -1)
    mu.energy = energy
    mu.propagated_distance = 0.
    mu.time = 0.

    mu_energies = []
    pp.RandomGenerator.get().set_seed(1234)

    for i in tqdm(range(statistics)):

        secondaries = prop.propagate(mu, dist * 100)

        mu_energies.append(secondaries.energy[-1])
        # del secondaries

    return mu_energies


if __name__ == "__main__":

    # =========================================================
    # 	Save energies
    # =========================================================

    energy = 1e8
    statistics = int(1e4)
    dist = 300
    binning = 100

    energies_1 = muons(energy, statistics, 0.05, False, dist)
    energies_2 = muons(energy, statistics, 0.0001, False, dist)
    energies_3 = muons(energy, statistics, 0.05, True, dist)

    tex_preamble = [
        r"\usepackage{amsmath}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[T1]{fontenc}",
    ]

    font_size = 10

    params = {
        'backend': 'pdf',
        'font.family': 'serif',
        'font.size': 12,
        'text.usetex': True,
        'text.latex.preamble': tex_preamble,
        'axes.labelsize': font_size,
        'legend.numpoints': 1,
        'legend.shadow': False,
        'legend.fontsize': font_size,
        'xtick.labelsize': font_size,
        'ytick.labelsize': font_size,
        'axes.unicode_minus': True
    }

    plt.rcParams.update(params)

    # =========================================================
    # 	Plot energies
    # =========================================================

    binning = np.linspace(0, energy, 100)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.hist(
        energies_1,
        histtype="step",
        log=True,
        bins=binning,
        label=r"$v_\text{cut} = 0.05$"
    )

    ax.hist(
        energies_2,
        histtype="step",
        log=True,
        bins=binning,
        label=r"$v_\text{cut} = 10^{-4}$"
    )

    ax.hist(
        energies_3,
        histtype="step",
        log=True,
        bins=binning,
        label=r"$v_\text{cut} = 0.05$ mit kont."
    )

    ax.set_xlabel(r'Finale Energie / MeV')
    ax.set_ylabel(r'Anzahl')

    ax.legend(loc='upper left')

    fig.tight_layout()
    fig.savefig("mu_continuous_new.pdf")
