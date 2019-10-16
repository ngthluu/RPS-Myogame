from Scene.scene import *
import pygame

class TutorialScene(Scene):

    def __init__(self, display, id, w_size, connector):
        super().__init__(display, id, w_size, connector)

    def update(self):
        super().update()
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
