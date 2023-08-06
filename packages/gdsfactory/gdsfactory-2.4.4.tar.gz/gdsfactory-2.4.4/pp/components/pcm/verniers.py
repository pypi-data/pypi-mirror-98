import numpy as np

import pp
from pp.component import Component
from pp.tech import TECH_SILICON_C, Tech


@pp.cell
def verniers(
    width_min: float = 0.1,
    width_max: float = 0.5,
    gap: float = 0.1,
    size_max: int = 11,
    tech: Tech = TECH_SILICON_C,
) -> Component:
    c = pp.Component()
    y = 0

    widths = np.linspace(width_min, width_max, int(size_max / (width_max + gap)))

    for width in widths:
        w = c << pp.c.waveguide(width=width, length=size_max, tech=tech)
        y += width / 2
        w.y = y
        c.add(pp.c.label(str(int(width * 1e3)), position=(0, y)))
        y += width / 2 + gap

    return c


if __name__ == "__main__":
    c = verniers()
    c.flatten()
    pp.write_gds(c, "verniers.gds")
    c.show()
