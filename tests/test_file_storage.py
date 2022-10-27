import unittest, sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

from providers.file_system_provider import FileSystemProvider
from providers.s3_storage_provider import AwsS3Provider
from image_storage import ImageStorageCLI


class TestFileStorage(unittest.TestCase):
    """Contains tests for when filesystem is the dependency"""  

    def storage_service(self):
        self.provider = FileSystemProvider()
        self.instance = ImageStorageCLI(db_provider=self.provider)
        self.instance.setup_app()
        return self.instance      

    def test_cli_file_setup(self):
        self.instance = self.storage_service()
        expected = (True, "Connected Successfully")
        returned = self.instance.setup_app()
        self.assertEqual(returned, expected, "Check File Connection Test")
    
    def test_file_upload(self):
        self.instance = self.storage_service()
        source = 'student.png'
        dest = f'/upload/{source}'     # the base path is chosen during connect
        expected = (True, 'File transferred') 
        returned = self.instance.upload_image(source, dest)
        self.assertEqual(returned, expected, "Check File Upload Test")
    
    def test_file_download(self):
        self.instance = self.storage_service()
        dest = 'student.png'
        source = f'/upload/{dest}'     # to download the uploaded pic into the base path
        expected = (True, 'File transferred')
        returned = self.instance.download_image(source, dest)
        self.assertEqual(returned, expected, "Check File Download Test")
    
    def test_file_get_secure_url(self):
        self.instance = self.storage_service()
        returned = self.instance.get_secure_url(path=path)
        self.assertIn(True, returned, "Check File URL test")

    def test_file_delete(self):
        self.instance = self.storage_service()
        source = 'student copy.png'
        dest = f'/upload/{source}'
        self.instance.upload_image(source, dest)
        file = 'student copy.png'
        path = f'/upload/{file}'
        expected = (True, "File deleted")
        returned = self.instance.delete_image(path=path)
        self.assertEqual(returned, expected, "Check File Delete Test")

    def test_file_copy_file(self):
        self.instance = self.storage_service()
        file = 'student.png'
        source = f'/upload/{file}'
        dest = f'/copy/{file}'
        expected = (True, 'File transferred')
        returned = self.instance.copy_file(source_uri=source, dest_url=dest)
        self.assertEqual(returned, expected, "Check File Copy test")

    def test_file_list_files(self):
        self.instance = self.storage_service()
        dir = '/'
        returned = self.instance.list_images(directory=dir)
        self.assertIn(True, returned, "Check List files test")

    def test_file_file_exists(self):
        self.instance = self.storage_service()
        file_uri = '/upload/student.png'    # check for uploaded file
        expected = (True, 'File exists')
        returned = self.instance.check_if_file_exists(file_uri)
        self.assertEqual(returned, expected, "Check File exists test")

    def test_file_file_doesnot_exist(self):
        self.instance = self.storage_service()
        file_uri = '/upload/student2.png'
        expected = (False, 'Error')
        returned = self.instance.check_if_file_exists(file_uri)
        self.assertEqual(returned, expected, "Check File doesnot exist test")

    def test_file_create_directory(self):
        self.instance = self.storage_service()
        folder = '/createdir'
        expected = (True, 'Directory created')
        returned = self.instance.create_directory(folder)
        self.assertEqual(returned, expected, "Check File Create dir test")
    
    def test_file_delete_directory(self):
        self.instance = self.storage_service()
        folder = '/createdir'
        expected = (True, 'Directory deleted')
        returned = self.instance.delete_directory(folder)
        self.assertEqual(returned, expected, "Check File delete dir test")

    def test_shut_app(self):
        expected = (True, "Disconnected Successfully")
        self.instance = self.storage_service()
        returned = self.instance.shut_app()
        self.assertEqual(returned, expected, "Check File CLI Shut test")
        

if __name__ == "__main__":
    unittest.main()