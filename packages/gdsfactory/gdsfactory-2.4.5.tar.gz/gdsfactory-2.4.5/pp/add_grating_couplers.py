"""Add grating_couplers to a component."""
from typing import Callable, List, Tuple

from phidl.device_layout import Label

import pp
from pp.cell import cell
from pp.component import Component
from pp.components.grating_coupler.elliptical_trenches import (
    grating_coupler_te,
    grating_coupler_tm,
)
from pp.routing.get_input_labels import get_input_labels
from pp.types import ComponentFactory


@cell
def add_grating_couplers(
    component: Component,
    grating_coupler: ComponentFactory = grating_coupler_te,
    layer_label: Tuple[int, int] = pp.LAYER.LABEL,
    gc_port_name: str = "W0",
    get_input_labels_function: Callable[..., List[Label]] = get_input_labels,
) -> Component:
    """Return component with grating couplers and labels."""

    cnew = Component(name=component.name + "_c")
    cnew.add_ref(component)
    grating_coupler = pp.call_if_func(grating_coupler)

    io_gratings = []
    optical_ports = component.get_ports_list(port_type="optical")
    for port in optical_ports:
        gc_ref = grating_coupler.ref()
        gc_port = gc_ref.ports[gc_port_name]
        gc_ref.connect(gc_port, port)
        io_gratings.append(gc_ref)
        cnew.add(gc_ref)

    labels = get_input_labels_function(
        io_gratings,
        list(component.ports.values()),
        component_name=component.name,
        layer_label=layer_label,
        gc_port_name=gc_port_name,
    )
    cnew.add(labels)
    return cnew


def add_te(*args, **kwargs):
    return add_grating_couplers(*args, **kwargs)


def add_tm(*args, grating_coupler=grating_coupler_tm, **kwargs):
    return add_grating_couplers(*args, grating_coupler=grating_coupler, **kwargs)


if __name__ == "__main__":
    # from pp.add_labels import get_optical_text
    # c = pp.components.grating_coupler_elliptical_te()
    # print(c.wavelength)

    # print(c.get_property('wavelength'))

    c = pp.components.waveguide(width=2)
    c = pp.components.mzi2x2(with_elec_connections=True)
    # cc = add_grating_couplers(c)
    cc = add_tm(c)
    print(cc)
    cc.show()
