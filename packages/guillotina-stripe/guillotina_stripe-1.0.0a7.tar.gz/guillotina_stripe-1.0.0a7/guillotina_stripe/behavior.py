from guillotina_stripe.interfaces import (
    IProduct,
    IMarkerProduct,
    IMarkerSubscription,
    ISubscription,
)
from guillotina import configure
from guillotina.behaviors.instance import ContextBehavior


@configure.behavior(
    title="Subscription behavior fields",
    provides=ISubscription,
    marker=IMarkerSubscription,
    for_="guillotina.interfaces.IResource",
)
class SubscriptionBehavior(ContextBehavior):
    pass


@configure.behavior(
    title="Product behavior fields",
    provides=IProduct,
    marker=IMarkerProduct,
    for_="guillotina.interfaces.IResource",
)
class ProductBehavior(ContextBehavior):
    pass
