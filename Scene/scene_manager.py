class SceneManager:

    def __init__(self):
        self.scm = []

    def set_scene(self, scene):
        if len(self.scm) > 0:
            self.scm.pop()
            self.scm.append(scene)
        else:
            self.scm.append(scene)

    def get_scene(self): return self.scm[0]