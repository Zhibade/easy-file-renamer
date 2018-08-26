"""
Test cases for utils module
"""

import io
import os
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


class TestGetNewFileName(TestCase):
    """Test cases for get_new_file_name utility"""

    FILENAME = "SomeFile_Extra.txt"

    def setUpClass():
        print("\nTesting utils -> get_new_file_name()\n")


    def test_rename(self):
        """get_new_file_name should replace old_name with new_name"""

        old_name = "SomeFile"
        new_name = "neWNamE"

        final_name = utils.get_new_file_name(self.FILENAME, old_name, new_name)

        no_ext = os.path.splitext(self.FILENAME)
        replaced_name = no_ext[0].replace(old_name, new_name)
        expected_name = "{0}{1}".format(replaced_name, no_ext[1])

        self.assertEqual(expected_name, final_name)


    def test_rename_ext(self):
        """get_new_file_name should not replace extension part of the filename"""

        old_name = ".txt"
        new_name = ".png"

        final_name = utils.get_new_file_name(self.FILENAME, old_name, new_name)

        self.assertEqual(self.FILENAME, final_name)


    def test_no_match(self):
        """get_new_file_name should not replace old_name with new_name if there is no match"""

        old_name = "WhatName"
        new_name = "neWNamE"

        final_name = utils.get_new_file_name(self.FILENAME, old_name, new_name)

        self.assertEqual(self.FILENAME, final_name)
