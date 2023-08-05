import tempfile

from unittest import TestCase
from Freya_alerce.core.commands.base_freya import Base

class TestCreateModule(TestCase):
    
    def setUp(self):
        self.tmp_test = tempfile.TemporaryDirectory()

    def test(self):
        Base(name='test_api',source='api',path=self.tmp_test.name).create_module_catalog()
        Base(name='test_db',source='db',path=self.tmp_test.name).create_module_catalog()
        #Base(name='test_db',source='other',path=self.tmp_test.name).create_module_catalog()

    def tearDown(self):
        self.tmp_test.cleanup()

if __name__ == '__main__':
    unittest.main() 