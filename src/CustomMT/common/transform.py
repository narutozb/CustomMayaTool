from maya import cmds


class Transform:

    @classmethod
    def is_group(cls, name: str):
        """
        检查是否为组
        :return:
        """
        if cmds.objectType(name, isType='transform'):
            if len(cmds.listRelatives(name, children=True, shapes=True) or []) == 0:
                return True

        return False

    @classmethod
    def is_empty_group(cls, name: str):
        """
        检查是否为空组
        :return:
        """
        if cls.is_group(name):
            if len(cmds.listRelatives(name, children=True) or []) == 0:
                return True
            else:
                return False

        raise BaseException(f'{name} is not a group!')
