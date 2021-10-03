"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import math
from typing import List

import arcade
import arcade.gui

from health import backend

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1024
SCREEN_TITLE = "Vitality Trainer"
FOOD_FILE = "health/data/food.csv"
ACTIONS_FILE = "health/data/ActionEvents.csv"
LAYER_NAME_FOOD = "food"
LAYER_NAME_PLAYER = "player"
LAYER_NAME_HEALTHBAR = "bar"
LAYER_NAME_TEXT = "text"
START = 0
STOP = math.pi
CENTER_X: int = int(SCREEN_WIDTH / 2)
CENTER_Y: int = int(SCREEN_HEIGHT / 2)
INDENT_X: int = 400
INDENT_Y: int = 300
BALLOON_START: int = 100


def position_sprites(sprites: List[arcade.Sprite], scene: arcade.Scene):
    spacing = int(INDENT_X * 2 / (len(sprites) - 1))
    positons = range(int(CENTER_X - INDENT_X), int(CENTER_X + INDENT_X + spacing), spacing)
    for i, sprite in enumerate(sprites):
        sprite.center_x = positons[i]
        sprite.center_y = CENTER_Y + INDENT_Y
        scene.add_sprite(LAYER_NAME_FOOD, sprite)


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """
    foodlist: List[backend.food]
    manager: arcade.gui.UIManager
    player: backend.player
    scene: arcade.Scene
    FOOD_PLACED: bool = False
    BAR_PLACED: bool = False
    gameBackend: backend.Backend
    healthSprite: arcade.Sprite
    healthBar: backend.healthBar
    SETUP: bool = False
    TEXT_PLACED: bool = False

    def __init__(self, width, height, title):
        super().__init__(width, height, title, vsync=True)

        arcade.set_background_color(arcade.color.WHITE)
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.physics_engine = None

        # If you have sprite lists, you should create them here,
        # and set them to None

    def get_events(self):
        if self.FOOD_PLACED:
            self.scene.remove_sprite_list_by_name(LAYER_NAME_FOOD)
        self.foodlist = self.gameBackend.get_events()
        position_sprites(self.foodlist, self.scene)
        self.FOOD_PLACED = True

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.FOOD_PLACED = False
        self.BAR_PLACED = False
        self.TEXT_PLACED = False
        self.gameBackend = backend.Backend(FOOD_FILE, ACTIONS_FILE)
        arcade.set_background_color(arcade.color.WHITE)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.player = self.gameBackend.get_player()
        self.scene = arcade.scene.Scene()
        self.get_events()
        self.reset_player()
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player)
        self.healthBar = backend.healthBar(self.player)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, [])
        self.SETUP = True

    def getBar(self):
        if self.BAR_PLACED:
            self.scene.remove_sprite_list_by_name(LAYER_NAME_HEALTHBAR)
        self.healthBar.get_image()
        self.healthSprite = self.healthBar.sprite
        self.healthSprite.center_x = (self.healthSprite.width / 2) + 20
        self.healthSprite.center_y = self.healthSprite.height / 2 + 27
        self.scene.add_sprite(LAYER_NAME_HEALTHBAR, self.healthSprite)

    def reset_player(self):
        self.player.center_y = SCREEN_HEIGHT / 2 - BALLOON_START
        self.player.center_x = SCREEN_WIDTH / 2

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        self.manager.draw()
        self.scene.draw()
        # Call draw() on all your sprite lists below

    def generate_text(self):
        if self.TEXT_PLACED:
            self.scene.remove_sprite_list_by_name(LAYER_NAME_TEXT)
        if self.SETUP:
            text = arcade.text_pillow.create_text_sprite(self.gameBackend.get_text(),
                                                         self.healthSprite.center_x - 20,
                                                         self.healthSprite.center_y - 20,
                                                         color=arcade.color.BLUE,
                                                         font_size=20, width=INDENT_X)
            self.scene.add_sprite(LAYER_NAME_TEXT, text)
            self.TEXT_PLACED = True

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        self.physics_engine.update()
        food_collisions = self.player.collides_with_list(
            self.scene.get_sprite_list(LAYER_NAME_FOOD))
        self.getBar()
        for food in food_collisions:
            self.reset_player()
            self.player.eatFood(food)
            self.gameBackend.event()
            self.get_events()
        if self.player.motivation < 0:
            self.game_over()
        self.generate_text()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = self.player.getSpeed()
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -self.player.getSpeed()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -self.player.getSpeed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = self.player.getSpeed()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """

        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """

        pass

    def game_over(self):
        messagebox = arcade.gui.UIMessageBox(width=300, height=200, message_text="You Lost")
        self.manager.add(messagebox)
        self.setup()

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
