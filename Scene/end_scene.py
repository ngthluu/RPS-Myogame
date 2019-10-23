from Scene.scene import *
import pygame


class EndScene(Scene):

    def __init__(self, display, id, w_size, connector, resources):
        super().__init__(display, id, w_size, connector, resources)

        self._status_font = pygame.font.Font(self.FONT_PATH, 40)
        self._status_text = self._status_font.render("You think you can beat my bot? Let's try", 0, (0, 0, 0))

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