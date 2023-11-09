from dataclasses import dataclass
from designer import *
from random import randint

TREX_SPEED = 5
JUMP_HEIGHT = 15


@dataclass
class World:
    trex: DesignerObject
    trex_speed: int
    is_jumping: bool
    jump_height: int


def create_world() -> World:
    """Create the world"""
    return World(create_trex(), TREX_SPEED, False, 0)


def create_trex() -> DesignerObject:
    """ Create the mermaid """
    trex = emoji("🦖")
    trex.y = get_height() * (.93)
    trex.flip_x = True
    trex.scale_x = 2
    trex.scale_y = 2
    return trex


def jump_trex(world: World, key: str):
    """Make the trex jump"""
    if key == "space":
        world.is_jumping = True
        world.jump_height = JUMP_HEIGHT


def head_left(world: World):
    """ Make the copter start moving left """
    world.trex_speed = -TREX_SPEED
    world.trex.flip_x = False


def head_right(world: World):
    """ Make the copter start moving right """
    world.trex_speed = TREX_SPEED
    world.trex.flip_x = True


def move_trex(world: World):
    """Move the trex horizontally"""
    world.trex.x += world.trex_speed
    if world.is_jumping:
        world.trex.y -= world.jump_height
        world.jump_height -= 1
        if world.jump_height < 0:
            world.is_jumping = False
    elif world.trex.y < get_height() * (.93):
        world.trex.y += 10


def flip_trex(world: World, key: str):
    if key == "left":
        head_left(world)
    elif key == "right":
        head_right(world)


when('starting', create_world)
when("updating", move_trex)
when("typing", flip_trex)
when("typing", jump_trex)

start()

