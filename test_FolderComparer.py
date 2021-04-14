import os
import subprocess
import unittest

def call_command(command):
    return subprocess.check_output(command, shell=True).rstrip().decode("utf-8")

class TestFolderComparer(unittest.TestCase):

    def test_OnlyOneFile(self):
        value = call_command("python FolderComparer.py test\one\ test\one")
        self.assertEqual("test\\one\\one.txt == test\\one\\one.txt", value)

    def test_TheSameFileInTwoFolders(self):
        value = call_command("python FolderComparer.py test\same1\ test\same2")
        self.assertEqual("test\\same1\\same.txt == test\\same2\\same.txt", value)

    def test_ADifferentFileInTwoFolders(self):
        value = call_command("python FolderComparer.py test\different1\ test\different2")
        self.assertEqual("test\\different1\\different.txt (36) != test\\different2\\different.txt (39)", value)

    def test_OnlyInFolderOne(self):
        value = call_command("python FolderComparer.py test\only1_1\ test\only1_2")
        self.assertEqual("only in test\\only1_1\\one.txt (25)", value)

    def test_OnlyInFolderTwo(self):
        value = call_command("python FolderComparer.py test\only2_1\ test\only2_2")
        self.assertEqual("only in test\\only2_2\\two.txt (25)", value)

    def test_AdditionalEmptyFolder(self):
        if not os.path.exists("test\\additional_empty_folder\\additional"):
            os.makedirs("test\\additional_empty_folder\\additional")
        value = call_command("python FolderComparer.py test\same1\ test\\additional_empty_folder")
        self.assertEqual("test\\same1\\same.txt == test\\additional_empty_folder\\same.txt", value)

    def test_AdditionalEmptyFolder2(self):
        if not os.path.exists("test\\additional_empty_folder\\additional"):
            os.makedirs("test\\additional_empty_folder\\additional")
        value = call_command("python FolderComparer.py test\\additional_empty_folder\ test\same1")
        self.assertEqual("test\\additional_empty_folder\\same.txt == test\\same1\\same.txt", value)

    def test_AdditionalFolder(self):
        value = call_command("python FolderComparer.py test\same1\ test\\additional_folder")
        self.assertEqual("test\\same1\\same.txt == test\\additional_folder\\same.txt\r\nonly in test\\additional_folder\\additional\\one.txt (35)", value)

    def test_AdditionalFolder2(self):
        value = call_command("python FolderComparer.py test\\additional_folder\ test\same1")
        self.assertEqual("test\\additional_folder\\same.txt == test\\same1\\same.txt\r\nonly in test\\additional_folder\\additional\\one.txt (35)", value)

    def test_AdditionalFolderButIgnoreSame(self):
        value = call_command("python FolderComparer.py test\same1\ test\\additional_folder --ignore-same")
        self.assertEqual("only in test\\additional_folder\\additional\\one.txt (35)", value)

if __name__ == '__main__':
    unittest.main()
