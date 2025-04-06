import dataclasses

from CustomMT.job_manager import ScriptJobManagerBase


@dataclasses.dataclass
class CustomJobParameter:
    _group_name: str = 'test'


class ToolManager1(ScriptJobManagerBase):

    @classmethod
    def run_jobs(cls):

        """
        运行所有注册的脚本任务
        :return:
        """
        for i in cls.registration_script_job_list:
            if i.custom_params.get('_group_name') == 'test':
                i.run_job()


class ToolManager2(ScriptJobManagerBase):
    pass


@ToolManager1.add_script_job_decorator(event=['NewSceneOpened', 'script'])
@ToolManager1.add_script_job_decorator(event=['SelectionChanged', 'script'], runOnce=True)
@ToolManager1.add_script_job_decorator(event=['SelectionChanged', 'script'], _group_name='test')
def f1():
    print('*' * 3, 'f1,event,SelectionChanged')


# @ToolManager2.add_script_job_decorator(event=['NewSceneOpened', 'script'])
def f2():
    print('*' * 3, 'f2,event,NewSceneOpened')


# ToolManager1.registration_script_job_list.clear()
# ToolManager2.registration_script_job_list.clear()

# TM.registration_script_job_list.clear()
print(ToolManager1.registration_script_job_list)
print(ToolManager2.registration_script_job_list)

ToolManager1.run_jobs()
ToolManager2.run_jobs()
#
# ToolManager1.kill_jobs()
# ToolManager2.kill_jobs()

# for i in ToolManager1.registration_script_job_list:
#     print(i.nice_name)
#
# for i in ToolManager1.registration_script_job_list:
#     print(i.job_id)
#
# ToolManager1.kill_jobs()
# for i in ToolManager1.registration_script_job_list:
#     print(i.job_id)

for i in ToolManager1.registration_script_job_list:
    print(i.custom_params.get('_group_name'))
    print(i.get_nice_name())
    print(i.is_job_running())
