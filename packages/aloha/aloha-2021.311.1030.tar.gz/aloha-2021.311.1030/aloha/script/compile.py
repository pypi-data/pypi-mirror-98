__all__ = ('build', 'main')

import glob
import os
import shutil
import time
from collections import defaultdict
from distutils.core import setup

from Cython.Build import cythonize


def _expand(patterns: list = None):
    files = []
    for pattern in patterns:
        for file in glob.glob(pattern):
            files.append(os.path.abspath(file))
    files = sorted(set(files))
    return files


def build(base: str = None, dist: str = 'build', exclude: list = None, keep: list = None, copy_others=True):
    path_base = base or os.path.abspath('.')
    path_build = os.path.join(path_base, dist)
    files_exclude = _expand(exclude or [])  # sorted(set(os.path.abspath(i) for i in files_exclude))
    files_keep = _expand(keep or [])  # sorted(set((os.path.abspath(i) for i in files_keep)))

    # decide which files to copy and which files to cythonize
    act_list = defaultdict(list)
    for dir_path, dir_names, file_names in os.walk(path_base):
        dir_name = dir_path.split(os.sep)[-1]  # name of the current directory

        if dir_path.startswith(path_build) or dir_path in files_exclude:
            continue  # skip: folder for build output, and excluded folders

        if dir_name.startswith('.') or (os.sep + '.' in dir_path):
            continue  # hidden folders and sub-folders

        for file in file_names:
            (name, extension), path = os.path.splitext(file), os.path.join(dir_path, file)

            if path in files_exclude or extension in ('.pyc', 'pyx') or name.startswith('.'):
                continue  # skip: excluded files, pyc/pyx files, and hidden files

            action = 'copy'
            if extension in ('.py',):
                if not name.startswith('__') and path not in files_keep:
                    action = 'cythonize'
            elif not copy_others:
                continue  # if not copying other files, skip the file

            dst = path.replace(path_base, path_build)

            act_list[action].append((path, dst))

    for (src, dst) in act_list.get('copy', ()) + act_list.get('cythonize', ()):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)

    target_cythonize = [dst for (src, dst) in act_list.get('cythonize', ())]

    n_parallel = os.cpu_count() or 8

    # python code -> c code
    cythonized = cythonize(target_cythonize, nthreads=n_parallel)

    # c code -> dynamic library file
    path_build_tmp = os.path.join(path_build, '.tmp')
    setup(ext_modules=cythonized, script_args=["build_ext", "-b", path_build, "-t", path_build_tmp, "-j", n_parallel])

    # clean up
    for c_module in cythonized:
        for c_file in c_module.sources:
            os.remove(c_file)

    for py_file in target_cythonize:
        os.remove(py_file)

    shutil.rmtree(path_build_tmp)

    print("\n\nSuccessfully finished building package to: ", path_build)


def main(*args, **kwargs):
    t = time.time()
    build(*args, **kwargs)
    t = time.time() - t
    print('Time consumed to build code: %s seconds.' % t)
