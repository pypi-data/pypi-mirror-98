"""You can define a path with a list of points combined with a cross-section.

The CrossSection object extrudes a path

Based on phidl.device_layout.CrossSection
"""

from typing import Callable, Iterable, Optional

from phidl.device_layout import CrossSection

from pp.layers import LAYER
from pp.types import Layer

CrossSectionFactory = Callable[..., CrossSection]


def strip(
    width: float,
    layer: Layer,
    cladding_offset: float = 0,
    layers_cladding: Optional[Iterable[Layer]] = None,
) -> CrossSection:
    """Returns a fully etched waveguide CrossSection."""

    layers_cladding = layers_cladding or []

    x = CrossSection()
    x.add(width=width, offset=0, layer=layer, ports=["in", "out"])

    for layer_cladding in layers_cladding:
        x.add(width=width + 2 * cladding_offset, offset=0, layer=layer_cladding)
    return x


if __name__ == "__main__":
    import pp

    # P = pp.path.euler(radius=10, use_eff=True)
    # P = euler()
    P = pp.Path()
    P.append(pp.path.straight(length=5))
    P.append(pp.path.arc(radius=10, angle=90))
    # P.append(pp.path.spiral())

    # Create a blank CrossSection
    X = CrossSection()
    X.add(width=2.0, offset=-4, layer=LAYER.HEATER, ports=["HW1", "HE1"])
    # X.add(width=0.5, offset=0, layer=LAYER.SLAB90, ports=["in", "out"])
    # X.add(width=2.0, offset=4, layer=LAYER.HEATER, ports=["HW0", "HE0"])

    # Combine the Path and the CrossSection into a Component
    c = pp.path.component(P, X)

    c = pp.path.component(P, strip(width=2, layer=LAYER.WG, cladding_offset=3))

    # c = pp.add_pins(c)
    # c << pp.components.bend_euler(radius=10)
    c << pp.components.bend_circular(radius=10)
    c.show()
