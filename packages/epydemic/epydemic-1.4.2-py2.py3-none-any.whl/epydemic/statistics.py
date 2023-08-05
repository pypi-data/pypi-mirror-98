# A process to collect global network statistics
#
# Copyright (C) 2021 Simon Dobson
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

from epydemic import Process
from networkx import degree_histogram, connected_components
import sys
if sys.version_info >= (3, 8):
    from typing import Final, Dict, Any
else:
    # backport compatibility with older typing
    from typing import Dict, Any
    from typing_extensions import Final


class NetworkStatistics(Process):
    '''A process that collects statistics about the final network. This process
    defines no events: it simply interrogates the underlying network and extracts
    a collection of descriptive statistics into the final experimental results.
    These are statistics commonly collected in different scenarios, which can
    thus be provided as standard.'''
    
    # Experimental results
    N : Final[str] = 'epydemic.networkstatistics.N'                    #: Result holding the order of the network.
    M : Final[str] = 'epydemic.networkstatistics.M'                    #: Result holding the total number of edges in the network.
    KMEAN : Final[str] = 'epydemic.networkstatistics.kmean'            #: Result holding the mean degree of nodes in the network.
    KDIST : Final[str] = 'epydemic.networkstatistics.k_distribution'   #: Result holding the degree histogram as an array.
    COMPONENTS : Final[str] = 'epydemic.networkstatistics.components'  #: Result holding the number of connected components in the network.
    LCC : Final[str] = 'epydemic.networkstatistics.lcc'                #: Result holding the size of the largest (giant) component
    SLCC : Final[str] = 'epydemic.networkstatistics.slcc'              #: Result holding the size of the second-largest component
    
    def __init__(self):
        super(NetworkStatistics, self).__init__()
        
    def results(self) -> Dict[str, Any]:
        '''Extract the network summary statistics into a dict.
        
        :returns: a dict of experimental results'''
        res = super(NetworkStatistics, self).results()
        
        # order statistics
        g = self.network()
        res[self.N] = g.order()
        res[self.M] = len(g.edges)
        
        # degree statistics
        hist = degree_histogram(g)
        ktotal = 0
        for i in range(len(hist)):
            ktotal += i * hist[i]
        res[self.KMEAN] = ktotal / g.order()
        res[self.KDIST] = hist
        
        # component statistics
        ccs = sorted(list(map(len, connected_components(g))), reverse=True)
        nccs = len(ccs)
        res[self.COMPONENTS] = nccs
        res[self.LCC] = ccs[0] if nccs > 0 else 0
        res[self.SLCC] = ccs[1] if nccs > 1 else 0
        
        return res

