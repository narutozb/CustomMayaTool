from maya import cmds

from .ui import UI


class MenuItem(UI):
    def __init__(self):
        super().__init__()
        self._cls = cmds.menuItem

    def create_divider(self, longDivider=False, dividerLabel='', *args, **kwargs):
        self.create(divider=True, longDivider=longDivider, dividerLabel=dividerLabel, *args, **kwargs)
        return self

    def create_check_box(self, *args, **kwargs):
        self.create(checkBox=True, *args, **kwargs)
        return self

    def create_sub_menu(self, *args, **kwargs):
        self.create(subMenu=True, *args, **kwargs)
        return self


class Menu(UI):
    def __init__(self):
        super().__init__()
        self._cls = cmds.menu

    def create_sub_menu_items(self, sub_menu_items: list[MenuItem]):
        for sub_menu_item in sub_menu_items:
            sub_menu_item.edit(parent=self.path)
