#!/usr/bin/env python
# coding: utf-8
import numpy as np
from ase.optimize import BFGS
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase.io.trajectory import Trajectory,TrajectoryWriter
from ase.calculators.singlepoint import SinglePointCalculator
from ase.io import read,write
from ase import units
from ase.visualize import view
from irff.irff_np import IRFF_NP
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')
from irff.AtomDance import AtomDance


def deb_energies(i=0,j=1,ffield='ffield.json',nn='T',traj='md.traj'):
    # atoms = read(traj)
    # ao = AtomDance(atoms)
    # images = ao.stretch([[i,j]],nbin=50,traj=False)
    images =  Trajectory(traj)
    atoms=images[0]
    
    nn_=True if nn=='T'  else False
    ir = IRFF_NP(atoms=atoms,
                 libfile=ffield,
                 rcut=None,
                 nn=nn_)

    ir.calculate_Delta(atoms)
    natom = ir.natom

    r_,eb,bosi,bop_si,bop,bop_pi,bop_pp,bo = [],[],[],[],[],[],[],[]
    eba,eo,dlpi,dlpj,ev,boe = [],[],[],[],[],[]
    esi,epi,epp = [],[],[]
    Di,Dj = [],[]
    Dpi   = []
   
    for i_,atoms in enumerate(images):
        positions = atoms.positions
        v = positions[j] - positions[i]
        r = np.sqrt(np.sum(np.square(v)))
        
        ir.calculate(atoms)
        r_.append(ir.r[i][j])
        eb.append(ir.ebond[i][j])
        eba.append(ir.ebond[i][j] + ir.eover[i] + ir.Evdw) 
        ev.append(ir.Evdw)
        eo.append(ir.Eover) 
        eb1 = ir.ebond[0][1]
        eb2 = ir.ebond[2][3]
        # print('%d Energies: ' %i_,'%12.4f ' %ir.E, 'Ebd: %8.4f' %ir.ebond[0][1],'Ebd: %8.4f' %ir.ebond[2][3] )

        print('%d Energies: ' %i_,
              '%12.4f ' %ir.E,
              'Ebd: %8.4f' %ir.Ebond,
              'Eov: %8.4f' %ir.Eover,
              'Eang: %8.4f' %ir.Eang,
              'Eun: %8.4f' %ir.Eunder,
              'Etor: %8.4f' %ir.Etor,
              'Ele: %8.4f' %ir.Elone,
              'Evdw: %8.4f' %ir.Evdw,
              'Ehb: %8.4f' %ir.Ehb)

        dlpi.append(ir.Delta_lpcorr[i])
        dlpj.append(ir.Delta_lpcorr[j])
        Di.append(ir.Delta[i])
        Dj.append(ir.Delta[j])
        Dpi.append(ir.Dpil[j])


if __name__ == '__main__':
   deb_energies()


