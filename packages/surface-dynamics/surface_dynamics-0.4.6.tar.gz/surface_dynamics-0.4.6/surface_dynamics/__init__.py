r"""
Flat surfaces
"""
#*****************************************************************************
#       Copyright (C) 2019 Vincent Delecroix <20100.delecroix@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
#*****************************************************************************

from __future__ import absolute_import

from .version import version as __version__

import warnings
warnings.filterwarnings('default',
    r'\[surface_dynamics].*')

# Make sure that sage's imports are going to resolve in the correct order
import sage.all

from .flat_surfaces.all import *
from .interval_exchanges.all import *
from .misc.constellation import Constellation, Constellations
from .topological_recursion import *
from .topology.all import *

del absolute_import
