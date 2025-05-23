import dataclasses
import functools
import json
import os
import tempfile

import maya.cmds as cmds

from CustomMT.job_manager import ScriptJobManagerBase
from CustomMT.menu_builder import MenuBuilder


@dataclasses.dataclass
class Sample1ToolParameterDC:
    watch_new_scene_opened: bool = False
    watch_selection_changed: bool = False


class __Single(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AppData(metaclass=__Single):
    save_data_path = os.path.join(tempfile.gettempdir(), 'CustomMT_sjm_sample1_save_data.json')
    temp_data: Sample1ToolParameterDC

    @classmethod
    def initialize(cls, data: Sample1ToolParameterDC = None):
        data = data or cls.load_from_file()
        print(cls.save_data_path)
        if not os.path.exists(cls.save_data_path):
            with open(cls.save_data_path, 'w', encoding='utf8') as f:
                f.write(json.dumps(dataclasses.asdict(data), indent=4))
        cls.save_data(data)
        cls.temp_data = cls.load_from_file()

    @classmethod
    def load_from_file(cls):
        try:
            if os.path.exists(cls.save_data_path):
                with open(cls.save_data_path, 'r', encoding='utf8') as f:
                    data = json.loads(f.read())
                    return Sample1ToolParameterDC(**data)
            else:
                return Sample1ToolParameterDC()
        except json.JSONDecodeError:
            return Sample1ToolParameterDC()

    @classmethod
    def save_data(cls, data: Sample1ToolParameterDC):
        with open(cls.save_data_path, 'w', encoding='utf8') as f:
            f.write(json.dumps(dataclasses.asdict(data), indent=4))


class ToolManager1(ScriptJobManagerBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print('ToolManager1 init'.center(50, '-'))

    def __del__(self):
        super().__del__()
        print('ToolManager1 del'.center(50, '-'))


class ToolManager2(ScriptJobManagerBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print('ToolManager2 init'.center(50, '-'))

    def __del__(self):
        super().__del__()
        print('ToolManager2 del'.center(50, '-'))


@ToolManager1.add_script_job_decorator(event=['NewSceneOpened', 'script'], )
def tool1(*args, **kwargs):
    cmds.confirmDialog(
        title='Tool1',
        message=f'Testing tool1\n' + 'NewSceneOpened',
        button=['OK'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel'
    )


def watch_new_scene_opened(check_on: bool, menu_name: str = None, *args, **kwargs):
    AppData.temp_data.watch_new_scene_opened = check_on
    cmds.menuItem(menu_name, edit=True, checkBox=check_on)

    if check_on:
        ToolManager1.run_jobs(debug_mode=True)
    else:
        ToolManager1.kill_jobs(debug_mode=True)

    AppData.save_data(AppData.temp_data)


@ToolManager2.add_script_job_decorator(event=['SelectionChanged', 'script'], )
def tool2(*args, **kwargs):
    print('selection changed')


def watch_selection_changed(check_on: bool, *args, **kwargs):
    print('*' * 3, 'event,SelectionChanged')
    AppData.temp_data.watch_selection_changed = check_on
    if check_on:
        ToolManager2.run_jobs(debug_mode=True)
    else:
        ToolManager2.kill_jobs(debug_mode=True)
    AppData.save_data(AppData.temp_data)


def close_tool_command():
    print('close_window'.center(50, '-'))
    ToolManager1.kill_jobs(debug_mode=True)
    ToolManager1.registration_script_job_list.clear()

    ToolManager2.kill_jobs(debug_mode=True)
    ToolManager2.registration_script_job_list.clear()


if __name__ == '__main__':
    AppData().initialize()
    WINDOW_NAME = 'myWindow'

    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME)
    cmds.window(WINDOW_NAME, menuBar=True, width=200, closeCommand=close_tool_command)

    cmds.menu(label='MainMenu1', tearOff=True)
    cmds.menuItem(divider=True, dividerLabel='Section 1')

    #
    watch_new_scene_opened_menu_name = 'watch_new_scene_opened'
    mi_check1 = cmds.menuItem(
        watch_new_scene_opened_menu_name,
        label=watch_new_scene_opened_menu_name,
        checkBox=AppData.temp_data.watch_new_scene_opened,
        command=functools.partial(watch_new_scene_opened,
                                  menu_name=watch_new_scene_opened_menu_name))
    if AppData.temp_data.watch_new_scene_opened:
        ToolManager1.run_jobs(debug_mode=True)

    menu_list = [
        {
            'parent': WINDOW_NAME,
            'label': 'MainMenu2',
            '__menu_items': [
                {
                    'label': 'MainMenu2-Sub1',
                    'command': watch_selection_changed,
                    'checkBox': AppData.temp_data.watch_selection_changed,
                }
            ]
        },
    ]
    menu_builder = MenuBuilder()

    menu_builder.build(menu_list)
    cmds.showWindow()

    for i in ToolManager1.registration_script_job_list:
        print(i.get_nice_name())
        print(i.is_job_running())
