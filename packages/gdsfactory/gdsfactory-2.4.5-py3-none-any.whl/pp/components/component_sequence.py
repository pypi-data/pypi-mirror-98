from itertools import count
from typing import Dict, Optional, Tuple

from pp.cell import cell
from pp.component import Component


class SequenceGenerator:
    def __init__(
        self, start_sequence="IL", repeated_sequence="ASASBSBS", end_sequence="LO"
    ):
        """sequence generator.
        Main use case: any type of cascade of components with repeating patterns
        such as serpentine, cutbacks etc...

        Component sequences have two ports by default.
        it adds aliases for the components forming the sequence.
        They use the component local name and append a suffix index starting from 1,
        so you may access the ports from any subcomponent.

        Usually we can break these components in 3 parts:
        - there is a starting pattern with input and possibly some special
        connections
        - then a repeating pattern
        - An ending pattern with an output

        Example of symbol meaning

        A: bend connected with input W0
        B: bend connected with input N0
        I: taper with input '1'
        O: taper with input '2'
        S: short straight waveguide
        L: long straight waveguide
        """

        self.start_sequence = start_sequence
        self.end_sequence = end_sequence
        self.repeated_sequence = repeated_sequence

    def get_sequence(self, n=2):
        return self.start_sequence + n * self.repeated_sequence + self.end_sequence


def _parse_component_name(name: str) -> Tuple[str, bool]:
    """
    If the component name has more than one character and starts with "!"
    then we need to flip along the axis given by the input port angle
    """
    if len(name) != 1 and name[0] == "!":
        return (name[1:], True)
    return (name, False)


def _flip_ref(c_ref, port_name):
    a = c_ref.ports[port_name].angle
    if a in [0, 180]:
        c_ref.reflect_v(port_name)
    else:
        c_ref.reflect_h(port_name)
    return c_ref


@cell
def component_sequence(
    sequence: str,
    symbol_to_component: Dict[str, Tuple[Component, str, str]],
    ports_map: Optional[Dict[str, Tuple[str, str]]] = None,
    input_port_name: str = "in",
    output_port_name: str = "out",
    start_orientation: float = 0.0,
) -> Component:
    """Returns component from a ASCII sequence and a dictionary to interpret each symbol

    Args:
        sequence: a string or a list of symbols
        symbol_to_component: maps symbols to (component, input, output)
        ports_map: (optional) extra port mapping using the convention
            {port_name: (alias_name, port_name)}
        input_port_name:
        output_port_name:
        start_orientation:

    Returns:
        component containing the sequence of sub-components
        instantiated and connected together in the sequence order

    .. plot::
        :include-source:

        import pp

        bend180 = pp.components.bend_circular180()
        wg_heater = pp.components.waveguide_heater()
        wg = pp.components.waveguide()

        # Define a map between symbols and (component, input port, output port)
        symbol_to_component = {
            "A": (bend180, "W0", "W1"),
            "B": (bend180, "W1", "W0"),
            "H": (wg_heater, "W0", "E0"),
            "-": (wg, "W0", "E0"),
        }

        # Each character in the sequence represents a component
        sequence = "AB-H-H-H-H-BA"
        c = pp.components.component_sequence(sequence=sequence, symbol_to_component=symbol_to_component)
        c.show()

    """
    ports_map = ports_map or {}

    # Remove all None devices from the sequence
    sequence = list(sequence[:])
    to_rm = []
    for i, d in enumerate(sequence):
        _name_device, _ = _parse_component_name(d)
        _device, _, _ = symbol_to_component[_name_device]
        if _device is None:
            to_rm += [i]

    while to_rm:
        sequence.pop(to_rm.pop())

    # To generate unique aliases for each instance
    counters = {k: count(start=1) for k in symbol_to_component.keys()}

    def _next_id(name):
        return "{}{}".format(name, next(counters[name]))

    component = Component()

    # Add first component reference and input port
    name_start_device, do_flip = _parse_component_name(sequence[0])
    _input_device, input_port, prev_port = symbol_to_component[name_start_device]

    prev_device = component.add_ref(_input_device, alias=_next_id(name_start_device))

    if do_flip:
        prev_device = _flip_ref(prev_device, input_port)

    prev_device.rotate(angle=start_orientation)

    component.add_port(name=input_port_name, port=prev_device.ports[input_port])

    # Generate and connect all elements from the sequence
    for s in sequence[1:]:
        s, do_flip = _parse_component_name(s)

        _component, input_port, next_port = symbol_to_component[s]
        ref = component.add_ref(_component, alias=_next_id(s))

        if do_flip:
            ref = _flip_ref(ref, input_port)

        ref.connect(input_port, prev_device.ports[prev_port])
        prev_device = ref
        prev_port = next_port

    # Deal with edge case where the sequence contains only one component
    if len(sequence) == 1:
        ref = prev_device
        next_port = prev_port

    try:
        component.add_port(name=output_port_name, port=ref.ports[next_port])
    except BaseException:
        print(sequence)
        raise

    # Add any extra port specified in ports_map
    for name, (alias, alias_port_name) in ports_map.items():
        component.add_port(name=name, port=component[alias].ports[alias_port_name])

    return component


if __name__ == "__main__":
    import pp

    bend180 = pp.components.bend_circular180()
    wg_heater = pp.components.waveguide_heater()
    wg = pp.components.waveguide()

    # Define a map between symbols and (component, input port, output port)
    symbol_to_component = {
        "A": (bend180, "W0", "W1"),
        "B": (bend180, "W1", "W0"),
        "H": (wg_heater, "W0", "E0"),
        "-": (wg, "W0", "E0"),
    }

    # Each character in the sequence represents a component
    sequence = "AB-H-H-H-H-BA"
    c = pp.components.component_sequence(
        sequence=sequence, symbol_to_component=symbol_to_component
    )
    s = c.get_settings(ignore=("symbol_to_component",))
    print(s["settings"])
    c.show()
