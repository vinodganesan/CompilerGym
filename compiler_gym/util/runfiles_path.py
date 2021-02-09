# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Module for resolving a runfiles path."""
import os
from pathlib import Path

# NOTE(cummins): Moving this file may require updating this relative path.
_PACKAGE_ROOT = Path(os.path.join(os.path.dirname(__file__), "../../")).resolve(
    strict=True
)


def runfiles_path(relpath: str) -> Path:
    """Resolve the path to a runfiles data path.

    Use environment variable COMPILER_GYM_RUNFILES=/path/to/runfiles if running
    outside of bazel.
    """
    # There are three ways of determining a runfiles path:
    #   1. Set the COMPILER_GYM_RUNFILES environment variable.
    #   2. Using the rules_python library that is provided by bazel. This will
    #      fail if not being executed within a bazel sandbox.
    #   3. Computing the path relative to the location of this file. This is the
    #      fallback approach that is used for when the code has been installed
    #      by setuptools.
    runfiles_path = os.environ.get("COMPILER_GYM_RUNFILES")
    if runfiles_path:
        return Path(runfiles_path) / relpath
    else:
        try:
            from rules_python.python.runfiles import runfiles

            return Path(runfiles.Create().Rlocation(relpath))
        except (ModuleNotFoundError, TypeError):
            # Try to find the files relative to the current file, assuming that
            # they are all given as paths "CompilerGym/compiler_gym/foo/bar.txt"
            # and such.
            return _PACKAGE_ROOT / Path(*Path(relpath).parts[1:])


def site_data_path(relpath: str) -> Path:
    """Return a path within the site data directory.

    CompilerGym uses a directory to store persistent site data files in, such as benchmark datasets.
    The default location is :code:`~/.local/share/compiler_gym`. Set the environment variable
    :code:`$COMPILER_GYM_SITE_DATA` to override this default location.
    """
    # NOTE(cummins): This function has a matching implementation in the C++
    # sources, compiler_gym::service::getSiteDataPath(). Any change to behavior
    # here must be reflected in the C++ version.
    forced = os.environ.get("COMPILER_GYM_SITE_DATA")
    if forced:
        return Path(forced) / relpath
    elif os.environ.get("HOME"):
        return Path("~/.local/share/compiler_gym").expanduser() / relpath
    else:
        return Path("/tmp/compiler_gym/site_data") / relpath


def cache_path(relpath: str) -> Path:
    """Return a path within the cache directory.

    CompilerGym uses a directory to cache files in, such as downloaded content. The default location
    for this cache is :code:`~/.cache/compiler_gym`. Set the environment variable
    :code:`$COMPILER_GYM_CACHE` to override this default location.

    :param relpath: The relative path within the cache.
    :return: The absolute path of the cache.
    """
    forced = os.environ.get("COMPILER_GYM_CACHE")
    if forced:
        return Path(forced) / relpath
    elif os.environ.get("HOME"):
        return Path("~/.cache/compiler_gym").expanduser() / relpath
    else:
        return Path("/tmp/compiler_gym/cache") / relpath
