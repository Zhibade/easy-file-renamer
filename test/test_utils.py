"""
Test cases for utils module
"""

import io

from unittest import TestCase
from unittest.mock import patch

from app import utils


class TestIniStrToBool(TestCase):
    """Test cases for ini_str_to_bool utility"""

    def setUpClass():
        print("\nTesting utils -> ini_str_to_bool()\n")


    def test_true(self):
        """ini_str_to_bool should return True if 'true' is passed"""

        value = utils.ini_str_to_bool("true")
        self.assertEqual(True, value)


    def test_false(self):
        """ini_str_to_bool should return False if 'false' is passed"""

        value = utils.ini_str_to_bool("false")
        self.assertEqual(False, value)


class TestGetFileText(TestCase):
    """Test cases for get_file_text utility"""

    FILE_PATH = "path/to/file.css"
    FILE_CONTENTS = "line1\nline2\n"

    def setUpClass():
        print("\nTesting utils -> get_file_text()\n")


    def setUp(self):
        self.file_contents = io.StringIO(self.FILE_CONTENTS)


    def test_arg(self):
        """get_file_text should open the file using the provided path"""

        with patch('builtins.open', return_value=self.file_contents) as open_mock:
            utils.get_file_text(self.FILE_PATH)
            open_mock.assert_called_with(self.FILE_PATH)


    def test_return(self):
        """get_file_text should return file contents as a single string"""

        with patch('builtins.open', return_value=self.file_contents):
            return_contents = utils.get_file_text(self.FILE_PATH)
            self.assertEqual(return_contents, self.FILE_CONTENTS.replace("\n", ""))


    def test_type(self):
        """get_file_text should return a string"""

        with patch('builtins.open', return_value=self.file_contents):
            return_contents = utils.get_file_text(self.FILE_PATH)
            self.assertIs(type(return_contents), str)


class TestGetRandomFilenameInDir(TestCase):
    """Test cases for get_random_filename_in_dir utility"""

    def setUpClass():
        print("\nTesting utils -> get_random_filename_in_dir()\n")


    def test_valid(self):
        """get_random_filename_in_dir should return a filename with extension if path is valid"""

        filename = "file.png"

        with patch('os.path.exists', return_value=True):
            with patch('os.walk', return_value=[("root", "dir", "file")]):
                with patch('os.listdir', return_value=[filename, filename]):
                    with patch('os.path.isfile', return_value=True):
                        value = utils.get_random_filename_in_dir("some/path")
                        self.assertEqual(filename, value)


    def test_invalid(self):
        """get_random_filename_in_dir should return an empty string if path is invalid"""

        with patch('os.path.exists', return_value=False):
            value = utils.get_random_filename_in_dir("some/path")
            self.assertEqual("", value)


    def test_no_subdir(self):
        """get_random_filename_in_dir should not include subdirectories if [include_subdir] is False"""

        folder = "folder"

        with patch('os.path.exists', return_value=True):
            with patch('os.walk', return_value=[("root", "dir", "file")]) as walk_mock:
                with patch('os.listdir', return_value=[folder, folder]):
                    with patch('os.path.isfile', return_value=True):
                        utils.get_random_filename_in_dir("some/path")
                        self.assertEqual(walk_mock.called, False)


    def test_subdir(self):
        """get_random_filename_in_dir should include subdirectories if [include_subdir] is True"""

        folder = "folder"

        with patch('os.path.exists', return_value=True):
            with patch('os.walk', return_value=[("root", "dir", "file")]) as walk_mock:
                with patch('os.listdir', return_value=[folder, folder]):
                    with patch('os.path.isfile', return_value=True):
                        utils.get_random_filename_in_dir("some/path", include_subdir=True)
                        self.assertEqual(walk_mock.called, True)
