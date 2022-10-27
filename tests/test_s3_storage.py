import unittest, os, sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

from providers.file_system_provider import FileSystemProvider
from providers.s3_storage_provider import AwsS3Provider
from image_storage import ImageStorageCLI


class TestS3Storage(unittest.TestCase):
    """Contains tests for when aws_s3 is the dependency"""
    def getDatabaseService(self, db_name):
        """choose database service"""
        if db_name == "filesystem":
            self.provider = FileSystemProvider()
        elif db_name == "aws_s3":
            self.provider = AwsS3Provider()  

    def storage_service(self):
        self.instance = ImageStorageCLI(db_provider=self.provider)
        self.instance.setup_app()
        return self.instance      

    def test_0_cli_setup(self):
        self.instance = self.storage_service()
        expected = (True, "Connected Successfully")
        returned = self.instance.setup_app()
        self.assertEqual(returned, expected, "Check S3 Connection Test")
    
    def test_s3_upload(self):
        self.instance = self.storage_service()
        source = 'student.png'
        dest = f'/img/{source}'
        expected = (True,"Uploaded Successfully")
        returned = self.instance.upload_image(source, dest)
        self.assertEqual(returned, expected, "Check S3 Upload Test")
    
    def test_s3_download(self):
        self.instance = self.storage_service()
        dest = 'student.png'
        source = f'/img/{dest}'
        expected = (True, "Downloaded Successfully")
        returned = self.instance.download_image(source, dest)
        self.assertEqual(returned, expected, "Check S3 Download Test")
    
    def test_s3_get_secure_url(self):
        self.instance = self.storage_service()
        file = 'student.png'
        path = f'/img/{file}'
        returned = self.instance.get_secure_url(path=path)
        self.assertIn(True, returned, "Check S3 URL test")

    def test_s3_delete(self):
        self.instance = self.storage_service()
        source = 'student copy.png'
        dest = f'/img/{source}'
        self.instance.upload_image(source, dest)
        file = 'student copy.png'
        path = f'/img/{file}'
        expected = (True, "Deleted Successfully")
        returned = self.instance.delete_image(path=path)
        self.assertEqual(returned, expected, "Check S3 Delete Test")

    def test_s3_copy_file(self):
        self.instance = self.storage_service()
        file = 'student.png'
        source = f'/img/{file}'
        dest = f'/img2/{file}'
        expected = (True, 'File transferred')
        returned = self.instance.copy_file(source_uri=source, dest_url=dest)
        self.assertEqual(returned, expected, "Check S3 Copy test")

    def test_s3_list_files(self):
        self.instance = self.storage_service()
        dir = '/img/'
        returned = self.instance.list_images(directory=dir)
        self.assertIn(True, returned, "Check S3 List files test")

    def test_s3_file_exists(self):
        self.instance = self.storage_service()
        file_uri = '/img/student.png'
        expected = (True, 'File exists')
        returned = self.instance.check_if_file_exists(file_uri)
        self.assertEqual(returned, expected, "Check s3 File exists test")

    def test_s3_file_doesnot_exist(self):
        self.instance = self.storage_service()
        file_uri = '/img/student2.png'
        expected = (False, 'File doesnot exists')
        returned = self.instance.check_if_file_exists(file_uri)
        self.assertEqual(returned, expected, "Check s3 File doesnot exist test")

    def test_s3_create_directory(self):
        self.instance = self.storage_service()
        folder = '/testdir'
        expected = (True, 'Directory created')
        returned = self.instance.create_directory(folder)
        self.assertEqual(returned, expected, "Check S3 Create dir test")
    
    def test_s3_delete_directory(self):
        self.instance = self.storage_service()
        folder = '/testdir'
        expected = (True, 'Directory deleted')
        returned = self.instance.delete_directory(folder)
        self.assertEqual(returned, expected, "Check S3 delete dir test")

    def test_shut_app(self):
        expected = (True, "Disconnected Successfully")
        self.instance = self.storage_service()
        returned = self.instance.shut_app()
        self.assertEqual(returned, expected, "Check CLI Shut test")
        

if __name__ == "__main__":
    unittest.main()