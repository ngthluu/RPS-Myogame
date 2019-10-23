from Scene.scene import *
import pygame
import ctypes
from Data.rec_data import *

class GameScene(Scene):

    def __init__(self, display, id, w_size, connector, resources):

        print("Game Scene")
        
        super().__init__(display, id, w_size, connector, resources)
        
        # Constants
        self.GET_DATA_TIME = 1.0

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

    def update(self):

        super().update()

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

                print(self._data_trainer.predict(self._input_data[:DataTrainer.NUM_OF_INPUT_SAMPLE]))
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