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

if __name__ == '__main__':
    unittest.main()
