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
        self.assertEqual("test\same1\same.txt == test\same2\same.txt", value)


if __name__ == '__main__':
    unittest.main()
