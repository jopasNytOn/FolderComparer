#!/usr/bin/env python

import os
import sys

ignore_same = False
if len(sys.argv) != 3:
    if len(sys.argv) == 4 and sys.argv[3] == "--ignore-same":
        ignore_same = True
    else:
        sys.exit('Version 0.05, Usage: python3 FolderComparer.py <folder1> <folder2> [--ignore-same] \n\n' \
                 '              e.g.   FolderComparer.py   C:\\folder_A  C:\\folder_B                 (in Cmd) \n'
                 '                     ./FolderComparer.py /c/folder_A/ /c/folder_B/ --ignore-same  (in Mingw64)')


class File():
    def __init__(self, whole_name, size):
        self.whole_name = whole_name
        self.size = size


class Folder():
    def __init__(self, path):
        self.path = path + '\\' if path[-1] != '\\' else path
        self.files = {}
        for r, d, f in os.walk(self.path):
            for file in f:
                self.add_file(r + '\\' if r[-1] != '\\' else r, file)

    def add_file(self, path, filename):
        self.files[filename] = File(path + filename, os.stat(path + filename).st_size)


class FolderComparer():
    def __init__(self, folder1, folder2):
        self.folder1 = folder1
        self.folder2 = folder2

    def are_files_equal(self, file1, file2):
        return file1.size == file2.size

    def print(self):
        for file in self.folder1.files:
            file1 = self.folder1.files[file]
            try:
                file2 = self.folder2.files[file]
            except KeyError:
                print('only in {} ({})'.format(file1.whole_name, file1.size))
                continue
            if self.are_files_equal(file1, file2):
                if ignore_same == False:
                    print('{} == {}'.format(file1.whole_name, file2.whole_name))
            else:
                print('{} ({}) != {} ({})'.format(file1.whole_name, file1.size, file2.whole_name, file2.size))
        for file in self.folder2.files:
            file2 = self.folder2.files[file]
            try:
                file1 = self.folder1.files[file]
            except KeyError:
                print('only in {} ({})'.format(file2.whole_name, file2.size))
                continue


folder1 = Folder(sys.argv[1].replace('\\\\', '\\'))
folder2 = Folder(sys.argv[2].replace('\\\\', '\\'))
compare = FolderComparer(folder1, folder2)
compare.print()
