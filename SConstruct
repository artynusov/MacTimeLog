import os
import shutil

from py2app.converters.nibfile import convert_xib

from setup import DATA_FILES


BASE_PATH = 'dist/MacTimeLog.app/Contents/'
RESOURCES_PATH = BASE_PATH + 'Resources/'
MACOS_PATH = BASE_PATH + 'MacOS/'

shell_env = os.environ.copy()
shell_env["SCONS"] = "1"
env = Environment(ENV=shell_env)


def convert_xib_action(source, target, env):
    convert_xib(str(source[0]), str(target[0]))


def cp_action(source, target, env):
    source_path = str(source[0])
    target_path = str(target[0])
    shutil.copyfile(source_path, target_path)


py2appc = env.Command(MACOS_PATH + 'MacTimeLog', 'setup.py',
        'python setup.py py2app --b /tmp/MacTimeLog/bulid')


for item in DATA_FILES:
    if os.path.isdir(item):
        for dirname, dirnames, filenames in os.walk(item):
            for name in filenames:
                if not name.startswith('.') and not name.startswith("pyc"):
                    target_path = RESOURCES_PATH + dirname.replace(item,
                            os.path.basename(item)) + '/' + name

                    source_path = dirname + '/' + name

                    if name.endswith(".xib"):
                        action_funct = convert_xib_action
                        target_path = target_path[:-3] + "nib"
                    else:
                        action_funct = cp_action

                    c = env.Command(target_path, source_path,
                            action=action_funct)
                    env.Precious(c)
    else:
        c = env.Command(RESOURCES_PATH + os.path.basename(item),
                    item, action=cp_action)
        env.Precious(c)
