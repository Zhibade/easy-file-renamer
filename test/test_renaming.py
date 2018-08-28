"""
Test cases for renaming module
"""

import os

from unittest import TestCase
from unittest.mock import patch, MagicMock

from app.lib import renaming


class TestFullRename(TestCase):
    """Test cases for full_rename function"""

    FILENAME = "TestFileNAME.txt"

    def setUpClass():
        print("\nTesting renaming -> full_rename()\n")


    def test_type(self):
        """full_rename should return a string"""

        with patch('app.lib.renaming.get_new_file_name', return_value="ReplacedName"):
            old_name = "FileNAME"
            new_name = "NewAwesomeName"

            final_name = renaming.full_rename(self.FILENAME, rename=True,
                                              old_name=old_name, new_name=new_name)

            self.assertIs(str, type(final_name))


class TestGetNewFileName(TestCase):
    """Test cases for get_new_file_name function"""

    FILENAME = "SomeFile_Extra.txt"
    FILENAME_SPLITEXT = ["SomeFile_Extra", ".txt"]

    def setUpClass():
        print("\nTesting utils -> get_new_file_name()\n")


    def test_rename(self):
        """get_new_file_name should replace old_name with new_name"""

        with patch('os.path.splitext', return_value=self.FILENAME_SPLITEXT):
            old_name = "SomeFile"
            new_name = "neWNamE"

            final_name = renaming.get_new_file_name(self.FILENAME, old_name, new_name)

            no_ext = os.path.splitext(self.FILENAME)
            replaced_name = no_ext[0].replace(old_name, new_name)
            expected_name = "{0}{1}".format(replaced_name, no_ext[1])

            self.assertEqual(expected_name, final_name)


    def test_rename_ext(self):
        """get_new_file_name should not replace extension part of the filename"""

        with patch('os.path.splitext', return_value=self.FILENAME_SPLITEXT):
            old_name = ".txt"
            new_name = ".png"

            final_name = renaming.get_new_file_name(self.FILENAME, old_name, new_name)

            self.assertEqual(self.FILENAME, final_name)


    def test_no_match(self):
        """get_new_file_name should not replace old_name with new_name if there is no match"""

        with patch('os.path.splitext', return_value=self.FILENAME_SPLITEXT):
            old_name = "WhatName"
            new_name = "neWNamE"

            final_name = renaming.get_new_file_name(self.FILENAME, old_name, new_name)

            self.assertEqual(self.FILENAME, final_name)


class TestGetFilenameWithPrefix(TestCase):
    """Test cases for get_file_name_with_prefix function"""

    PREFIX = "PRE_"
    FILENAME = "TestFileNAME.txt"

    def setUpClass():
        print("\nTesting renaming -> get_file_name_with_prefix()\n")


    def test_prefix(self):
        """get_file_name_with_prefix should return the provided filename with the prefix added"""

        value = renaming.get_file_name_with_prefix(self.FILENAME, self.PREFIX)
        expected = "{0}{1}".format(self.PREFIX, self.FILENAME)

        self.assertEqual(expected, value)


    def test_type(self):
        """get_file_name_with_prefix should return a string"""

        value = renaming.get_file_name_with_prefix(self.FILENAME, self.PREFIX)
        self.assertIs(str, type(value))


class TestGetFilenameWithSuffix(TestCase):
    """Test cases for get_file_name_with_suffix function"""

    SUFFIX = "_SUFF"
    FILENAME = "TestFileNAME.txt"
    FILENAME_SPLITEXT = ["TestFileNAME", ".txt"]

    def setUpClass():
        print("\nTesting renaming -> get_file_name_with_suffix()\n")


    def test_prefix(self):
        """get_file_name_with_suffix should return the provided filename with the suffix added"""

        with patch('os.path.splitext', return_value=self.FILENAME_SPLITEXT):
            value = renaming.get_file_name_with_suffix(self.FILENAME, self.SUFFIX)
            expected = "{0}{1}{2}".format(self.FILENAME_SPLITEXT[0], self.SUFFIX,
                                          self.FILENAME_SPLITEXT[1])

        self.assertEqual(expected, value)


    def test_type(self):
        """get_file_name_with_suffix should return a string"""

        with patch('os.path.splitext', return_value=self.FILENAME_SPLITEXT):
            value = renaming.get_file_name_with_suffix(self.FILENAME, self.SUFFIX)
            self.assertIs(str, type(value))


class TestGetPreviewFilename(TestCase):
    """Test cases for get_preview_file_name function"""

    PATH = "some/path"

    def setUpClass():
        print("\nTesting renaming -> get_preview_file_name()\n")


    @patch('os.path.normpath', MagicMock(return_value=PATH))
    @patch('os.path.exists', MagicMock(return_value=True))
    @patch('app.lib.renaming.get_random_filename_in_dir', MagicMock(return_value="RandomFile.png"))
    @patch('app.lib.renaming.full_rename', MagicMock(return_value="NewName.png"))
    def test_cached(self):
        """get_preview_file_name should return the same filename if get_new is False and it has been called once"""

        value_a = renaming.get_preview_file_name(self.PATH, rename=True, old_name="", new_name="")

        with patch('app.lib.renaming.get_random_filename_in_dir', return_value="RandomFileB.png"):
            value_b = renaming.get_preview_file_name(self.PATH, rename=True,
                                                     old_name="", new_name="")
            self.assertEqual(value_a, value_b)


    @patch('os.path.normpath', MagicMock(return_value=PATH))
    @patch('os.path.exists', MagicMock(return_value=False))
    @patch('app.lib.renaming.get_random_filename_in_dir', MagicMock(return_value="RandomFile.png"))
    @patch('app.lib.renaming.full_rename', MagicMock(return_value="NewName.png"))
    def test_invalid(self):
        """get_preview_file_name should return "Invalid directory" when path is invalid"""

        value = renaming.get_preview_file_name(self.PATH, rename=True, old_name="", new_name="")
        self.assertEqual("Invalid directory", value)


    @patch('os.path.normpath', MagicMock(return_value=PATH))
    @patch('os.path.exists', MagicMock(return_value=True))
    @patch('app.lib.renaming.get_random_filename_in_dir', MagicMock(return_value=None))
    @patch('app.lib.renaming.full_rename', MagicMock(return_value="NewName.png"))
    def test_no_files(self):
        """get_preview_file_name should return "No files found" when no files are present in the directory"""

        value = renaming.get_preview_file_name(self.PATH, rename=True, old_name="",
                                               new_name="", get_new=True)
        self.assertEqual("No files found", value)


    @patch('os.path.normpath', MagicMock(return_value=PATH))
    @patch('os.path.exists', MagicMock(return_value=True))
    @patch('app.lib.renaming.get_random_filename_in_dir', MagicMock(return_value="RandomFile.png"))
    @patch('app.lib.renaming.full_rename', MagicMock(return_value="NewName.png"))
    def test_type(self):
        """get_preview_file_name should return a string"""

        value = renaming.get_preview_file_name(self.PATH, rename=True, old_name="", new_name="")
        self.assertIs(str, type(value))


    @patch('os.path.normpath', MagicMock(return_value=PATH))
    @patch('os.path.exists', MagicMock(return_value=True))
    @patch('app.lib.renaming.get_random_filename_in_dir', MagicMock(return_value="RandomFile.png"))
    @patch('app.lib.renaming.full_rename', MagicMock(return_value="NewName.png"))
    def test_valid(self):
        """get_preview_file_name should return the new filename"""

        value = renaming.get_preview_file_name(self.PATH, rename=True, old_name="", new_name="")
        self.assertEqual("NewName.png", value)
            