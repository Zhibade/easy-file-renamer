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


class TestGetFilenameWithNewExt(TestCase):
    """Test cases for get_file_name_with_new_ext function"""

    NEW_EXT = "cs"
    FILENAME = "TestFileNAME.txt"
    FILENAME_SPLITEXT = ["TestFileNAME", ".txt"]

    def setUpClass():
        print("\nTesting renaming -> get_file_name_with_new_ext()\n")


    def test_ext(self):
        """get_file_name_with_new_ext should return the provided filename with the new extension"""

        with patch('os.path.splitext', return_value=self.FILENAME_SPLITEXT):
            value = renaming.get_file_name_with_new_ext(self.FILENAME, self.NEW_EXT)
            expected = "{0}.{1}".format(self.FILENAME_SPLITEXT[0], self.NEW_EXT)

            self.assertEqual(expected, value)


    def test_no_dot(self):
        """get_file_name_with_new_ext should remove any dots from the extension"""

        dot_ext = ".cs"

        with patch('os.path.splitext', return_value=self.FILENAME_SPLITEXT):
            value = renaming.get_file_name_with_new_ext(self.FILENAME, dot_ext)
            expected = "{0}{1}".format(self.FILENAME_SPLITEXT[0], dot_ext)

            self.assertEqual(value, expected)


    def test_type(self):
        """get_file_name_with_new_ext should return a string"""

        with patch('os.path.splitext', return_value=self.FILENAME_SPLITEXT):
            value = renaming.get_file_name_with_new_ext(self.FILENAME, self.NEW_EXT)
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


class TestRenameNonRecursive(TestCase):
    """Test cases for rename_non_recursive function"""

    PATH = "norm//path"
    FILES = ["file1.png", "file2.png"]
    JOIN_PATH = "{0}{1}".format(PATH, FILES[0])
    NEW_NAME = "newFile1.png"

    def setUpClass():
        print("\nTesting renaming -> rename_non_recursive()\n")


    @patch('os.path.normpath', MagicMock(return_value=PATH))
    @patch('os.listdir', MagicMock(return_value=FILES))
    @patch('os.path.join', MagicMock(return_value=JOIN_PATH))
    @patch('os.path.isfile', MagicMock(return_value=True))
    @patch('os.rename')
    @patch('logging.info')
    def test_args(self, mock_a, mock_b):
        """rename_non_recursive should pass all of its keyword arguments to [full_rename] function"""

        path = self.PATH
        add_prefix = True
        prefix = "PRE_"
        add_suffix = True
        suffix = "_SUFF"
        change_ext = True
        new_ext = "abc"
        rename = True
        old_name = "Old"
        new_name = "New"

        with patch('app.lib.renaming.full_rename', return_value=self.NEW_NAME) as mock_full_rename:
            renaming.rename_non_recursive(path, add_prefix=add_prefix, prefix=prefix,
                                          add_suffix=add_suffix, suffix=suffix,
                                          change_ext=change_ext, new_ext=new_ext,
                                          rename=rename, old_name=old_name, new_name=new_name)

            self.assertTrue(mock_full_rename.called)
            mock_full_rename.assert_called_with(self.FILES[1], add_prefix=add_prefix, prefix=prefix,
                                                add_suffix=add_suffix, suffix=suffix,
                                                change_ext=change_ext, new_ext=new_ext,
                                                rename=rename, old_name=old_name, new_name=new_name)


    @patch('os.path.normpath', MagicMock(return_value=PATH))
    @patch('os.path.join', MagicMock(return_value=JOIN_PATH))
    @patch('os.path.isfile', MagicMock(return_value=True))
    @patch('app.lib.renaming.full_rename', MagicMock(return_value=NEW_NAME))
    @patch('os.rename')
    @patch('logging.info')
    def test_no_subdir(self, mock_a, mock_b):
        """rename_non_recursive should not include subdirectories"""

        with patch('os.listdir', return_value=self.FILES) as mock_listdir:
            renaming.rename_non_recursive("")
            self.assertTrue(mock_listdir.called)


    @patch('os.path.normpath', MagicMock(return_value=PATH))
    @patch('os.listdir', MagicMock(return_value=FILES))
    @patch('os.path.join', MagicMock(return_value=JOIN_PATH))
    @patch('os.path.isfile', MagicMock(return_value=True))
    @patch('app.lib.renaming.full_rename', MagicMock(return_value=NEW_NAME))
    @patch('logging.info')
    def test_rename(self, mock_a):
        """rename_non_recursive should rename the all the files"""

        with patch('os.rename') as mock_rename:
            renaming.rename_non_recursive("")

            self.assertTrue(mock_rename.called)
            self.assertTrue(mock_rename.call_count, len(self.FILES))


