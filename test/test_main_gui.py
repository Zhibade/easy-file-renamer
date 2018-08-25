"""
Test cases for main_gui module
"""

import sys
from unittest import TestCase
from unittest.mock import patch

from PySide2.QtWidgets import QApplication
from PySide2.QtTest import QTest
from PySide2.QtCore import Qt

from app.ui.main_gui import GUI


QApplication(sys.argv)


class TestAddPrefixCheckbox(TestCase):
    """Test cases for Add Prefix checkbox widget"""

    def setUpClass():
        print("\nTesting main_gui -> Add Prefix checkbox\n")


    def test_true(self):
        """Add prefix line edit should be enabled when prefix_chk is checked"""

        with patch('PySide2.QtCore.QSettings'):
            gui = GUI()
            gui.prefix_chk.setChecked(False)
            gui.prefix_line_edit.setEnabled(False)

            QTest.mouseClick(gui.prefix_chk, Qt.LeftButton)
            self.assertEqual(True, gui.prefix_line_edit.isEnabled())


    def test_false(self):
        """Add prefix line edit should be disabled when prefix_chk is not checked"""

        with patch('PySide2.QtCore.QSettings'):
            gui = GUI()
            gui.prefix_chk.setChecked(True)
            gui.prefix_line_edit.setEnabled(True)

            QTest.mouseClick(gui.prefix_chk, Qt.LeftButton)
            self.assertEqual(False, gui.prefix_line_edit.isEnabled())


class TestAddSuffixCheckbox(TestCase):
    """Test cases for Add Suffix checkbox widget"""

    def setUpClass():
        print("\nTesting main_gui -> Add Suffix checkbox\n")


    def test_true(self):
        """Add suffix line edit should be enabled when suff_chk is checked"""

        with patch('PySide2.QtCore.QSettings'):
            gui = GUI()
            gui.suff_chk.setChecked(False)
            gui.suff_line_edit.setEnabled(False)

            QTest.mouseClick(gui.suff_chk, Qt.LeftButton)
            self.assertEqual(True, gui.suff_line_edit.isEnabled())


    def test_false(self):
        """Add suffix line edit should be disabled when suff_chk is not checked"""

        with patch('PySide2.QtCore.QSettings'):
            gui = GUI()
            gui.suff_chk.setChecked(True)
            gui.suff_line_edit.setEnabled(True)

            QTest.mouseClick(gui.suff_chk, Qt.LeftButton)
            self.assertEqual(False, gui.suff_line_edit.isEnabled())


class TestChangeExtensionCheckbox(TestCase):
    """Test cases for Change Extension checkbox widget"""

    def setUpClass():
        print("\nTesting main_gui -> Change Extension checkbox\n")


    def test_true(self):
        """Change extension line edit should be enabled when ext_chk is checked"""

        with patch('PySide2.QtCore.QSettings'):
            gui = GUI()
            gui.ext_chk.setChecked(False)
            gui.ext_line_edit.setEnabled(False)

            QTest.mouseClick(gui.ext_chk, Qt.LeftButton)
            self.assertEqual(True, gui.ext_line_edit.isEnabled())


    def test_false(self):
        """Change extension line edit should be disabled when ext_chk is not checked"""

        with patch('PySide2.QtCore.QSettings'):
            gui = GUI()
            gui.ext_chk.setChecked(True)
            gui.ext_line_edit.setEnabled(True)

            QTest.mouseClick(gui.ext_chk, Qt.LeftButton)
            self.assertEqual(False, gui.ext_line_edit.isEnabled())


class TestRenameCheckbox(TestCase):
    """Test cases for Rename checkbox widget"""

    def setUpClass():
        print("\nTesting main_gui -> Rename checkbox\n")


    def test_true(self):
        """Old name and new name line edits should be enabled when rename_chk is checked"""

        with patch('PySide2.QtCore.QSettings'):
            gui = GUI()
            gui.rename_chk.setChecked(False)
            gui.rename_old_line_edit.setEnabled(False)
            gui.rename_new_line_edit.setEnabled(False)

            QTest.mouseClick(gui.rename_chk, Qt.LeftButton)
            self.assertEqual(True, gui.rename_old_line_edit.isEnabled())
            self.assertEqual(True, gui.rename_new_line_edit.isEnabled())


    def test_false(self):
        """Old name and new name line edits should be disabled when rename_chk is not checked"""

        with patch('PySide2.QtCore.QSettings'):
            gui = GUI()
            gui.rename_chk.setChecked(True)
            gui.rename_old_line_edit.setEnabled(True)
            gui.rename_new_line_edit.setEnabled(True)

            QTest.mouseClick(gui.rename_chk, Qt.LeftButton)
            self.assertEqual(False, gui.rename_old_line_edit.isEnabled())
            self.assertEqual(False, gui.rename_new_line_edit.isEnabled())
