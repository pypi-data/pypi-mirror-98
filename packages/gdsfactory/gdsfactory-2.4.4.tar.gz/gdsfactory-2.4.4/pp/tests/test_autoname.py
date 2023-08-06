from typing import Tuple

import pp
from pp.component import Component


def test_cell() -> Tuple[Component, Component]:
    wg1 = pp.c.waveguide(length=10, width=0.5)
    wg2 = pp.c.waveguide(width=0.5, length=10)
    assert (
        wg1.name == wg2.name
    ), f"{wg1} and {wg2} waveguides have the same settings and should have the same name"
    return wg1, wg2


if __name__ == "__main__":
    wg1, wg2 = test_cell()
    print(wg1)
    print(wg2)
