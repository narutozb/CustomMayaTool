from maya import cmds, mel


class CustomMenu:
    def __init__(self):
        self.name = None

    def create_menu(self, **kwargs):
        self.name = cmds.menu(**kwargs)
        return self.name

    def edit_menu(self, **kwargs):
        cmds.menu(self.name, edit=True, **kwargs)


class CustomMenuItem:
    def __init__(self):
        self.name = None

    def create_menu_item(self, subMenu=False, **kwargs):
        self.name = cmds.menuItem(subMenu=subMenu, **kwargs)
        return self.name

    def edit_menu_item(self, **kwargs):
        cmds.menuItem(self.name, edit=True, **kwargs)


class MenuBuilder:
    """
    MenuBuilder 用于根据配置结构递归创建菜单及其子菜单项，
    支持顶层菜单和内层菜单项的统一构建，并自动注入父对象的 name。

    参数说明：
        top_children_key: 顶层菜单中的子项配置键（默认为"__menu_items"）
        item_children_key: 非顶层菜单项中的子项配置键（默认为"__sub_items"）
    """

    def __init__(self, top_children_key="__menu_items", item_children_key="__sub_items"):
        self.top_children_key = top_children_key
        self.item_children_key = item_children_key

    def filter_config(self, config: dict) -> dict:
        """
        过滤字典中所有以"__"开头的自定义键，返回供 Maya cmds 调用的参数字典。
        """
        filter_list = [
            self.top_children_key, self.item_children_key
        ]
        return {k: v for k, v in config.items() if k not in filter_list}

    def build(self, configs: list, parent: str = None):
        """
        递归构建菜单：
          - 如果 parent 为 None，则认为是顶层菜单，使用 CustomMenu 创建。
          - 否则使用 CustomMenuItem 创建菜单项，并自动添加 parent 参数。

        当检测到配置字典中存在对应的子菜单键（顶层使用 self.top_children_key，
        内层使用 self.item_children_key）时，自动添加 subMenu=True（仅对内层有效）并递归构建。
        """
        # 根据是否有父节点判断当前层级及应使用的 children_key 和构造器
        if parent is None:
            children_key = self.top_children_key
            BuilderClass = CustomMenu
        else:
            children_key = self.item_children_key
            BuilderClass = CustomMenuItem

        for config in configs:
            # 过滤自定义键，得到实际传递给 Maya 命令的数据
            data = self.filter_config(config)
            # 如果处于子层级，自动注入 parent 参数
            if parent:
                data["parent"] = parent

            # 检查是否存在子菜单配置
            children = config.get(children_key)
            if children and parent is not None:
                # 内层菜单如果有子菜单，需要标记 subMenu=True
                data["subMenu"] = True

            # 根据当前层级创建对应的对象
            builder = BuilderClass()
            if parent is None:
                created_name = builder.create_menu(**data)
            else:
                created_name = builder.create_menu_item(**data)

            # 递归处理子菜单数据
            if children:
                self.build(children, parent=created_name)
