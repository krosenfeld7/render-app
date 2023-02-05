from src.classes.collection_overseer import CollectionOverseer, collection_dispatcher
from src.classes.material_overseer import MaterialOverseer, material_dispatcher
from src.classes.overseer import Overseer
from src.classes.view_overseer import ViewOverseer, view_dispatcher
from src.classes.world_overseer import WorldOverseer, world_dispatcher


def collection(*args, **kwargs) -> CollectionOverseer:
    return collection_dispatcher(*args, **kwargs)


def view(*args, **kwargs) -> ViewOverseer:
    return view_dispatcher(*args, **kwargs)


def material(*args, **kwargs) -> MaterialOverseer:
    return material_dispatcher(*args, **kwargs)


def world(*args, **kwargs) -> WorldOverseer:
    return world_dispatcher(*args, **kwargs)


dispatch_map = {
    'CollectionOverseer': collection,
    'ViewOverseer': view,
    'MaterialOverseer': material,
    'WorldOverseer': world
}


def overseer_dispatcher(overseer,
                        *args,
                        **kwargs) -> Overseer:
    return dispatch_map[overseer](*args, **kwargs)
