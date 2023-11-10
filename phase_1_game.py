from dataclasses import dataclass
from designer import *
from random import randint

TREX_SPEED = 5
JUMP_HEIGHT = 15


@dataclass
class World:
    volcano: DesignerObject
    trex: DesignerObject
    trex_speed: int
    is_jumping: bool
    jump_height: int
    platforms: list[DesignerObject]


def create_world() -> World:
    return World(create_volcano(), create_trex(), TREX_SPEED, False, 0, create_platforms())


def create_volcano() -> DesignerObject:
    volcano = emoji("🌋")
    volcano.y = get_height() * (.59)
    volcano.scale_x = 25
    volcano.scale_y = 20
    return volcano


def create_trex() -> DesignerObject:
    trex = emoji("🦖")
    trex.y = get_height() * (.93)
    trex.flip_x = True
    trex.scale_x = 2
    trex.scale_y = 2
    return trex


def create_platforms() -> list[DesignerObject]:
    platforms = []
    count = 10
    while count > 0:
        platform = rectangle("purple", 100, 20)
        platform.x = get_width() * (randint(1, 10) * .1)
        platform.y = get_height() * (randint(1, 10) * .1)
        platforms.append(platform)
        count -= 1

    return platforms


def check_platform_collision(world: World):
    for platform in world.platforms:
        if (
                world.trex.x < platform.x + platform.width
                and world.trex.x + world.trex.width > platform.x
                and world.trex.y < platform.y + platform.height
                and world.trex.y + world.trex.height > platform.y
        ):
            if not world.is_jumping:
                world.trex.y = platform.y - world.trex.height * 0.7
            return True
    return False


def jump_trex(world: World, key: str):
    """Make the trex jump"""
    if key == "space" and not world.is_jumping:
        world.is_jumping = True
        world.jump_height = JUMP_HEIGHT


def head_left(world: World):
    world.trex_speed = -TREX_SPEED
    world.trex.flip_x = False


def head_right(world: World):
    world.trex_speed = TREX_SPEED
    world.trex.flip_x = True


def move_trex(world: World):
    world.trex.x += world.trex_speed
    if world.is_jumping:
        world.trex.y -= world.jump_height
        world.jump_height -= 1
        if world.jump_height < 0:
            world.is_jumping = False
    elif world.trex.y < get_height() * (.93):
        world.trex.y += 10
    check_platform_collision(world)


def flip_trex(world: World, key: str):
    if key == "left":
        head_left(world)
    elif key == "right":
        head_right(world)


def wall_pow(world: World):
    if world.trex.x > get_width():
        head_left(world)
    elif world.trex.x < 0:
        head_right(world)
    if world.trex.y < 0:
        world.trex.y = 0
        world.is_jumping = False


when('starting', create_world)
when("updating", move_trex)
when("typing", flip_trex)
when("typing", jump_trex)
when("updating", wall_pow)

start()