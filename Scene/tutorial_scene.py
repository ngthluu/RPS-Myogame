from Scene.scene import *
import pygame
import ctypes
from Data.rec_data import *

class TutorialScene(Scene):

    def __init__(self, display, id, w_size, connector, resources):

        print ("Tutorial Scene")

        super().__init__(display, id, w_size, connector, resources)

        # Constants

        self.GET_DATA_TIME = 4.5
        
        self.ROCK_TITLE = "Wave out a rock and hold on for "+str(int(self.GET_DATA_TIME))+" seconds !"
        self.PAPER_TITLE = "Wave out a paper and hold on for "+str(int(self.GET_DATA_TIME))+" seconds !"
        self.SCISSORS_TITLE = "Wave out a scissors and hold on for "+str(int(self.GET_DATA_TIME))+" seconds !"
        self.FONT_PATH = r"..\Resource\OpenSans-Regular.ttf"
        
        # Init status text
        self._status_font = pygame.font.Font(self.FONT_PATH, 40)
        self._status_text = self._status_font.render(self.ROCK_TITLE, 0, (0, 0, 0))
        self._status_text_pos = (self._w_size[0] / 2, self._w_size[1] * 0.75)

        self._rock_img = self._resources[0]
        self._paper_img = self._resources[1]
        self._scissors_img = self._resources[2]

        self._img = self._rock_img
        self._img_pos = (self._w_size[0] / 2, self._w_size[1] * 0.35)
        self._img_size = self._img.get_rect().size
        
        self._on_rock_time = True
        self._rock_data = []

        self._on_paper_time = False
        self._paper_data = []

        self._on_scissors_time = False
        self._scissors_data = []

        self._ptr_accel = self._connector.get_accel()
        self._ptr_emg_data = self._connector.get_emg_data()

        self._clock = pygame.time.Clock()
        self._timer = 0
        self._movement_accel = [(0, 0, 0), (0, 0 ,0)]
        self._has_wave = False

        if os.path.isfile(DataTrainer.MODEL_FILE_PATH):
            self._isEndScene = True

    def update(self):
        super().update()

        # Check movement per 0.25s, capture vector movement to _movement_accel
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
                if x - ox < -0.75 and ox != 0:
                    self._has_wave = True
                    
        else:
            if self._timer <= self.GET_DATA_TIME:
                self._timer += self._clock.tick() / 1000
                self.collect_data()
            else:
                # Finish delta_time second
                self._timer = 0
                self._has_wave = False

                if self._on_rock_time:
                    print(len(self._rock_data))
                    self._on_rock_time = False
                    self._on_paper_time = True

                elif self._on_paper_time:
                    print(len(self._paper_data))
                    self._on_paper_time = False
                    self._on_scissors_time = True
                
                elif self._on_scissors_time:
                    print(len(self._scissors_data))
                    self._on_scissors_time = False
                    data_trainer = DataTrainer([self._rock_data[:DataTrainer.NUM_OF_TRAINING_SAMPLE], self._paper_data[:DataTrainer.NUM_OF_TRAINING_SAMPLE], self._scissors_data[:DataTrainer.NUM_OF_TRAINING_SAMPLE]])       
                    data_trainer.train() 
                    self._isEndScene = True        

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
        if self._has_wave:
            self._status_text = self._status_font.render(str(int(self.GET_DATA_TIME - self._timer)), 0, (0, 0, 0))
        else:
            if self._on_rock_time:
                self._img = self._rock_img
                self._status_text = self._status_font.render(self.ROCK_TITLE, 0, (0, 0, 0))
            elif self._on_paper_time:
                self._img = self._paper_img
                self._status_text = self._status_font.render(self.PAPER_TITLE, 0, (0, 0, 0))
            elif self._on_scissors_time:
                self._img = self._scissors_img
                self._status_text = self._status_font.render(self.SCISSORS_TITLE, 0, (0, 0, 0))

        self._display.blit(self._status_text, fix_pos(self._status_text_pos, self._status_text.get_size()))
        self._display.blit(self._img, fix_pos(self._img_pos, self._img_size))

    def collect_data(self):
        temp = (ctypes.c_int * DataTrainer.NUM_OF_SENSORS).from_address(self._ptr_emg_data)
        if self._on_rock_time:
            self._rock_data.append([temp[i] for i in range(DataTrainer.NUM_OF_SENSORS)])
        elif self._on_paper_time:
            self._paper_data.append([temp[i] for i in range(DataTrainer.NUM_OF_SENSORS)])
        elif self._on_scissors_time:
            self._scissors_data.append([temp[i] for i in range(DataTrainer.NUM_OF_SENSORS)])

    def reset_data(self):
        if self._on_rock_time:
            self._rock_data = []
        elif self._on_paper_time:
            self._paper_data = []
        elif self._on_scissors_time:
            self._scissors_data = []