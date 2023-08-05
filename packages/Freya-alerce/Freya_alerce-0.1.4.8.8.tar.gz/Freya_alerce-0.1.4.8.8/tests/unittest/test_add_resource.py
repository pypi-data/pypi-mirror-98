import tempfile
import os

from unittest import TestCase,mock
from Freya_alerce.core.commands.base_api import BaseAPI
from Freya_alerce.files.list_file import ListFiles
from Freya_alerce.files.verify_file import Verify

class TestAddResource(TestCase):
    
    def setUp(self):
        self.temp_FreyaAPI = tempfile.TemporaryDirectory()

    def test(self):
        BaseAPI(path=self.temp_FreyaAPI.name).create_new_api()
        path_api = os.path.join(self.temp_FreyaAPI.name,'FreyaAPI')
        BaseAPI(name='ztf',path=path_api).create_new_resource()

    def tearDown(self):
        self.temp_FreyaAPI.cleanup()

if __name__ == '__main__':
    unittest.main() 