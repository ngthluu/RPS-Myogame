import os
import ctypes
import pygame
from Scene.scene_manager import SceneManager
from Scene.tutorial_scene import TutorialScene
from Scene.game_scene import GameScene
from Scene.end_scene import EndScene

# Game constants
FPS = 60
WORLD_SIZE = WIDTH, HEIGHT = 960, 600
WORLD_COLOR = 255, 255, 255
GAME_TITLE = "RPS - Myo Demo V1.0.0"

# Game variables
os.chdir(os.getcwd() + r"\lib")
connector = ctypes.cdll.LoadLibrary(os.getcwd() + r"\MyoData.dll")

# Game init
pygame.init()
pygame.font.init()

pygame.display.set_caption(GAME_TITLE)
game_display = pygame.display.set_mode(WORLD_SIZE)

scene_manager = SceneManager()
scene_manager.set_scene(TutorialScene(game_display, 1, WORLD_SIZE))

# Game loop
if connector.init():
    try:
        while True:
            # Get data
            connector.run(FPS)
            pointer_emg = connector.get_emg_data()
            temp = (ctypes.c_int * 8).from_address(pointer_emg)
            data_list = [temp[i] for i in range(8)]
            print(data_list)

            # Updating game
            pygame.time.delay(1000 // FPS)
            game_display.fill(WORLD_COLOR)

            if scene_manager.get_scene().end():
                if scene_manager.get_scene().get_id() == 1:
                    scene_manager.set_scene(GameScene(game_display, 2, WORLD_SIZE))
                elif scene_manager.get_scene().get_id() == 2:
                    scene_manager.set_scene(EndScene(game_display, 3, WORLD_SIZE))
                elif scene_manager.get_scene().get_id() == 3:
                    scene_manager.set_scene(GameScene(game_display, 2, WORLD_SIZE))
                else:
                    pass
            scene_manager.get_scene().update()
            scene_manager.get_scene().render()

            pygame.display.update()


    except KeyboardInterrupt as e:
        print("Exiting...")
        connector.close()
        pygame.quit()
        exit()
else:
    print("Unable to connect to the Myo Armband !")