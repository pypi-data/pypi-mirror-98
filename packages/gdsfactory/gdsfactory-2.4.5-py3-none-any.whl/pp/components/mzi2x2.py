from typing import Optional

from pp.cell import cell
from pp.component import Component
from pp.components.bend_euler import bend_euler
from pp.components.component_sequence import component_sequence
from pp.components.coupler import coupler
from pp.components.extension import line
from pp.components.waveguide import waveguide
from pp.components.waveguide_heater import wg_heater_connected
from pp.netlist_to_gds import netlist_to_component
from pp.port import select_ports
from pp.routing.route_ports_to_side import route_elec_ports_to_side
from pp.tech import TECH_SILICON_C, Tech
from pp.types import ComponentFactory


@cell
def mzi_arm(
    L0: float = 60.0,
    DL: float = 0.0,
    L_top: float = 10.0,
    bend_radius: float = 10.0,
    bend90_factory: ComponentFactory = bend_euler,
    waveguide_heater_function: ComponentFactory = wg_heater_connected,
    waveguide_function: ComponentFactory = waveguide,
    with_elec_connections: bool = True,
    tech: Optional[Tech] = None,
) -> Component:
    """Returns an MZI arm.

    Args:
        L0: vertical length with heater
        DL: extra vertical length without heater (delat_length=2*DL)
        L_top: 10.0, horizontal length
        bend_radius: 10.0
        bend90_factory: bend_euler
        waveguide_heater_function: wg_heater_connected
        waveguide_function: waveguide

    ::

         L_top
        |     |
        DL    DL
        |     |
        L0    L0
        |     |
       -|     |-

        B2-Sh1-B3
        |     |
        Sv1   Sv2
        |     |
        H1    H2
        |     |
       -B1    B4-


    """
    tech = tech or TECH_SILICON_C
    if not with_elec_connections:
        waveguide_heater_function = waveguide_function

    _bend = bend90_factory(radius=bend_radius, tech=tech)

    straight_vheater = waveguide_heater_function(length=L0, tech=tech)
    straight_h = waveguide_function(length=L_top, tech=tech)
    straight_v = waveguide_function(length=DL, tech=tech) if DL > 0 else None

    symbol_to_component = {
        "A": (_bend, "W0", "N0"),
        "B": (_bend, "N0", "W0"),
        "H": (straight_vheater, "W0", "E0"),
        "h": (straight_h, "W0", "E0"),
        "v": (straight_v, "W0", "E0"),
    }

    # sequence = ["A", "v", "H", "B", "Sh", "B", "H", "v", "A"]
    sequence = "AvHBhBHvA"

    if with_elec_connections:
        ports_map = {
            "E_0": ("H2", "E_1"),
            "E_1": ("H1", "E_0"),
            "E_2": ("H1", "E_1"),
            "E_3": ("H2", "E_0"),
        }
    else:
        ports_map = {}

    component = component_sequence(
        sequence=sequence,
        symbol_to_component=symbol_to_component,
        ports_map=ports_map,
        input_port_name="W0",
        output_port_name="E0",
    )
    return component


