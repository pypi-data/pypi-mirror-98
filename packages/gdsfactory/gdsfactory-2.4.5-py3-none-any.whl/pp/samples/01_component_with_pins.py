"""You can pass any component that has ports to a function that will add pins in a pin layer.

"""

import pp


def waveguide_sample(length=5, width=1):
    """Returns waveguide with ports."""
    wg = pp.Component("waveguide_sample")
    wg.add_polygon([(0, 0), (length, 0), (length, width), (0, width)], layer=(1, 0))
    wg.add_port(name="W0", midpoint=[0, width / 2], width=width, orientation=180)
    wg.add_port(name="E0", midpoint=[length, width / 2], width=width, orientation=0)
    return wg


if __name__ == "__main__":
    wg = waveguide_sample()
    wg_with_pins = pp.add_pins(wg)
    wg_with_pins.show()
