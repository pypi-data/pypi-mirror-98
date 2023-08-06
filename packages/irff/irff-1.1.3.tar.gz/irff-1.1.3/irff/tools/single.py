#!/usr/bin/env python
# -*- coding: utf-8 -*-
from irff.dft.SinglePointEnergy import SinglePointEnergies
from ase.io import read


if __name__ == '__main__':
   SinglePointEnergies('md.traj',label='h2o-s3',
                       xcf='GGA',
                       xca='PBE',
                       basistype='split',
                       frame=50,cpu=4)




