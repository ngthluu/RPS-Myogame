from Scene.scene import *
import pygame

class TutorialScene(Scene):

    def __init__(self, display, id, w_size, connector, resources):
        super().__init__(display, id, w_size, connector, resources)

        # Init status text
        self._status_text = pygame.font.Font(r"..\Resource\OpenSans-Regular.ttf", 32).render("Wave out a rock and hold on for 3 seconds !", 1, (0, 0, 0))
        self._status_text_pos = (self._w_size[0] / 2, self._w_size[1] * 0.75)

        self._rock = self._resources[0]
        self._rock_pos = (self._w_size[0] / 2, self._w_size[1] * 0.35)
        self._rock_size = self._rock.get_rect().size

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
        self._display.blit(self._status_text, fixPosition(self._status_text_pos, self._status_text.get_size()))
        self._display.blit(self._rock, fixPosition(self._rock_pos, self._rock_size))
