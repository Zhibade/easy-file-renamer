"""
Test cases for renaming module
"""

from unittest import TestCase

from app.lib import renaming


class TestFullRename(TestCase):
    """Test cases for full_rename utility"""

    FILENAME = "TestFileNAME.txt"

    def setUpClass():
        print("\nTesting renaming -> full_rename()\n")


    def test_rename(self):
        """full_rename should replace old_name with new_name on filename"""

        old_name = "FileNAME"
        new_name = "NewAwesomeName"

        final_name = renaming.full_rename(self.FILENAME, rename=True,
                                          old_name=old_name, new_name=new_name)
        expected_name = self.FILENAME.replace(old_name, new_name)

        self.assertEqual(expected_name, final_name)
