from dataclasses import dataclass
from designer import *
from random import randint

TREX_SPEED = 7
JUMP_HEIGHT = 15


@dataclass
class Meteor:
    meteorite: DesignerObject
    falling_speed: int


@dataclass
class Meat:
    steak: DesignerObject
    falling_speed: int
    eaten: bool


@dataclass
class World:
    volcano: DesignerObject
    trex: DesignerObject
    trex_speed: int
    is_jumping: bool
    jump_height: int
    platforms: list[DesignerObject]
    meteors: list[Meteor]
    words: DesignerObject
    score: int
    game_over: bool
    meats: list[Meat]


def create_world() -> World:
    return World(create_volcano(), create_trex(),
                 TREX_SPEED, False, 0, create_platforms(),
                 [], text("black", "", 25, get_width() // 6, 8), score=0, game_over=False,
                 meats=[])


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


def create_meteor(world: World):
    meteor = emoji("comet")
    meteor.x = randint(0, get_width() - meteor.width)
    meteor.y = -10
    falling_speed = randint(5, 15)
    new_meteor = Meteor(meteor, falling_speed)
    world.meteors.append(new_meteor)


def create_meat(world: World):
    meat = emoji("🥩")
    meat.x = randint(0, get_width() - meat.width)
    meat.y = -10
    falling_speed = randint(5, 15)
    new_meat = Meat(meat, falling_speed, False)
    world.meats.append(new_meat)


def falling_meteors(world: World):
    kept_meteors = []
    for meteor in world.meteors:
        meteor.meteorite.y += meteor.falling_speed
        if meteor.meteorite.y < get_height():
            kept_meteors.append(meteor)
        else:
            destroy(meteor.meteorite)
    world.meteors = kept_meteors


def falling_meats(world: World):
    kept_meat = []
    for meat in world.meats:
        meat.steak.y += meat.falling_speed
        if colliding(meat.steak, world.trex):
            world.trex.scale_y += .1
            world.score += 3
            destroy(meat.steak)
        else:
            kept_meat.append(meat)
    world.meats = kept_meat


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


def check_meteor_collision(world: World):
    for meteor in world.meteors:
        if (colliding(world.trex, meteor.meteorite)):
            world.trex.scale_y -= .05
            world.trex.scale_x += .05
            world.score -= 1


def check_platform_collision(world: World):
    for platform in world.platforms:
        if (world.trex.x < platform.x + platform.width
                and world.trex.x + world.trex.width > platform.x
                and world.trex.y < platform.y + platform.height
                and world.trex.y + world.trex.height > platform.y):
            if not world.is_jumping:
                world.trex.y = platform.y - world.trex.height * 0.6
            return True
    return False


def meteor_on_key(world: World):
    count = 3
    if randint(1, 10) % 2 == 0:
        while count > 0:
            create_meteor(world)
            count -= 1


def meat_on_key(world: World):
    if randint(1, 10) % 2 == 0:
        create_meat(world)


def jump_trex(world: World, key: str):
    if key == "space" and not world.is_jumping:
        world.is_jumping = True
        world.jump_height = JUMP_HEIGHT
        meteor_on_key(world)
        meat_on_key(world)


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
        meteor_on_key(world)
        meat_on_key(world)
    elif key == "right":
        head_right(world)
        meteor_on_key(world)
        meat_on_key(world)


def wall_pow(world: World):
    if world.trex.x > get_width():
        head_left(world)
        meteor_on_key(world)
        meat_on_key(world)
    elif world.trex.x < 0:
        head_right(world)
        meteor_on_key(world)
        meat_on_key(world)
    if world.trex.y < 0:
        world.trex.y = 0
        world.is_jumping = False



def game_end(world: World):
    if world.score <= -30:
        world.game_over = True


def display_score(world: World):
    if not world.game_over:
        # Update the score display
        world.words.text = f"Score: {world.score}"
    else:
        # Display game over message
        world.trex_speed = 0
        world.words.text = "GAME OVER! :P"


when('starting', create_world)
when("updating", move_trex)
when("typing", flip_trex)
when("typing", jump_trex)
when("updating", wall_pow)
when("updating", check_meteor_collision)
when("updating", falling_meteors)
when("updating", falling_meats)
when("updating", display_score)
when("updating", game_end)

start()




