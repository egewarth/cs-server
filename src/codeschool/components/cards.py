from functools import singledispatch

from bricks.helpers import js_class
from bricks.html5 import div, a_or_span, h1, p, aside, article, section
from . import mdl


@singledispatch
def simple_card(text, title=None, href=None, icon='help', faded=False,
                onclick=None,
                id=None, class_=None):
    """
    Returns HTML for a cs-card block.

    This function accepts multiple dispatch and clients might register
    different implementations for specific models/types.

    Args:
        text:
            Card description and main content.
        title:
            Card title.
        href:
            Optional address for the class icon.
        icon:
            Material icon for card.
        faded:
            If True, card is rendered with the faded state.
        onclick:
            Action to be associated with the onclick event.
        id/class_:
            Card's id/class attributes.
    """
    class_ = js_class('cs-card mdl-shadow--4dp', 'mdl-cell',
                      faded and 'cs-card--faded', class_)
    icon = mdl.icon(class_='cs-card__icon')[icon]
    icon = a_or_span(href=href, onclick=onclick, class_='cs-card__link')[icon]

    return \
        div(class_=class_, id=id)[
            icon,
            title and h1(class_='cs-card__title')[title],
            text and p(text)
        ]


def card_container(cards, title=None, description=None, class_=None, **kwargs):
    """
    A container for simple card elements.

    Args:
        cards:
            A list of cards.
        title:
            Title to show to the LHS of the container.
        description:
            Short description bellow title.
    """
    if title:
        cls = 'cs-card-aside__aside mdl-cell mdl-cell--3-col'
        lhs_aside = \
            aside(class_=cls)[
                h1(title),
                description and p(description)
            ]

    ncols = 9 if title else 12
    cls = js_class('cs-card-aside mdl-grid mdl-grid--no-spacing', class_)
    return \
        section(class_=cls)[
            title and lhs_aside,

            article(class_='mdl-cell mdl-cell--%-col' % ncols)[
                div(class_='cs-card-aside__content mdl-grid')[
                    cards,
                ]
            ],
        ]
