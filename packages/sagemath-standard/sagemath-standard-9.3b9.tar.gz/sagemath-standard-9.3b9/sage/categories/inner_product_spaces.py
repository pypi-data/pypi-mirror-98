r"""
Inner Product Spaces
"""
#*****************************************************************************
#  Copyright (C) 2015 Travis Scrimshaw <tscrim at ucdavis.edu>
#                2020 Matthias Koeppe
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.misc.cachefunc import cached_method
from sage.categories.category import Category
from sage.categories.category_with_axiom import CategoryWithAxiom
from sage.categories.covariant_functorial_construction import RegressiveCovariantConstructionCategory

class WithInnerProductCategory(RegressiveCovariantConstructionCategory):

    _functor_category = "WithInnerProduct"

    @classmethod
    def default_super_categories(cls, category):
        """
        Return the default super categories of ``category.WithInnerProduct()``.

        Mathematical meaning: if `A` is an inner product space in the
        category `C`, then `A` is also a normed space.

        INPUT:

        - ``cls`` -- the class ``WithInnerProductCategory``
        - ``category`` -- a category `Cat`

        OUTPUT:

        A (join) category

        In practice, this returns ``category.WithInnerProduct``, joined
        together with the result of the method
        :meth:`RegressiveCovariantConstructionCategory.default_super_categories()
        <sage.categories.covariant_functorial_construction.RegressiveCovariantConstructionCategory.default_super_categories>`
        (that is the join of ``category`` and ``cat.WithInnerProduct`` for
        each ``cat`` in the super categories of ``category``).

        EXAMPLES:

        Consider ``category=Groups()``. Then, a group `G` with a metric
        is simultaneously a topological group by itself, and a
        inner product space::

            sage: Groups().WithInnerProduct.super_categories()
            [Category of topological groups, Category of inner product spaces]

        This resulted from the following call::

            sage: sage.categories.metric_spaces.WithInnerProductCategory.default_super_categories(Groups())
            Join of Category of topological groups and Category of inner product spaces
        """
        return Category.join([category.Normed(),
                              super(WithInnerProductCategory, cls).default_super_categories(category)])

    # We currently don't have a use for this, but we probably will
    def _repr_object_names(self):
        """
        EXAMPLES::

            sage: Groups().WithInnerProduct  # indirect doctest
            Join of Category of topological groups and Category of inner product spaces
        """
        return "{} with inner product".format(self.base_category()._repr_object_names())

class InnerProductSpaces(WithInnerProductCategory):
    r"""
    The category of inner product spaces.

    A *metric* on a set `S` is a function `d : S \times S \to \RR`
    such that:

    - `d(a, b) \geq 0`,
    - `d(a, b) = 0` if and only if `a = b`.

    A inner product space is a set `S` with a distinguished metric.

    .. RUBRIC:: Implementation

    Objects in this category must implement either a ``dist`` on the parent
    or the elements or ``metric`` on the parent; otherwise this will cause
    an infinite recursion.

    EXAMPLES::

        sage: from sage.categories.metric_spaces import InnerProductSpaces
        sage: C = InnerProductSpaces()
        sage: C
        Category of inner product spaces
        sage: TestSuite(C).run()
    """
    def _repr_object_names(self):
        """
        EXAMPLES::

            sage: Sets().WithInnerProduct  # indirect doctest
            Category of inner product spaces
        """
        return "inner product spaces"

    class ParentMethods:

        pass

    class ElementMethods:
        def abs(self):
            """
            Return the absolute value of ``self``.

            EXAMPLES::

                sage: CC(I).abs()
                1.00000000000000
            """
            P = self.parent()
            return P.metric()(self, P.zero())

    class Complete(CategoryWithAxiom):
        """
        The category of complete inner product spaces.
        """
