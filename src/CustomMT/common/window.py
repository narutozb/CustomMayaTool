from maya import cmds, mel

from .ui import UI


class Window(UI):

    def __init__(self):
        super().__init__()
        self._cls = cmds.window

    def show(self):
        cmds.showWindow(self.path)

    def close(self):
        self.close_windows([self.path])

    @classmethod
    def get_main_window(cls, ):
        """
        获取 Maya 主窗口的名称
        :return: 主窗口名称
        """

        return mel.eval('$tmpVar=$gMainWindow')

    @classmethod
    def close_windows(cls, name_list: list[str] = None):
        """
        关闭指定名称的窗口
        :param name_list: 窗口名称列表
        """
        if name_list is None:
            name_list = []

        result = []
        for name in name_list:
            if cmds.window(name, exists=True):
                if name != cls.get_main_window():
                    try:
                        cmds.deleteUI(name)
                        result.append(name)
                    except Exception as e:
                        # 忽略可能出现的错误，例如窗口已被删除
                        raise e
        return result

    @classmethod
    def close_all_windows(cls, exclude_windows: list[str] = None):
        """
        关闭所有窗口，排除指定的窗口
        """
        result = []
        # 获取当前打开的所有窗口
        open_windows = cmds.lsUI(windows=True)
        for window in open_windows:
            # 如果窗口在排除列表中，则跳过
            if exclude_windows and window in exclude_windows:
                continue
            # 排除主 Maya 窗口
            if window != cls.get_main_window() and cmds.window(window, exists=True):
                try:
                    cmds.deleteUI(window, window=True)
                    result.append(window)
                except Exception as e:
                    # 忽略可能出现的错误，例如窗口已被删除
                    raise e
        return result
