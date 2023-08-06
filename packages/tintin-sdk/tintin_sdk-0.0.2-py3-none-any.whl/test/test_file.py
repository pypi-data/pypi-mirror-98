import os
import unittest
from unittest import mock

from tintin.file import FileManager 

class TestFileDownload(unittest.TestCase):
    debug = False
    host = 'https://api.tintin.footprint-ai.com'
    m = mock.patch.dict(os.environ, { 'TINTIN_SESSION_TEMPLATE_PROJECT_ID': '427wr4e8lno9gjgzmd6kp03vxyz51w',
    'TINTIN_SESSION_TEMPLATE_PROJECT_TOKEN_MINIO_DOWNLOAD': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIqLmZvb3RwcmludC1haS5jb20iLCJleHAiOjIyNDY2OTM0NDUsImp0aSI6ImEyZWM0YmUwLTA0NDYtNDc1Mi05ZjRmLWQ2YTg5NDM4MmM0YiIsImlhdCI6MTYxNTk3MzQ0NSwiaXNzIjoiYXV0aG9yaXphdGlvbi5mb290cHJpbnQtYWkuY29tIiwibmJmIjoxNjE1OTczNDQ1fQ.lCd3QwELdGXUhocQ3vhC1604RXdjOTJ2dRb9FHHQbAxAR-uTXECmVwRRbrRIGJV0p17t8gQ-5RnPMSh1Hj8ldQ',
        })
    def test_http_file_download(self):
        self.m.start()
        mgr = FileManager(self.host, self.debug)
        self.assertEqual(mgr.download('/tmp',
            ['https://api.tintin.footprint-ai.com/api/v1/project/427wr4e8lno9gjgzmd6kp03vxyz51w/minio/object/testdata/1.jpg'],
        ), True)
        self.m.stop()

    def test_localpath_file_download(self):
        self.m.start()
        mgr = FileManager(self.host, self.debug)
        self.assertEqual(mgr.download('/tmp',
            ['/testdata/1.jpg'],
        ), True)
        self.m.stop()

    def test_localpath_download_notfound(self):
        self.m.start()
        mgr = FileManager(self.host, self.debug)
        self.assertEqual(mgr.download('/tmp',
            ['/testdata/notfound.jpg'],
        ), False)
        self.m.stop()

    def test_localpath_dir_download(self):
        self.m.start()
        mgr = FileManager(self.host, self.debug)
        self.assertEqual(mgr.download('/tmp',
            ['/testdata'],
            self.debug,
        ), True)
        self.m.stop()

    def test_file_upload(self):
        self.m.start()
        mgr = FileManager(self.host, self.debug)
        self.assertEqual(mgr.upload('/testupload', './testdata'), True)
        self.m.stop()

if __name__ == '__main__':
    unittest.main()
