"""
Test cases for utils module
"""

import io
from unittest import TestCase
from unittest.mock import patch

from app import utils


class TestGetFileText(TestCase):

    FILE_PATH = "path/to/file.css"
    FILE_CONTENTS = "line1\nline2\n"

    def setUpClass():
        print("\nTesting utils -> get_file_text() tests\n")


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
