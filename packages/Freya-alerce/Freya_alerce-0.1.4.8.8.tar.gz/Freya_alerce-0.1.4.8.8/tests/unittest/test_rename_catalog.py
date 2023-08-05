import tempfile

from unittest import TestCase
from Freya_alerce.core.commands.base_freya import Base
from Freya_alerce.files.list_file import ListFiles

class TestRenameCatalog(TestCase):

    def setUp(self):
        self.tmp_test = tempfile.TemporaryDirectory()

    def test(self):
        new_catalog = Base(name='test',source='api',path=self.tmp_test.name).create_module_catalog()
        Base(name='test',new_name='test2',path=self.tmp_test.name).rename_catalog()

        new_catalog = Base(name='test3',source='db',path=self.tmp_test.name).create_module_catalog()
        Base(name='test3',new_name='test4',path=self.tmp_test.name).rename_catalog()
    def tearDown(self):
        self.tmp_test.cleanup()

if __name__ == '__main__':
    unittest.main() 