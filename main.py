import os
import ctypes
import pygame

# Game constants
FPS = 60
WORLD_SIZE = WIDTH, HEIGHT = 960, 600
WORLD_COLOR = 255, 255, 255
GAME_TITLE = "RPS - Myo Demo V1.0.0"

# Game variables
os.chdir(os.getcwd() + r"\lib")
connector = ctypes.cdll.LoadLibrary(os.getcwd() + r"\MyoData.dll")

# Game init
pygame.display.set_caption(GAME_TITLE)
game_display = pygame.display.set_mode(WORLD_SIZE)


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

            # Rendering game
            

    except KeyboardInterrupt as e:
        print("Exiting...")
        pygame.quit()
        connector.close()
else:
    print("Unable to connect to the Myo Armband !")