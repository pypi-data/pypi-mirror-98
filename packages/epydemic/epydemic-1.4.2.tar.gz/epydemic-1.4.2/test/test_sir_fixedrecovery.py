# Test SIR with fixed recovery time under different dynamics
#
# Copyright (C) 2017--2020 Simon Dobson
# 
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epydemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epydemic. If not, see <http://www.gnu.org/licenses/gpl.html>.

from epydemic import *
from test.compartmenteddynamics import CompartmentedDynamicsTest
import epyc
import unittest
import networkx

class SIRFixedRecoveryTest(unittest.TestCase, CompartmentedDynamicsTest):

    def setUp( self ):
        '''Set up the experimental parameters and experiment.'''
        
        # single experiment
        self._params = dict()
        self._params[SIR.P_INFECT] = 0.1
        self._params[SIR.P_INFECTED] = 0.01
        self._params[SIR_FixedRecovery.T_INFECTED] = 1.0
        self._network = networkx.erdos_renyi_graph(1000, 0.005)

        # lab run
        self._lab = epyc.Lab()
        self._lab[SIR.P_INFECT] = [ 0.1,  0.3 ]
        self._lab[SIR.P_INFECTED] = 0.01
        self._lab[SIR_FixedRecovery.T_INFECTED] = [ 1.0, 2.0 ]

        # model
        self._model = SIR_FixedRecovery()

    def testEpidemic( self ):
        '''Test we get an epidemic'''
        self._lab = epyc.Lab()
        self._lab[SIR.P_INFECT] = 0.3
        self._lab[SIR.P_INFECTED] = 0.01
        self._lab[SIR_FixedRecovery.T_INFECTED] = 1.0
        e = StochasticDynamics(self._model, self._network)
        self._lab.runExperiment(e)
        rc = (self._lab.results())[0]

        self.assertCountEqual(rc[epyc.Experiment.RESULTS], [SIR.SUSCEPTIBLE, SIR.INFECTED, SIR.REMOVED])
        self.assertTrue(rc[epyc.Experiment.RESULTS][SIR.SUSCEPTIBLE] > 0)
        self.assertTrue(rc[epyc.Experiment.RESULTS][SIR.INFECTED] == 0)
        self.assertTrue(rc[epyc.Experiment.RESULTS][SIR.REMOVED] > 0)
        self.assertEqual(rc[epyc.Experiment.RESULTS][SIR.SUSCEPTIBLE] + rc[epyc.Experiment.RESULTS][SIR.REMOVED], self._network.order())

if __name__ == '__main__':
    unittest.main()
