from maya import cmds


class UI:
    def __init__(self, ):
        self.path = None
        self._cls: callable = None

    def delete_ui(self, *args, **kwargs):
        cmds.deleteUI(self.path, *args, **kwargs)

    def edit(self, *args, **kwargs):
        self._cls(self.path, edit=True, *args, **kwargs)

    def create(self, *args, **kwargs):
        self.path = self._cls(*args, **kwargs)
        return self
