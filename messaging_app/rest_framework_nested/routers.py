from rest_framework.routers import DefaultRouter


class NestedDefaultRouter(DefaultRouter):
    """Shim for NestedDefaultRouter.

    This class stands in to satisfy imports and basic router behavior during
    checks. It behaves like DefaultRouter.
    """

    pass
