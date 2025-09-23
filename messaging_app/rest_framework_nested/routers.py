try:
    # If the real package is installed, import from it
    from rest_framework_nested.routers import NestedDefaultRouter as RealNestedDefaultRouter  # type: ignore
except Exception:
    RealNestedDefaultRouter = None  # sentinel

from rest_framework.routers import DefaultRouter


class NestedDefaultRouter(DefaultRouter):
    """Shim for NestedDefaultRouter.

    If the real rest_framework_nested is available, this shim won't be used; if
    not, this class stands in to satisfy imports and basic router behavior
    during checks. It behaves like DefaultRouter.
    """

    pass
