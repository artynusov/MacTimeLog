import sys
import os
import shutil

from modulegraph.find_modules import find_modules, parse_mf_results
from modulegraph.modulegraph import SourceModule
from py2app.converters.nibfile import convert_xib

from setup import DATA_FILES, APP, OPTIONS


PYTHON_VER = sys.version[:3]
DEBUG = ARGUMENTS.get('debug', 0)

WORKING_DIR = Dir('.').abspath
BUILD_PATH = '/tmp/MacTimeLog/bulid'
APP_BUNDLE_PATH = 'dist/MacTimeLog.app'
PACKAGE_BASE_PATH = '{0}/Contents/'.format(APP_BUNDLE_PATH)
RESOURCES_PATH = PACKAGE_BASE_PATH + 'Resources/'
MACOS_PATH = PACKAGE_BASE_PATH + 'MacOS/'
LOCAL_SETTINGS_PATH = 'local_settings.py'
PYTHON_PATH = '{0}lib/python{1}/'.format(RESOURCES_PATH, PYTHON_VER)
SOURCES_ZIP_PATH = '{0}site-packages.zip'.format(PYTHON_PATH)


def convert_xib_action(source, target, env):
    convert_xib(str(source[0]), str(target[0]))


def cp_action(source, target, env):
    source_path = str(source[0])
    target_path = str(target[0])
    if os.path.isdir(source_path):
        shutil.copytree(source_path, target_path)
    else:
        shutil.copyfile(source_path, target_path)


def create_debug_settings_action(source, target, env):
    target_path = str(target[0])

    with open(target_path, 'w') as f:
        f.write('\n'.join([
            'import sys',
            'from common.settings_utils import initAppDirs',
            'initAppDirs(sys.modules[__name__], "MacTimeLogDev")'
        ]))


def is_site_pkg(path):
    """
    Retrun true if path is a site package or module and it's not
    listed in py2app options
    """
    return (path.find('/site-packages/') != -1 and
            all([path.find("/site-packages/{0}".format(p)) == -1
                    for p in OPTIONS['packages']]))


def py2app_builder(env):
    t = env.Command(MACOS_PATH + 'MacTimeLog', 'setup.py',
            'python setup.py py2app --b {0}'.format(BUILD_PATH))
    env.Clean(t, [APP_BUNDLE_PATH, BUILD_PATH])


def data_files_builder(env):
    for item in DATA_FILES:
        if os.path.isdir(item):
            for dirname, dirnames, filenames in os.walk(item):
                for name in filenames:
                    if not name.startswith('.') and not name.startswith('pyc'):
                        target_path = RESOURCES_PATH + dirname.replace(item,
                                os.path.basename(item)) + '/' + name

                        source_path = dirname + '/' + name

                        if name.endswith('.xib'):
                            action_funct = convert_xib_action
                            target_path = target_path[:-3] + 'nib'
                        else:
                            action_funct = cp_action

                        c = env.Command(target_path, source_path,
                                action=action_funct)
                        env.Precious(c)


def source_files_builder(env):
    env.Zip(SOURCES_ZIP_PATH, APP)

    for f in parse_mf_results(find_modules(APP))[0]:
        if "." not in f.identifier:
            if f.filename.startswith(WORKING_DIR):
                if isinstance(f, SourceModule):
                    file_name = os.path.split(f.filename)[1]
                    if file_name != LOCAL_SETTINGS_PATH:
                        env.Zip(SOURCES_ZIP_PATH, file_name)
                else:
                    env.Zip(SOURCES_ZIP_PATH, f.identifier)

            elif is_site_pkg(f.filename):
                if isinstance(f, SourceModule):
                    path = f.filename
                else:
                    path = os.path.split(f.filename)[0]
                name = os.path.split(path)[1]
                env.Command("{0}{1}".format(PYTHON_PATH, name), path,
                        action=cp_action)

    # debug settings
    if DEBUG:
        env.Command(LOCAL_SETTINGS_PATH, None,
                action=create_debug_settings_action)
        env.Zip(SOURCES_ZIP_PATH, LOCAL_SETTINGS_PATH)


# define SCONS variable, so setup.py will not build data files
shell_env = os.environ.copy()
shell_env['SCONS'] = '1'
env = Environment(ENV=shell_env)

py2app_builder(env)
data_files_builder(env)
source_files_builder(env)