class TestRenameRecursive(TestCase):
    """Test cases for rename_recursive function"""

    PATH = "norm//path"
    FILES = ["file1.png", "file2.png"]
    JOIN_PATH = "{0}{1}".format(PATH, FILES[0])
    NEW_NAME = "newFile1.png"
    WALK_DIR_TREE = [("path", "dir", "file"), ("path2", "dir2", "file2")]

    def setUpClass():
        print("\nTesting renaming -> rename_recursive()\n")


    @patch('os.path.normpath', MagicMock(return_value=PATH))
    @patch('os.walk', MagicMock(return_value=WALK_DIR_TREE))
    @patch('os.path.join', MagicMock(return_value=JOIN_PATH))
    @patch('os.path.dirname', MagicMock(return_value=PATH))
    @patch('os.path.basename', MagicMock(return_value=FILES[0]))
    @patch('os.rename')
    @patch('logging.info')
    def test_args(self, mock_a, mock_b):
        """rename_recursive should pass all of its keyword arguments to [full_rename] function"""

        path = self.PATH
        add_prefix = True
        prefix = "PRE_"
        add_suffix = True
        suffix = "_SUFF"
        change_ext = True
        new_ext = "abc"
        rename = True
        old_name = "Old"
        new_name = "New"

        with patch('app.lib.renaming.full_rename', return_value=self.NEW_NAME) as mock_full_rename:
            renaming.rename_recursive(path, add_prefix=add_prefix, prefix=prefix,
                                      add_suffix=add_suffix, suffix=suffix,
                                      change_ext=change_ext, new_ext=new_ext,
                                      rename=rename, old_name=old_name, new_name=new_name)

            self.assertTrue(mock_full_rename.called)
            mock_full_rename.assert_called_with(self.FILES[0], add_prefix=add_prefix, prefix=prefix,
                                                add_suffix=add_suffix, suffix=suffix,
                                                change_ext=change_ext, new_ext=new_ext,
                                                rename=rename, old_name=old_name, new_name=new_name)


    @patch('os.path.normpath', MagicMock(return_value=PATH))
    @patch('os.path.join', MagicMock(return_value=JOIN_PATH))
    @patch('os.path.dirname', MagicMock(return_value=PATH))
    @patch('os.path.basename', MagicMock(return_value=FILES[0]))
    @patch('app.lib.renaming.full_rename', MagicMock(return_value=NEW_NAME))
    @patch('os.rename')
    @patch('logging.info')
    def test_no_subdir(self, mock_a, mock_b):
        """rename_recursive should include subdirectories"""

        with patch('os.walk', return_value=self.WALK_DIR_TREE) as mock_walk:
            renaming.rename_recursive("")
            self.assertTrue(mock_walk.called)


    @patch('os.path.normpath', MagicMock(return_value=PATH))
    @patch('os.walk', MagicMock(return_value=WALK_DIR_TREE))
    @patch('os.path.join', MagicMock(return_value=JOIN_PATH))
    @patch('os.path.dirname', MagicMock(return_value=PATH))
    @patch('os.path.basename', MagicMock(return_value=FILES[0]))
    @patch('app.lib.renaming.full_rename', MagicMock(return_value=NEW_NAME))
    @patch('logging.info')
    def test_rename(self, mock_a):
        """rename_recursive should rename the all the files"""

        with patch('os.rename', return_value=self.FILES) as mock_rename:
            renaming.rename_recursive("")

            self.assertTrue(mock_rename.called)
            self.assertTrue(mock_rename.call_count, len(self.WALK_DIR_TREE))
