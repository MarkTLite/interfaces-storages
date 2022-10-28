import os
import shutil

from storage_interface import StorageInterface


class FileSystemProvider(StorageInterface):
    def connect(self):
        self.base_path = 'file_store/'
        return (True, "Connected Successfully")

    def disconnect(self):
        return (True, "Disconnected Successfully")

    def upload_file(self, source_uri: str, dest_url: str):
        return self.copy_file(source_uri, dest_url)

    def download_file(self, source_uri: str, dest_url: str):
        return self.copy_file(source_uri, dest_url)
        
    def get_secure_file_url(self, path: str):
        if path is None:
                return (False, 'Error')
        return (True, "")

    def delete_file(self, path: str) -> tuple:        
        try:
            path = self.base_path + path
            os.remove(path)
            print(f'File at {path} deleted succesfully')
            return (True, "File deleted")
        
        except(Exception) as err:
            print(f'Error: {err}')
            return (False, 'Error')

    def copy_file(self, source_uri: str, dest_url: str) -> tuple:
        try:
            source_uri = self.base_path + source_uri
            dest_url = self.base_path + dest_url          # basing on the file store folder
            shutil.copy(source_uri, dest_url)
            print(f'File transferred successsfuly to {dest_url}')
            return (True, 'File transferred')   

        except(Exception) as err:
            print(f'Error: {err}')
            return (False, 'Error')
        
    def list_files_in_directory(self, dir: str):
        
        try:
            path = self.base_path + dir
            with os.scandir(path) as entries:
                for entry in entries:
                    print(entry.name)
            
            return (True, "List Success")

        except(Exception) as err:
            print(f'Error: {err}')
            return (False, "Error")

    def check_if_file_exists(self, file_uri: str) -> tuple:
        file_uri = self.base_path + file_uri
        if os.path.isfile(file_uri):
            print(f'File at {file_uri} exists')
            return (True, 'File exists')
        else:
            print(f'File at {file_uri} doesnot exist')
            return (False, 'Error')

    def create_directory(self, dir: str):
        
        try:
            dir = self.base_path + dir
            os.mkdir(dir)
            print(f'Directory: {dir} succesfully created')
            return (True, 'Directory created')

        except(Exception, FileExistsError) as err:
            print(f'Error: {err}')
            return (False, 'Error')

    def delete_directory(self, dir: str):        
        try:
            dir = self.base_path + dir
            shutil.rmtree(dir)
            print(f'Directory: {dir} succesfully deleted')
            return (True, 'Directory deleted')

        except(Exception, OSError) as e:
            return (False, 'Error')

