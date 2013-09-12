import sys
import os
import shutil

from modulegraph.find_modules import find_modules, parse_mf_results
from modulegraph.modulegraph import SourceModule
from py2app.converters.nibfile import convert_xib

from setup import DATA_FILES, APP


WORKING_DIR = Dir('.').abspath
PACKAGE_BASE_PATH = 'dist/MacTimeLog.app/Contents/'
RESOURCES_PATH = PACKAGE_BASE_PATH + 'Resources/'
MACOS_PATH = PACKAGE_BASE_PATH + 'MacOS/'

# define SCONS variable, so setup.py will not build data files
shell_env = os.environ.copy()
shell_env["SCONS"] = "1"
env = Environment(ENV=shell_env)


def convert_xib_action(source, target, env):
    convert_xib(str(source[0]), str(target[0]))


def cp_action(source, target, env):
    source_path = str(source[0])
    target_path = str(target[0])
    shutil.copyfile(source_path, target_path)

# py2app builder
env.Command(MACOS_PATH + 'MacTimeLog', 'setup.py',
        'python setup.py py2app --b /tmp/MacTimeLog/bulid')


# data files builder
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

# sources builder
sources = APP + []
for f in parse_mf_results(find_modules(APP))[0]:
    if f.filename.startswith(WORKING_DIR):
            if "." not in f.identifier:
                if isinstance(f, SourceModule):
                    file_name = os.path.split(f.filename)[1]
                    sources.append(file_name)
                else:
                    sources.append(f.identifier)
c = env.Zip(RESOURCES_PATH + "lib/python{0}/site-packages.zip".format(
        sys.version[:3]), sources)
env.Precious(c)
