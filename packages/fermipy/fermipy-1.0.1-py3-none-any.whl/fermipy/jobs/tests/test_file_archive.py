# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function

import os

from fermipy.jobs.file_archive import FileStatus, FileHandle, FileArchive

def assert_str_eq(str1, str2):
    try:
        test_str = str2.decode()
    except AttributeError:
        test_str = str2
    assert test_str == str1


def test_file_handle():
    """ Test that we can build a `FileHandle` """

    file_handle = FileHandle(path="test",
                             key=0,
                             creator=0,
                             timestamp=0,
                             status=FileStatus.no_file)
    file_dict = {file_handle.key: file_handle}
    table = FileHandle.make_table(file_dict)
    file_dict2 = FileHandle.make_dict(table)
    file_handle2 = file_dict2[file_handle.key]

    assert_str_eq(file_handle.path, file_handle2.path)
    assert_str_eq(file_handle.key, file_handle2.key)
    assert_str_eq(file_handle.creator, file_handle2.creator)
    assert file_handle.timestamp == file_handle2.timestamp
    assert file_handle.status == file_handle2.status


def test_file_archive():
    """ Test that we can build a `FileArchive` """

    file_archive = FileArchive(file_archive_table='archive_files.fits',
                               base_path=os.path.abspath('.'))

    file_handle = file_archive.register_file(filepath='test',
                                             creator=0,
                                             status=FileStatus.no_file)
    file_handle2 = file_archive.update_file(filepath='test',
                                            creator=0,
                                            status=FileStatus.expected)
    assert file_handle.path == file_handle2.path
    assert file_handle.key == file_handle2.key


if __name__ == '__main__':
    test_file_handle()
    test_file_archive()
