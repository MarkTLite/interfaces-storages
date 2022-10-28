import unittest, os, sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

from providers.file_system_provider import FileSystemProvider
from providers.s3_storage_provider import AwsS3Provider
from image_storage import ImageStorageCLI


class TestAllStorage(unittest.TestCase):
    """Since dependency change should not conflict the system, same here. This class' tests are applicable to all supported
    db types: aws_s3 or file system.
    No need for new test modules for if you wish to add another provider.
    Run tests when one dependency choice is given by cli argument to the image storage app"""
    store_name = None
    def getDatabaseService(self):
        """choose database service"""
        if self.store_name == "filesystem":
            self.provider = FileSystemProvider()
        elif self.store_name == "aws_s3":
            self.provider = AwsS3Provider()  

    def storage_service(self):
        self.getDatabaseService()
        self.instance = ImageStorageCLI(db_provider=self.provider)
        self.instance.setup_app()
        return self.instance      

    def test_0_cli_setup(self):
        self.instance = self.storage_service()
        expected = (True, "Connected Successfully")
        returned = self.instance.setup_app()
        self.assertEqual(returned, expected, f"Check {self.store_name} Connection Test")
    
    def test_1_upload(self):
        self.instance = self.storage_service()
        source = 'student.png'
        dest = f'/upload/{source}'     # the base path is chosen during connect
        expected = (True, 'File transferred')
        returned = self.instance.upload_image(source, dest)
        self.assertEqual(returned, expected, f"Check {self.store_name} Upload Test")
    
    def test_2_download(self):
        self.instance = self.storage_service()
        dest = 'studentdl.png'       # dl to show it downloaded
        source = f'/upload/student.png'     
        expected = (True, 'File transferred')
        returned = self.instance.download_image(source, dest)
        self.assertEqual(returned, expected, f"Check {self.store_name} Download Test")
    
    def test_3_get_secure_url(self):
        self.instance = self.storage_service()
        path = f'/upload/student.png'
        returned = self.instance.get_secure_url(path=path)
        self.assertIn(True, returned, f"Check {self.store_name} URL test")

    def test_4_delete(self):
        self.instance = self.storage_service()
        source = 'student copy.png'
        dest = f'/upload/{source}'
        self.instance.upload_image(source, dest)
        file = 'student copy.png'
        path = f'/upload/{file}'
        expected = (True, "File deleted")
        returned = self.instance.delete_image(path=path)
        self.assertEqual(returned, expected, f"Check {self.store_name} Delete Test")

    def test_5_copy_file(self):
        self.instance = self.storage_service()
        file = 'student.png'
        source = f'/upload/{file}'
        dest = f'/copy/{file}'
        expected = (True, 'File transferred')
        returned = self.instance.copy_file(source_uri=source, dest_url=dest)
        self.assertEqual(returned, expected, f"Check {self.store_name} Copy test")

    def test_6_list_files(self):
        self.instance = self.storage_service()
        dir = '/'
        returned = self.instance.list_images(directory=dir)
        self.assertIn(True, returned, f"Check {self.store_name} List files test")

    def test_7_file_exists(self):
        self.instance = self.storage_service()
        file_uri = '/upload/student.png'    # check for uploaded file
        expected = (True, 'File exists')
        returned = self.instance.check_if_file_exists(file_uri)
        self.assertEqual(returned, expected, f"Check {self.store_name} File exists test")

    def test_8_file_doesnot_exist(self):
        self.instance = self.storage_service()
        file_uri = '/upload/student2.png'
        expected = (False, 'Error')
        returned = self.instance.check_if_file_exists(file_uri)
        self.assertEqual(returned, expected, f"Check {self.store_name} File doesnot exist test")

    def test_10_create_directory(self):
        self.instance = self.storage_service()
        folder = '/createdir'
        expected = (True, 'Directory created')
        returned = self.instance.create_directory(folder)
        self.assertEqual(returned, expected, f"Check {self.store_name} Create dir test")
    
    def test_9_delete_directory(self):
        self.instance = self.storage_service()
        folder = '/createdir'
        expected = (True, 'Directory deleted')
        returned = self.instance.delete_directory(folder)
        self.assertEqual(returned, expected, f"Check {self.store_name} delete dir test")

    def test_11_shut_app(self):
        expected = (True, "Disconnected Successfully")
        self.instance = self.storage_service()
        returned = self.instance.shut_app()
        self.assertEqual(returned, expected, "Check CLI Shut test")
    
    def test_12_fail_upload(self):
        self.instance = self.storage_service()
        source = None
        dest = f'/upload/{source}'     # the base path is chosen during connect
        expected = (False, 'Error')
        returned = self.instance.upload_image(source, dest)
        self.assertEqual(returned, expected, f"Check {self.store_name} Upload fail Test")
    
    def test_13_fail_download(self):
        self.instance = self.storage_service()
        dest = None       # dl to show it downloaded
        source = f'/upload/student.png'     
        expected = (False, 'Error')
        returned = self.instance.download_image(source, dest)
        self.assertEqual(returned, expected, f"Check {self.store_name} Download failTest")
    
    def test_14_fail_get_secure_url(self):
        self.instance = self.storage_service()
        path = None
        returned = self.instance.get_secure_url(path=path)
        self.assertIn(False, returned, f"Check {self.store_name} URL fail test")

    def test_15_fail_delete(self):
        self.instance = self.storage_service()
        source = 'student copy.png'
        dest = f'/upload/{source}'
        self.instance.upload_image(source, dest)
        path = None
        expected = (False, 'Error')
        returned = self.instance.delete_image(path=path)
        self.assertEqual(returned, expected, f"Check {self.store_name} Delete fail Test")

    def test_16_fail_copy_file(self):
        self.instance = self.storage_service()
        file = 'student.png'
        source = None
        dest = f'/copy/{file}'
        expected = (False, 'Error')
        returned = self.instance.copy_file(source_uri=source, dest_url=dest)
        self.assertEqual(returned, expected, f"Check {self.store_name} Copy fail test")

    def test_17_fail_list_files(self):
        self.instance = self.storage_service()
        dir = None
        returned = self.instance.list_images(directory=dir)
        self.assertIn(False, returned, f"Check {self.store_name} List files fail test")

    def test_19_fail_create_directory(self):
        self.instance = self.storage_service()
        folder = None
        expected = (False, 'Error')
        returned = self.instance.create_directory(folder)
        self.assertEqual(returned, expected, f"Check {self.store_name} Create dir test")
    
    def test_18_fail_delete_directory(self):
        self.instance = self.storage_service()
        folder = None
        expected = (False, 'Error')
        returned = self.instance.delete_directory(folder)
        self.assertEqual(returned, expected, f"Check {self.store_name} delete dir test")


if __name__=='__main__':
    if len(sys.argv) > 1:
        TestAllStorage.store_name = sys.argv.pop()

    if (TestAllStorage.store_name == 'aws_s3'     
     or TestAllStorage.store_name == 'filesystem'):
        unittest.main()

    else:
        print('Provide an expected dependency argument. Choose 1 of the supported dbs:\n1. filesystem\n2. aws_s3')