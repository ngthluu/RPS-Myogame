class Scene:

    def __init__(self, display, id, w_size, connector):
        self._isEndScene = False
        self._display = display
        # id = 1 means tut_scene, id = 2 means game_scene, id = 3 means end_scene
        self._id = id
        self._w_size = w_size
        self._connector = connector

    def update(self):
        pass

    def render(self):
        pass

    def get_id(self):
        return self._id

    def end(self):
        return self._isEndScene