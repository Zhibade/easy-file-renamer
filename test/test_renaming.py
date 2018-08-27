"""
Test cases for renaming module
"""

import os

from unittest import TestCase
from unittest.mock import patch

from app.lib import renaming


class TestFullRename(TestCase):
    """Test cases for full_rename utility"""

    FILENAME = "TestFileNAME.txt"

    def setUpClass():
        print("\nTesting renaming -> full_rename()\n")


    def test_rename(self):
        """full_rename should return a string"""

        with patch('app.lib.renaming.get_new_file_name', return_value="ReplacedName"):
            old_name = "FileNAME"
            new_name = "NewAwesomeName"

            final_name = renaming.full_rename(self.FILENAME, rename=True,
                                              old_name=old_name, new_name=new_name)

            self.assertIs(type("string"), type(final_name))



class TestGetNewFileName(TestCase):
    """Test cases for get_new_file_name utility"""

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
