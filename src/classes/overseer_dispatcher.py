""" This module provides functions for a seamless dispatch implementation
    for returning the correct overseer type.
"""

from src.classes.collection_overseer import CollectionOverseer, collection_dispatcher
from src.classes.material_overseer import MaterialOverseer, material_dispatcher
from src.classes.overseer import Overseer
from src.classes.view_overseer import ViewOverseer, view_dispatcher
from src.classes.world_overseer import WorldOverseer, world_dispatcher


def collection(*args, **kwargs) -> CollectionOverseer:
    """ The generic CollectionOverseer dispatcher. """

    return collection_dispatcher(*args, **kwargs)


def view(*args, **kwargs) -> ViewOverseer:
    """ The generic ViewOverseer dispatcher. """

    return view_dispatcher(*args, **kwargs)


def material(*args, **kwargs) -> MaterialOverseer:
    """ The generic MaterialOverseer dispatcher. """

    return material_dispatcher(*args, **kwargs)


def world(*args, **kwargs) -> WorldOverseer:
    """ The generic WorldOverseer dispatcher. """

    return world_dispatcher(*args, **kwargs)

# maps the overseer names to the dispatch functions above.
dispatch_map = {
    'CollectionOverseer': collection,
    'ViewOverseer': view,
    'MaterialOverseer': material,
    'WorldOverseer': world
}


def overseer_dispatcher(overseer,
                        *args,
                        **kwargs) -> Overseer:
    """ The generic Overseer dispatcher. """

    return dispatch_map[overseer](*args, **kwargs)
