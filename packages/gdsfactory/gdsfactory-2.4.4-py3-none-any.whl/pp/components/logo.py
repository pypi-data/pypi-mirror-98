import pp
from pp.component import Component


@pp.cell
def logo(text: str = "GDS_FACTORY") -> Component:
    """Returns GDSfactory logo."""
    c = pp.Component()
    elements = []
    for i, letter in enumerate(text):
        c << pp.c.text(letter, layer=(i + 1, 0), size=10)
        elements.append(c)

    c.distribute(
        elements="all",  # either 'all' or a list of objects
        direction="x",  # 'x' or 'y'
        spacing=1,
        separation=True,
    )
    return c


if __name__ == "__main__":
    c = logo()
    c.show()