@cell
def mzi2x2(
    CL_1: float = 20.147,
    L0: float = 60.0,
    DL: float = 7.38,
    L2: float = 10.0,
    gap: float = 0.234,
    bend_radius: float = 10.0,
    bend90_factory: ComponentFactory = bend_euler,
    waveguide_heater_function: ComponentFactory = wg_heater_connected,
    waveguide_function: ComponentFactory = waveguide,
    coupler_function: ComponentFactory = coupler,
    with_elec_connections: bool = False,
    tech: Optional[Tech] = None,
) -> Component:
    """Mzi 2x2

    Args:
        CL_1: coupler length
        L0: vertical length for both and top arms
        DL: bottom arm extra length
        L2: L_top horizontal length
        gap: 0.235
        bend_radius: 10.0
        bend90_factory: bend_euler
        waveguide_heater_function: wg_heater_connected or waveguide
        waveguide_function: waveguide
        coupler_function: coupler
        with_elec_connections: add electrical pads
        tech: Technology


    .. code::

         __L2__
        |      |
        L0     L0
        |      |
      ==|      |==
        |      |
        L0     L0
        |      |
        DL     DL
        |      |
        |__L2__|


    .. code::

               top_arm
        ==CL_1=       =CL_1===
               bot_arm


    """
    tech = tech or TECH_SILICON_C
    if not with_elec_connections:
        waveguide_heater_function = waveguide_function

    cpl = coupler_function(length=CL_1, gap=gap)

    arm_defaults = {
        "L_top": L2,
        "bend_radius": bend_radius,
        "bend90_factory": bend90_factory,
        "waveguide_heater_function": waveguide_heater_function,
        "waveguide_function": waveguide_function,
        "with_elec_connections": with_elec_connections,
    }

    arm_top = mzi_arm(L0=L0, **arm_defaults)
    arm_bot = mzi_arm(L0=L0, DL=DL, **arm_defaults)

    components = {
        "CP1": (cpl, "None"),
        "CP2": (cpl, "None"),
        "arm_top": (arm_top, "None"),
        "arm_bot": (arm_bot, "mirror_x"),
    }

    connections = [
        # Top arm
        ("CP1", "E1", "arm_top", "W0"),
        ("arm_top", "E0", "CP2", "W1"),
        # Bottom arm
        ("CP1", "E0", "arm_bot", "W0"),
        ("arm_bot", "E0", "CP2", "W0"),
    ]

    if with_elec_connections:

        ports_map = {
            "W0": ("CP1", "W0"),
            "W1": ("CP1", "W1"),
            "E0": ("CP2", "E0"),
            "E1": ("CP2", "E1"),
            "E_TOP_0": ("arm_top", "E_0"),
            "E_TOP_1": ("arm_top", "E_1"),
            "E_TOP_2": ("arm_top", "E_2"),
            "E_TOP_3": ("arm_top", "E_3"),
            "E_BOT_0": ("arm_bot", "E_0"),
            "E_BOT_1": ("arm_bot", "E_1"),
            "E_BOT_2": ("arm_bot", "E_2"),
            "E_BOT_3": ("arm_bot", "E_3"),
        }

        component = netlist_to_component(components, connections, ports_map)
        # Need to connect common ground and redefine electrical ports

        ports = component.ports
        y_elec = ports["E_TOP_0"].y
        for ls, le in [
            ("E_BOT_0", "E_BOT_1"),
            ("E_TOP_0", "E_TOP_1"),
            ("E_BOT_2", "E_TOP_2"),
        ]:
            component.add_polygon(line(ports[ls], ports[le]), layer=ports[ls].layer)

        # Add GND
        component.add_port(
            name="GND",
            midpoint=0.5 * (ports["E_BOT_2"].midpoint + ports["E_TOP_2"].midpoint),
            orientation=180,
            width=ports["E_BOT_2"].width,
            layer=ports["E_BOT_2"].layer,
            port_type="dc",
        )

        component.ports["E_TOP_3"].orientation = 0
        component.ports["E_BOT_3"].orientation = 0

        # Remove the eletrical ports that we have just used internally
        for lbl in ["E_BOT_0", "E_BOT_1", "E_TOP_0", "E_TOP_1", "E_BOT_2", "E_TOP_2"]:
            component.ports.pop(lbl)

        # Reroute electrical ports
        _e_ports = select_ports(component.ports, port_type="dc")
        routes, e_ports = route_elec_ports_to_side(_e_ports, side="north", y=y_elec)

        for route in routes:
            component.add(route["references"])

        for p in e_ports:
            component.ports[p.name] = p

        # Create nice electrical port names
        component.ports["HT1"] = component.ports["E_TOP_3"]
        component.ports.pop("E_TOP_3")

        component.ports["HT2"] = component.ports["E_BOT_3"]
        component.ports.pop("E_BOT_3")

        # Make sure each port knows its name
        for k, p in component.ports.items():
            p.name = k

    else:
        ports_map = {
            "W0": ("CP1", "W0"),
            "W1": ("CP1", "W1"),
            "E0": ("CP2", "E0"),
            "E1": ("CP2", "E1"),
        }

        component = netlist_to_component(components, connections, ports_map)

    return component


def get_mzi_delta_length(m, neff=2.4, wavelength=1.55):
    """ m*wavelength = neff * delta_length """
    return m * wavelength / neff


if __name__ == "__main__":

    # print(get_mzi_delta_length(m=15))
    # print(get_mzi_delta_length(m=150))
    # for p in c.ports.values():
    #     print(p.port_type)
    # c = mzi_arm(DL=100)
    # c = mzi2x2(waveguide_heater_function=wg_heater_connected, with_elec_connections=True)
    # pp.write_gds(c, "mzi.gds")
    # print(c)
    # print(hash(frozenset(c.settings.items())))
    # print(hash(c))

    # c = mzi2x2(with_elec_connections=True)
    # cc = pp.add_pins(c)
    # cc.show()

    c = mzi2x2(with_elec_connections=True)
    # c = mzi_arm()
    # from pp.cell import print_cache

    # print_cache()
    c.show(show_subports=True)
