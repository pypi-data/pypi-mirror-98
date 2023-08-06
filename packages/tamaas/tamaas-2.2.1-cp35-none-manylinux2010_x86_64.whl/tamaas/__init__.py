# -*- mode:python; coding: utf-8 -*-
# @file
# @section LICENSE
#
# Copyright (©) 2016-2021 EPFL (École Polytechnique Fédérale de Lausanne),
# Laboratory (LSMS - Laboratoire de Simulation en Mécanique des Solides)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Tamaas is a library dedicated to the fast treatment of rough contact problems.

See https://tamaas.readthedocs.io for documentation on how to use Tamaas.

See __author__, __license__, __copyright__ for extra information about Tamaas.
"""

__version__ = "2.2.1"
__author__ = ['Lucas Frérot', 'Guillaume Anciaux', 'Valentine Rey', 'Son Pham-Ba', 'Jean-François Molinari']
# TODO Change copyright when is issue with unicode is found
__copyright__ = u"Copyright (©) 2016-2021 EPFL " \
    + u"(École Polytechnique Fédérale de Lausanne), " \
    + u"Laboratory (LSMS - Laboratoire de Simulation en Mécanique des Solides)"
__license__ = "AGPLv3"
__maintainer__ = "Lucas Frérot"
__email__ = "lucas.frerot@protonmail.com"


try:
    from ._tamaas import model_type
    from ._tamaas import _type_traits as __tt

    type_traits = {
        model_type.basic_1d: __tt.basic_1d,
        model_type.basic_2d: __tt.basic_2d,
        model_type.surface_1d: __tt.surface_1d,
        model_type.surface_2d: __tt.surface_2d,
        model_type.volume_1d: __tt.volume_1d,
        model_type.volume_2d: __tt.volume_2d,
    }

    del __tt

    from ._tamaas import *  # noqa

except ImportError as e:
    print("Error trying to import _tamaas:\n{}".format(e))
    raise e
