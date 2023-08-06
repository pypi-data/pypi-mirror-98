from typing import Dict, Tuple

from pp.cell import cell
from pp.component import Component
from pp.components.ring_single import ring_single
from pp.components.waveguide import waveguide
from pp.types import ComponentFactory


@cell
def ring_single_array(
    ring_function: ComponentFactory = ring_single,
    waveguide_function: ComponentFactory = waveguide,
    spacing: float = 5.0,
    list_of_dicts: Tuple[Dict[str, float], ...] = (
        dict(length_x=10.0, radius=5.0),
        dict(length_x=20.0, radius=10.0),
    ),
) -> Component:
    """Ring of single bus connected with waveguides.

    .. code::

           ______               ______
          |      |             |      |
          |      |  length_y   |      |
          |      |             |      |
         --======-- spacing ----==gap==--

          length_x

    """
    c = Component()
    settings0 = list_of_dicts[0]
    ring1 = c << ring_function(**settings0)

    ringp = ring1
    wg = waveguide_function(length=spacing)

    for settings in list_of_dicts[1:]:
        ringi = c << ring_function(**settings)
        wgi = c << wg
        wgi.connect("W0", ringp.ports["E0"])
        ringi.connect("W0", wgi.ports["E0"])
        ringp = ringi

    c.add_port("W0", port=ring1.ports["W0"])
    c.add_port("E0", port=ringi.ports["E0"])
    return c


if __name__ == "__main__":
    c = ring_single_array()
    c.show()
