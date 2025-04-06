import functools
import typing
from typing import Optional

from maya import cmds


class CustomJob:
    def __init__(self, script_job_params: dict, func_name: str = None, custom_params: dict = None, **kwargs):
        self.script_job_params = script_job_params
        self.func_name = func_name or ''
        self.job_id: Optional[int] = None
        self.custom_params = custom_params or {}

    @classmethod
    def get_running_job_id_list(cls) -> list:
        """
        获取当前运行的脚本任务ID列表
        :return:
        """
        job_id_list = [int(_.split(':')[0]) for _ in cmds.scriptJob(listJobs=True)]
        return job_id_list

    def get_nice_name(self) -> str:
        """
        生成脚本任务的友好名称
        使用肉串化的参数名称和函数名称来生成一个名称
        格式为：<函数名称>-<参数名称1>-<参数名称2>...
        :return:
        """
        name = self.func_name
        sorted_key_list = sorted(list(self.script_job_params.keys()))
        for k in sorted_key_list:
            values = self.script_job_params[k]
            if isinstance(values, list) and len(values) == 2 and isinstance(values[1], typing.Callable):
                name += f'-{values[0]}-{values[1].__name__}'
            else:
                name += f'-{k}'
        return name

    def is_job_running(self) -> bool:
        """
        检查脚本任务是否存在
        :return:
        """
        if self.job_id in self.get_running_job_id_list():
            return True
        else:
            self.job_id = None
            return False

    def run_job(self, debug_mode: bool = False):
        if not self.is_job_running():
            self.job_id = cmds.scriptJob(**self.script_job_params)
        if debug_mode:
            print(f'Running job: {self.job_id}')

    def kill_job(self, debug_mode: bool = False):
        if self.is_job_running():
            if debug_mode:
                print(f'Killing job: {self.job_id}')
            cmds.scriptJob(kill=self.job_id)


class _JobManagerMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ScriptJobManagerBase(metaclass=_JobManagerMeta):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        cls.registration_script_job_list: list[CustomJob] = []

    @classmethod
    def add_job(cls, custom_job: CustomJob):
        cls.registration_script_job_list.append(custom_job)

    @classmethod
    def run_jobs(cls, debug_mode: bool = False):
        """
        运行所有注册的脚本任务
        :return:
        """
        for i in cls.registration_script_job_list:
            i.run_job(debug_mode=debug_mode)

    @classmethod
    def kill_jobs(cls, debug_mode: bool = False):
        """
        终止所有注册的脚本任务
        :return:
        """
        for i in cls.registration_script_job_list:
            i.kill_job(debug_mode=debug_mode)

    @classmethod
    def add_script_job_decorator(cls, **decorator_kwargs):
        r"""
        该装饰器将函数注册为脚本任务，并在函数定义时添加到脚本任务列表中。
        参数参考 maya.cmds.scriptJob 的参数
        :param decorator_kwargs:
        :return:
        """
        # custom_parameters = decorator_kwargs.pop('__CustomParameters', {})  # 自定义属性
        custom_params = {}
        # 当键名以"__"开头时，表示是自定义参数
        for i in list(decorator_kwargs.keys()):
            if i.startswith('_') and i != 'func_name':
                custom_params[i] = decorator_kwargs.pop(i)

        def decorator(func):
            # 在函数定义时注册（只注册一次）
            for condition, lst in decorator_kwargs.items():
                if isinstance(lst, list) and len(lst) == 2 and lst[1] == 'script':
                    # 这里注册的是原始的 unbound 方法
                    lst[1] = func
            cls.registration_script_job_list.append(
                CustomJob(decorator_kwargs, func_name=func.__name__, custom_params=custom_params)
            )

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def __del__(self):
        """
        清除注册的脚本任务
        :return:
        """
        self.kill_jobs()
        self.registration_script_job_list.clear()
