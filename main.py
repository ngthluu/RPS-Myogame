import os
import ctypes
import pygame
from Scene.scene_manager import SceneManager
from Scene.tutorial_scene import TutorialScene
from Scene.game_scene import GameScene
from Scene.end_scene import EndScene

# Game constants
FPS = 100
WORLD_SIZE = WIDTH, HEIGHT = 960, 600
WORLD_COLOR = 255, 255, 255
GAME_TITLE = "RPS - Myo Demo V1.0.0"

# Game variables
os.chdir(os.getcwd() + r"\Library")
connector = ctypes.cdll.LoadLibrary(os.getcwd() + r"\MyoData.dll")

# Game init
pygame.init()
pygame.font.init()

pygame.display.set_caption(GAME_TITLE)
game_display = pygame.display.set_mode(WORLD_SIZE)

# Preload resources

rock_img = pygame.image.load(r"..\Resource\Rock.png")
paper_img = pygame.image.load(r"..\Resource\Paper.png")
scissors_img = pygame.image.load(r"..\Resource\Scissors.png")
mystery_img = pygame.image.load(r"..\Resource\Mystery.png")

human_img = pygame.image.load(r"..\Resource\Human.jpg")
robot_img = pygame.image.load(r"..\Resource\Robot.png")

resources = [rock_img, paper_img, scissors_img, mystery_img, human_img, robot_img]

# Scene manager
scene_manager = SceneManager()

# Game loop
if connector.init():

    scene_manager.set_scene(TutorialScene(game_display, 1, WORLD_SIZE, connector, resources))

    while True:
        # Run the connector
        connector.run(FPS)

        # Updating game
        game_display.fill(WORLD_COLOR)

        if scene_manager.get_scene().end():
            if scene_manager.get_scene().get_id() == 1:
                scene_manager.set_scene(GameScene(game_display, 2, WORLD_SIZE, connector, resources))
            elif scene_manager.get_scene().get_id() == 2:
                scene_manager.set_scene(EndScene(game_display, 3, WORLD_SIZE, connector, resources))
            elif scene_manager.get_scene().get_id() == 3:
                scene_manager.set_scene(GameScene(game_display, 2, WORLD_SIZE, connector, resources))
            else:
                pass
        scene_manager.get_scene().update()
        scene_manager.get_scene().render()

        pygame.display.update()
        pygame.time.delay(1000 // FPS)
else:
    connector.close()
    print("Unable to connect to the Myo Armband !")
