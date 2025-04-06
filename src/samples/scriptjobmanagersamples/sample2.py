from maya import cmds

from CustomMT import ScriptJobManagerBase


class SJM(ScriptJobManagerBase): pass


model_name = 'mySphere'
cmds.sphere(n=model_name)


@SJM.add_script_job_decorator(runOnce=True, attributeChange=['mySphere.ty', 'script'])
def warn1():
    height = cmds.getAttr(f'{model_name}.ty')
    if height > 5.0:
        print('Sphere is too high!')


@SJM.add_script_job_decorator(attributeChange=['mySphere.sx', 'script'])
def warn2():
    height = cmds.getAttr(f'{model_name}.sx')
    if height > 1.0:
        print('Sphere is too big!')


SJM.run_jobs()
SJM.kill_jobs()
