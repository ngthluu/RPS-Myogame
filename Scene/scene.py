# Other fuction
def fix_pos(pos, size):
    return (pos[0] - size[0] / 2, pos[1] - size[1] / 2)

class Scene:

    def __init__(self, display, id, w_size, connector, resources):
        self._isEndScene = False
        self._display = display
        # id = 1 means tut_scene, id = 2 means game_scene, id = 3 means end_scene
        self._id = id
        self._w_size = w_size
        self._connector = connector
        self._resources = resources

    def update(self):
        pass

    def render(self):
        pass

    def get_id(self):
        return self._id

    def end(self):
        return self._isEndScene