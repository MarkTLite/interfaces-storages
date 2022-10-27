import abc

class StorageInterface(metaclass=abc.ABCMeta):
    """Interface for Common methods in storage operations"""   
    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass

    @abc.abstractmethod
    def upload_file(self, source_uri: str, dest_url: str):
        pass

    @abc.abstractmethod
    def download_file(self, source_uri: str, dest_url: str):
        pass

    @abc.abstractmethod
    def get_secure_file_url(self, path: str):
        pass

    @abc.abstractmethod
    def delete_file(self, path: str):
        pass

    @abc.abstractmethod
    def copy_file(self, source_uri: str, dest_url: str):
        pass

    @abc.abstractmethod
    def list_files_in_directory(self, dir: str):
        pass

    @abc.abstractmethod
    def check_if_file_exists(self, file_uri: str):
        pass 

    @abc.abstractmethod
    def create_directory(self, dir: str):
        pass

    @abc.abstractmethod
    def delete_directory(self, dir: str):
        pass

