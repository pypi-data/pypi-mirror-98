import tempfile

from unittest import TestCase
from Freya_alerce.core.commands.base_freya import Base

class TestDeleteCatalog(TestCase):

    def setUp(self):
        self.tmp_test = tempfile.TemporaryDirectory()

    def test(self):
        new_catalog = Base(name='test',source='api',path=self.tmp_test.name).create_module_catalog()
        Base(name='test',path=self.tmp_test.name).delete_catalog()

        new_catalog = Base(name='test3',source='db',path=self.tmp_test.name).create_module_catalog()
        Base(name='test3',path=self.tmp_test.name).delete_catalog()


    def tearDown(self):
        self.tmp_test.cleanup()

if __name__ == '__main__':
    unittest.main() 