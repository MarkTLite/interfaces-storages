import os

from providers.file_system_provider import FileSystemProvider
from providers.s3_storage_provider import AwsS3Provider
from storage_interface import StorageInterface

class ImageStorageCLI:
    def __init__(self, db_provider: "StorageInterface"):
        self.db_provider = db_provider
    
    def setup_app(self):        
        return self.db_provider.connect()

    def upload_image(self, source_uri: str, dest_url:str):
        return self.db_provider.upload_file(source_uri, dest_url)

    def download_image(self, source_uri: str, dest_url: str):
        return self.db_provider.download_file(source_uri,dest_url)

    def delete_image(self,path: str):
        return self.db_provider.delete_file(path)

    def get_secure_url(self, path: str):
        return self.db_provider.get_secure_file_url(path)

    def copy_file(self, source_uri: str, dest_url: str):
        return self.db_provider.copy_file(source_uri,dest_url)
    
    def list_images(self, directory: str):
        return self.db_provider.list_files_in_directory(directory)
    
    def check_if_file_exists(self, path: str):
        return self.db_provider.check_if_file_exists(path)
    
    def create_directory(self, directory: str):
        return self.db_provider.create_directory(directory)
    
    def delete_directory(self, directory: str):
        return self.db_provider.delete_directory(directory)

    def shut_app(self):
        return self.db_provider.disconnect()

# if __name__ == '__main__':    
#     choice = 'File storage'
#     print('Initialising Image Store App')

#     # Choose a provider dependency and inject it
#     # file_provider = FileSystemProvider()    
#     s3_provider = AwsS3Provider()

#     image_app = ImageStorageCLI(db_provider=s3_provider)
#     image_app.setup_app()
#     print('Done Initialising Image Store App')

#     # source_uri=''
#     # dest_url=''
#     # print(f'Uploading {source_uri} to {dest_url}')
#     # image_app.upload_image(source_uri='', dest_url='')
#     # print(f'Upload successful')

#     # source_uri=''
#     # dest_url=''
#     # print(f'Downloading image from {source_uri}')
#     # image_app.download_image(source_uri='', dest_url='')
#     # print(f'Download Successful')

#     # print(f'Uploading another image to {choice}')
#     # image_app.upload_image(source_uri='', dest_url='')
#     # print(f'Upload successful')

#     # path = ''
#     # print(f'Deleting image from {path}')
#     # image_app.delete_image(path=path)
#     # print(f'{path} successfully deleted')

#     # path = ''
#     # print(f'Generating secure image url ...')
#     # secure_url = image_app.get_secure_url(path=path)
#     # print(f'{secure_url} generated successfully')

#     # directory = ''
#     # print(f'Images in {directory}:')
#     # image_app.list_images(dir=directory)

#     # path = ''
#     # print(f'Checking for {path} ...')
#     # file_check = image_app.check_if_file_exists(path=path)
#     # print(f'file at {path} exists')

#     # directory = ''
#     # print(f'Creating dir at {directory} ...')
#     # dir_check = image_app.create_directory(dir=directory)
#     # print(f'file at {directory} created successfuly')

#     # directory = ''
#     # print(f'Deleting dir at {directory} ...')
#     # dir_check = image_app.create_directory(dir=directory)
#     # print(f'file at {directory} deleted successfuly')

#     # print('Shutting down Image Storage App')
#     # image_app.shut_app()


