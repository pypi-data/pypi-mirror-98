import tempfile

from unittest import TestCase
from Freya_alerce.core.commands.base_freya import Base

class TestCreateModuleLocal(TestCase):
    

    def setUp(self):
        self.tmp_test = tempfile.TemporaryDirectory()

    def test(self):
        Base(name='test_api',source='api',path=self.tmp_test.name).create_module_catalog_local()
        Base(name='test_db',source='db',path=self.tmp_test.name).create_module_catalog_local()
        # Base(name='test_db',source='other',path=self.tmp_test.name).create_module_catalog_local()

    def tearDown(self):
        self.tmp_test.cleanup()

if __name__ == '__main__':
    unittest.main() 