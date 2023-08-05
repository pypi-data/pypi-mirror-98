import tempfile

from unittest import TestCase
from Freya_alerce.core.commands.base_api import BaseAPI


class TestCreateApi(TestCase):
    
    def setUp(self):
        self.temp_FreyaApi = tempfile.TemporaryDirectory()

    def test(self):
        BaseAPI(path=self.temp_FreyaApi.name).create_new_api()

    def tearDown(self):
        self.temp_FreyaApi.cleanup()

if __name__ == '__main__':
    unittest.main() 