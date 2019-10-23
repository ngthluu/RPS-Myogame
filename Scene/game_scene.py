from Scene.scene import *
import pygame
import ctypes
from Data.rec_data import *

class GameScene(Scene):

    def __init__(self, display, id, w_size, connector, resources):

        print("Game Scene")
        
        super().__init__(display, id, w_size, connector, resources)
        
        # Constants
        self.GET_DATA_TIME = 1.25
        self.FONT_PATH = r"..\Resource\OpenSans-Regular.ttf"

        self._is_in_intro = True
        self._intro_font = pygame.font.Font(self.FONT_PATH, 40)
        self._info_text = self._intro_font.render("You think you can beat my bot? Let's try", 0, (0, 0, 0))

        self._data_trainer = DataTrainer()
        self.NUM_OF_INPUT_SAMPLE = DataTrainer.NUM_OF_INPUT_SAMPLE
        self._input_data = []

        self._connector = connector

        self._ptr_accel = self._connector.get_accel()
        self._ptr_emg_data = self._connector.get_emg_data()

        self._clock = pygame.time.Clock()
        self._timer = 0
        self._movement_accel = [(0, 0, 0), (0, 0, 0)]
        self._has_wave = False

        self._turn_number = 0

        for i in range(len(self._resources)):
            self._resources[i] = pygame.transform.scale(self._resources[i], (125, 125))

        self._render_imgs = []
        offset = 450, (self._w_size[1] - self._resources[3].get_rect().size[1] * 2 * 1.2) // 2
        for i in range(6):  
            original_pos = (i % 3) * self._resources[3].get_rect().size[0] * 1.2, (i // 3) * self._resources[3].get_rect().size[1] * 1.2
            pos = tuple(map(lambda x, y: x + y, offset, original_pos))
            self._render_imgs.append([self._resources[3], pos])

    def update(self):

        super().update()

        if self._is_in_intro:
            self._timer += self._clock.tick() / 1000
            if self._timer >= 3.0:
                self._timer = 0
                self._is_in_intro = False
        else:
            if not self._has_wave:
                if self._timer <= 0.25:
                    if self._timer == 0:
                        temp = (ctypes.c_float * 3).from_address(self._ptr_accel)
                        self._movement_accel[0] = [temp[i] for i in range(3)]
                    self._timer += self._clock.tick() / 1000
                
                else:
                    self._timer = 0
                    temp = (ctypes.c_float * 3).from_address(self._ptr_accel)
                    self._movement_accel[1] = [temp[i] for i in range(3)]
                    ox = self._movement_accel[0][0]
                    x = self._movement_accel[1][0]
                    # Wave down
                    if x - ox < -0.7 and ox != 0:
                        self._has_wave = True
        
            else:
                if self._timer <= self.GET_DATA_TIME:
                    self._timer += self._clock.tick() / 1000
                    temp = (ctypes.c_int * DataTrainer.NUM_OF_SENSORS).from_address(self._ptr_emg_data)
                    self._input_data.append([temp[i] for i in range(DataTrainer.NUM_OF_SENSORS)])
                else:
                    # Finish delta_time second
                    self._timer = 0
                    self._has_wave = False

                    print(len(self._input_data))

                    predict_result = self._data_trainer.predict(self._input_data[:DataTrainer.NUM_OF_INPUT_SAMPLE])
                    self._render_imgs[self._turn_number + 3][0] = self._resources[predict_result]
                    self._render_imgs[self._turn_number][0] = self._resources[(predict_result + 1) % 3]
                
                    if self._turn_number < 2:
                        self._turn_number = self._turn_number + 1
                    else:
                        self._isEndScene = True

                    self._input_data = []
                

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
                else: pass
            else: pass

    def render(self):
        super().render()

        if self._is_in_intro:
            self._display.blit(self._info_text, fix_pos([self._w_size[0] // 2, self._w_size[1] // 2], self._info_text.get_size()))

        else:
            self._display.blit(self._resources[4], (120, 300))
            self._display.blit(self._resources[5], (120, 140))

            for i in range(6):
                self._display.blit(self._render_imgs[i][0], self._render_imgs[i][1])

        
        