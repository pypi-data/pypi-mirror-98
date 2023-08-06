import unittest
from winregmgr.winreg_manager import OpenKey
import winreg

KEY = winreg.HKEY_CURRENT_USER
SUB_KEY = r"SOFTWARE\\"
PARAMETER = "Test_parameter"
VALUE = "Test Value"


class TestReadWriteDelete(unittest.TestCase):
    def test1_create(self):
        with OpenKey(KEY, SUB_KEY) as reg_key:
            reg_key.set_value(PARAMETER, VALUE)
        self.assertEqual(True, True)

    def test2_read(self):
        with OpenKey(KEY, SUB_KEY) as reg_key:
            value, reg_type = reg_key.get_value_regtype(PARAMETER)
            self.assertEqual(value, VALUE)
            self.assertEqual(reg_type, 1)

    def test3_read_value(self):
        with OpenKey(KEY, SUB_KEY) as reg_key:
            value = reg_key.get_value(PARAMETER)
            self.assertEqual(value, VALUE)

    def test4_read_values(self):
        with OpenKey(KEY, SUB_KEY) as reg_key:
            values = reg_key.get_values()
            self.assertEqual(values[PARAMETER], VALUE)

    def test5_delete(self):
        with OpenKey(KEY, SUB_KEY) as reg_key:
            reg_key.delete_value(PARAMETER)

        try:
            with OpenKey(KEY, SUB_KEY) as reg_key:
                _, _ = reg_key.get_value(PARAMETER)
        except FileNotFoundError:
            self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
