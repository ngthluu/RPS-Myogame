from Scene.scene import *
import pygame


class EndScene(Scene):

    def __init__(self, display, id, w_size, connector, resources):
        super().__init__(display, id, w_size, connector, resources)

        #Constants
        self.FONT_PATH = r"..\Resource\OpenSans-Regular.ttf"

        self._status_font = pygame.font.Font(self.FONT_PATH, 40)
        self._status_text = self._status_font.render("Better luck next time ", 0, (0, 0, 0))

        self._resources[6] = pygame.transform.scale(self._resources[6], (125, 125))

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
                else: pass
            else: pass

    def render(self):
        super().render()

        self._display.blit(self._status_text, fix_pos([self._w_size[0] * 0.45, self._w_size[1] // 2], self._status_text.get_size()))
        self._display.blit(self._resources[6], (650, 230))