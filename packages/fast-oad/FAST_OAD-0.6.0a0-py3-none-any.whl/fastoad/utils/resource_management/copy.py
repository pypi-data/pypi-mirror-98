"""
Helper module for copying resources
"""
#  This file is part of FAST-OAD : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2020  ONERA & ISAE-SUPAERO
#  FAST is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os.path as pth
import shutil
from importlib.resources import Package, contents, is_resource
from importlib.resources import path
from types import ModuleType
from typing import List

from fastoad.utils.files import make_parent_dir


def copy_resource(package: Package, resource: str, target_path):
    """
    Copies the indicated resource file to provided target path.

    If target_path matches an already existing folder, resource file will be copied in this folder
    with same name. Otherwise, target_path will be the used name of copied resource file

    :param package: package as in importlib.resources.read_binary()
    :param resource: resource as in importlib.resources.read_binary()
    :param target_path: file system path
    """
    make_parent_dir(target_path)

    if pth.isdir(target_path):
        target_path = pth.join(target_path, resource)

    with path(package, resource) as source_path:
        shutil.copy(source_path, target_path)


def copy_resource_folder(package: Package, destination_path: str, exclude: List[str] = None):
    """
    Copies the full content of provided package in destination folder.

    Names of files that should not be copied have to be listed in `exclude`.

    .. Warning ::

        As the resources in the folder are discovered by browsing
        through the folder, they are not explicitly listed in the Python code.
        Therefore, to have the install process run smoothly, these resources need
        to be listed in the MANIFEST.in file.

    :param package: name of resource package to copy
    :param destination_path: file system path of destination
    :param exclude: list of item names that should not be copied
    """
    exclusion_list = ["__pycache__"]
    if exclude:
        exclusion_list += exclude

    for resource_name in contents(package):
        if resource_name in exclusion_list:
            continue
        if is_resource(package, resource_name):
            destination_file_path = pth.join(destination_path, resource_name)
            copy_resource(package, resource_name, destination_file_path)
        else:
            # In case of subfolders that are only declared in MANIFEST.in,
            # getattr(package, "resource_name") will fail (is there another way?).
            # So we fall back to using package name as as string.
            if isinstance(package, ModuleType):
                package_name = package.__name__
            else:  # str
                package_name = package
            new_package_name = ".".join([package_name, resource_name])
            new_destination_path = pth.join(destination_path, resource_name)
            copy_resource_folder(new_package_name, new_destination_path, exclude=exclude)
