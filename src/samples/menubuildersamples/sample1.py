import functools

from maya import cmds, mel

from CustomMT.menu_builder import MenuBuilder


def test_function(*args, **kwargs):
    name: str = kwargs.get('name', 'test_function')
    print(name.center(50, '-'))
    print(f'args: {args}, kwargs: {kwargs}')


def test_check_box_function(*args, **kwargs):
    name: str = kwargs.get('name', 'test_function1')
    print(name.center(50, '-'))
    print(f'args: {args}, kwargs: {kwargs}')


print('测试mel'.center(50, '-'))
if __name__ == '__main__':
    # 示例：窗口创建和菜单配置
    window_name = 'TestWindow'
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    window = cmds.window(window_name, menuBar=True)

    menu_list = [
        {
            'parent': window,
            'label': 'Menu 1',
            'tearOff': True,
            '__menu_items': [
                {
                    'label': 'Sub Menu 1',
                    'command': test_function
                },
                {
                    'label': 'Sub Menu 2',
                    '__sub_items': [
                        {
                            'label': 'Sub Menu 2-1',
                            'command': functools.partial(test_function, name='Sub Menu 2-1'),

                        },
                        {
                            'label': 'Sub Menu 2-2',
                            'command': functools.partial(test_function, name='Sub Menu 2-2'),
                        },
                        {
                            'divider': True,
                            'dividerLabel': 'divider'},
                        {
                            'label': 'Sub Menu 2-3',
                            'command': 'print("Sub Menu 2-3")'
                        },
                        {
                            'label': 'Sub Menu 2-4',
                            '__sub_items': [
                                {
                                    'label': 'Sub Menu 2-4-1',
                                    'checkBox': True,
                                },
                            ]
                        }
                    ],
                },
            ],
        },
        {
            'parent': window, 'label': 'Menu 2',
            'tearOff': True,
            '__menu_items': [
                {
                    'label': 'Sub Menu2 2-1',
                    'checkBox': True,
                    'command': functools.partial(test_check_box_function, name='Sub Menu2 2-1'),
                }
            ],
        },
    ]

    # 通过 MenuBuilder 递归构建菜单结构
    menu_builder = MenuBuilder()
    menu_builder.build(menu_list)

    cmds.showWindow(window)
