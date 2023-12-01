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

@dataclass
class Dino:
   body: DesignerObject
   falling_speed: int


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
   dinos: list[Dino]


def create_world() -> World:
   """
       This function returns the in game world.

       Returns:
           World: What is displayed in the game
   """
   return World(create_volcano(), create_trex(),
                TREX_SPEED, False, 0, create_platforms(),
                [], text("black", "", 25, get_width() // 6, 8), score=0, game_over=False,
                meats=[], dinos=[])


def create_volcano() -> DesignerObject:
   """
       This function creates a volcano, which is then later used as a
       field in the World dataclass.

       Returns:
           DesignerObject: The volcano emoji with a specific size and position
   """
   volcano = emoji("🌋")
   volcano.y = get_height() * (.59)
   volcano.scale_x = 25
   volcano.scale_y = 20
   return volcano


def create_trex() -> DesignerObject:
   """
       This function creates a trex, which is then later used as a
       field in the World dataclass.

       Returns:
           DesignerObject: The trex emoji with a specific size and position
   """
   trex = emoji("🦖")
   trex.y = get_height() * (.93)
   trex.flip_x = True
   trex.scale_x = 2
   trex.scale_y = 2
   return trex


def create_meteor(world: World):
   """
       This function creates a meteor, which is then later added to a
       field in the World dataclass.

       Args:
           world(World): Uses the world dataclass to append an object to
           one of its field lists.
   """
   meteor = emoji("comet")
   meteor.x = randint(0, get_width() - meteor.width)
   meteor.y = -10
   falling_speed = randint(5, 15)
   new_meteor = Meteor(meteor, falling_speed)
   world.meteors.append(new_meteor)


def create_meat(world: World):
   """
       This function creates meat, which is then later added to a
       field in the World dataclass.

       Args:
           world(World): Uses the world dataclass to append an object to
           one of its field lists.
   """
   meat = emoji("🥩")
   meat.x = randint(0, get_width() - meat.width)
   meat.y = -10
   falling_speed = randint(5, 15)
   new_meat = Meat(meat, falling_speed)
   world.meats.append(new_meat)

def create_dino(world: World):
   """
       This function creates a dino, which is then later added to a
       field in the World dataclass.

       Args:
            world(World): Uses the world dataclass to append an object to
            one of its fields.
   """
   dino = emoji("🦕")
   dino.x = randint(0, get_width() - dino.width)
   dino.y = -10
   falling_speed = randint(15, 20)
   new_dino = Dino(dino, falling_speed)
   world.dinos.append(new_dino)

def falling_meteors(world: World):
   """
       This function makes the meteors in the meteors field fall and then
       disappear once they hit the ground

       Args:
           world(World): The dataclass is accessed in order to make the
            objects in the meteors field fall
   """
   kept_meteors = []
   for meteor in world.meteors:
       meteor.meteorite.y += meteor.falling_speed
       if meteor.meteorite.y < get_height():
           kept_meteors.append(meteor)
       else:
           destroy(meteor.meteorite)
   world.meteors = kept_meteors


def falling_meats(world: World):
   """
           This function makes the meat in the meats field fall and then
           disappear once the dinosaur "eats" them

           Args:
               world(World): The dataclass is accessed in order to make the
               objects in the meats field fall
   """
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

def falling_dinos(world: World):
   """
       This function makes the dino in the dinos field fall and then
       disappear once the dinosaur "eats" them

       Args:
           world(World): The dataclass is accessed in order to make the
           objects in the dinos field fall
   """
   kept_dinos= []
   for dino in world.dinos:
       dino.body.y += dino.falling_speed
       if colliding(dino.body, world.trex):
           world.trex.scale_y = 50
           world.trex.scale_x = 50
           world.score += 100
           destroy(dino.body)
       else:
           kept_dinos.append(dino)
   world.dinos = kept_dinos

def create_platforms() -> list[DesignerObject]:
   """
       This function returns list of DesignerObjects that are used in the
       platforms field in the world dataclass.

       Returns:
           list[DesignerObject]: A list of rectangles that act as platforms
           for the game
   """
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
   """
       This function changes world.trex and world.score if there was any collision
       between the trex and any of the meteors in the world.meteors

       Args:
           world(World): The game world dataclass with the trex, score, and
           meteors field
   """
   for meteor in world.meteors:
       if (colliding(world.trex, meteor.meteorite)):
           world.trex.scale_y -= .05
           world.trex.scale_x += .05
           world.score -= 1


def check_platform_collision(world: World):
   """
       This function makes it so that the dinosaur can sit on top of the
       in game platforms when colliding with them

       Args:
           world(World): The game world dataclass with the trex and platforms
   """
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
   """
       This function has a 50% of calling the create_meteor function three times.

       Args:
           world(World): The game world dataclass
   """
   count = 3
   if randint(1, 10) % 2 == 0:
       while count > 0:
           create_meteor(world)
           count -= 1



def meat_on_key(world: World):
   """
       This function has a 50% of calling the create_meat function

       Args:
           world(World): The game world dataclass
   """
   if randint(1, 10) % 2 == 0:
       create_meat(world)

def dino_on_key(world: World):
   """
       This function has a 1 in 20 of calling the create_dino function three

       Args:
           world(World): The game world dataclass
   """
   if randint(1, 20) % 15 == 0:
       create_dino(world)

def jump_trex(world: World, key: str):
   """
       This makes it so that the dinosaur is able to jump when the space key is
       pressed.

       Args:
           world(World): The game world dataclass
           key(str): The key that the player presses
   """
   if key == "space" and not world.is_jumping:
       world.is_jumping = True
       world.jump_height = JUMP_HEIGHT
       meteor_on_key(world)
       meat_on_key(world)
       dino_on_key(world)


def head_left(world: World):
   """
       This makes it so that the dinosaur's goes to the left.

       Args:
           world(World): The game world dataclass
   """
   world.trex_speed = -TREX_SPEED
   world.trex.flip_x = False


def head_right(world: World):
   """
       This makes it so that the dinosaur object flips and
       goes to the right

       Args:
           world(World): The game world dataclass
   """
   world.trex_speed = TREX_SPEED
   world.trex.flip_x = True


def move_trex(world: World):
    """
        This function changes the direction of the trex whenever the appropriate
        keys are pressed. left: changes the t-rex's direction to move to the left.
        right: changes the t-rex's direction to move to the right.
        args:
         - world dataclass with the trex field
         - the check for collisions function
        returns:
         - an action that changes to trex and makes it move around on the screen
         when keys are clicked.
    """
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
    """
    This function changes the direction of the trex whenever the appropriate
    keys are pressed. left: changes the t-rex's direction to move to the left.
    right: changes the t-rex's direction to move to the right.
    args:
    - world dataclass with the key field
    returns:
    - an action that changes the direction of the trex when a left or right key
       is pressed.
    """

    if key == "left":
       head_left(world)
       meteor_on_key(world)
       meat_on_key(world)
       dino_on_key(world)
    elif key == "right":
       head_right(world)
       meteor_on_key(world)
       meat_on_key(world)
       dino_on_key(world)


def wall_pow(world: World):
    """
        This function changes the direction of the trex is it touches a wall.
        args:
           - world dataclass with the trex field
        returns:
           - does an action which is changing the direction of the trex
    """
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
    """
        This function ends the game if the user has either won(30p) or lost(-30p)
        args:
         - world dataclass with the game over field
        returns:
         - ends the game for the user, after they've won or lost
    """

    if world.score <= -30 or world.score >= 30:
       world.game_over = True


def display_score(world: World):
    """
        This function is to keep track of the user's score.
        args:
        - world dataclass with the score field
        returns:
        - displays the score of the user
    """

    if not world.game_over:
       world.words.text = f"Score: {world.score}"
    elif world.game_over and world.score >= 30:
       world.trex_speed = 0
       world.words.text = "YOU WIN!"
       world.words.color = "red"
       world.words.text_size = 100
       world.words.y = get_height() // 2
       world.words.x = get_width() // 2
    elif world.game_over and world.score <= -30:
       world.trex_speed = 0
       world.words.text = "GAME OVER! :P"
       world.words.color = "red"
       world.words.text_size = 100
       world.words.y = get_height()//2
       world.words.x = get_width()//2

def game_is_done(world:World)->bool:
    """
       This function completely ends the game
       args:
       - world dataclass with the game_over field
       returns:
       - ends the game for the user
   """

    return world.game_over

when('starting', create_world)
when("updating", move_trex)
when("typing", flip_trex)
when("typing", jump_trex)
when("updating", wall_pow)
when("updating", check_meteor_collision)
when("updating", falling_meteors)
when("updating", falling_meats)
when("updating", falling_dinos)
when("updating", display_score)
when("updating", game_end)
when(game_is_done, display_score, pause)

start()






