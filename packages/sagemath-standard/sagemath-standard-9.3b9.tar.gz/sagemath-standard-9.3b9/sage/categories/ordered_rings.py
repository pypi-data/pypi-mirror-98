"""
Ordered Rings
"""

#*****************************************************************************
#  Copyright (C) 2020      Matthias Koeppe <mkoeppe@math.ucdavis.edu>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.categories.category_with_axiom import CategoryWithAxiom

class OrderedRings(CategoryWithAxiom):

    """
    The category of ordered rings

    Associative rings with unit, not necessarily commutative, with a
    total order such that `x \leq y` implies `x + z < y + z` and
    `0 \leq x`, `0 \leq y` implies `0 \leq xy`.
    """

    Commutative = LazyImport('sage.categories.ordered_commutative_rings', 'OrderedCommutativeRings', at_startup=True)

class OrderedCommutativeRings(CategoryWithAxiom):

    """
    The category of ordered commutative rings

    Often, they are referred to as simply "ordered rings".

    Commutative rings with unit and a total order such that `x \leq y`
    implies `x + z < y + z` and `0 \leq x`, `0 \leq y` implies `0 \leq
    xy`.
    """

