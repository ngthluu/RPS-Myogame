from Scene.scene import *
import pygame
import ctypes

class TutorialScene(Scene):

    def __init__(self, display, id, w_size, connector, resources):
        super().__init__(display, id, w_size, connector, resources)

        # Constants
        ROCK_TITLE = "Wave out a rock and hold on for 3 seconds !"
        PAPER_TITLE = "Wave out a paper and hold on for 3 seconds !"
        SCISSORS_TITLE = "Wave out a scissors and hold on for 3 seconds !"
        FONT_PATH = r"..\Resource\OpenSans-Regular.ttf"

        # Init status text
        self._status_text = pygame.font.Font(FONT_PATH, 32).render(ROCK_TITLE, 1, (0, 0, 0))
        self._status_text_pos = (self._w_size[0] / 2, self._w_size[1] * 0.75)

        self._rock = self._resources[0]
        self._rock_pos = (self._w_size[0] / 2, self._w_size[1] * 0.35)
        self._rock_size = self._rock.get_rect().size
        
        self._on_rock_time = True
        self._on_paper_time = False
        self._on_scissors_time = False

        self._ptr_accel = self._connector.get_accel()
        self._ptr_rotation = self._connector.get_rotation()
        self._ptr_gyro = self._connector.get_gyro()

        self._clock = pygame.time.Clock()
        self._timer = 0
        self._movement_accel = [(0, 0, 0), (0, 0 ,0)]

    def update(self):
        super().update()

        # Check movement per 0.25s
        if self._timer <= 0.25:
            if self._timer == 0:
                temp = (ctypes.c_float * 3).from_address(self._ptr_accel)
                self._movement_accel[0] = [temp[i] for i in range(3)]
            self._timer += self._clock.tick() / 1000
        else:
            temp = (ctypes.c_float * 3).from_address(self._ptr_accel)
            self._movement_accel[1] = [temp[i] for i in range(3)]
            ox = self._movement_accel[0][0]
            x = self._movement_accel[1][0]
            print((ox, x))
            if x - ox >= 0.3:
                print("Move down")
                print ((ox, x))
            elif x - ox <= -0.3:
                print("Move up")
                print ((ox, x))
            self._timer = 0

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting...")
                self._connector.close()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Change Scene to Game Scene:
                    self._isEndScene = True
                else: 
                    pass
            else: 
                pass

    def render(self):
        super().render()
        self._display.blit(self._status_text, fix_pos(self._status_text_pos, self._status_text.get_size()))
        self._display.blit(self._rock, fix_pos(self._rock_pos, self._rock_size))
