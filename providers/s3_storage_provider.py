import boto3, os

from storage_interface import StorageInterface
from botocore.exceptions import ClientError
from dotenv import load_dotenv


class AwsS3Provider(StorageInterface):
    def connect(self):
        load_dotenv()
        credentials = {
            'aws_access_key_id': os.getenv('aws_access_key_id'),
        'aws_secret_access_key': os.getenv('aws_secret_access_key'),
        }
        self.bucket_name = 'interfaces-prac' 
   
        self.s3_resource = boto3.resource('s3',**credentials)
        self.s3_client = boto3.client('s3', **credentials)   
        self.bucket = self.s3_resource.Bucket(name= self.bucket_name)
        return (True, "Connected Successfully")

    def disconnect(self):
        return (True, "Disconnected Successfully")

    def upload_file(self, source_uri: str, dest_url: str):
        try:
            response = self.s3_client.upload_file(source_uri, self.bucket_name, dest_url)
            return (True, 'File transferred')

        except(Exception, ClientError) as e:
            print(e)
            return (False, "Error")

    def download_file(self, source_uri: str, dest_url: str):
        dl_dest = dest_url
        try:
            response = self.s3_client.download_file(self.bucket_name, source_uri, dl_dest)
            return (True, 'File transferred')

        except(Exception, ClientError) as e:
            print(e)
            return (False,"Error")
        
    def get_secure_file_url(self, path: str):
        try:
            if path is None:
                raise Exception()
            response = self.s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': self.bucket_name,
                                                            'Key': path},
                                                    ExpiresIn=3600)
            # The response contains the presigned URL
            return (True, response)

        except (Exception, ClientError) as e:
            print(e)
            return (False, "Error")

    def delete_file(self, path: str):
        try:
            if path is None:
                raise Exception()
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=path)
            print(f'File at {path} deleted succesfully')
            return (True, "File deleted")
        
        except(Exception, ClientError) as err:
            print(f'Error: {err}')
            return (False, 'Error')

    def copy_file(self, source_uri: str, dest_url: str):
        copy_source = {
        'Bucket': self.bucket_name,
        'Key': source_uri
    }
        try: 
            self.s3_resource.Object(self.bucket_name, dest_url).copy(copy_source)
            print(f'File transferred successsfuly to {dest_url}')
            return (True, 'File transferred')   

        except(Exception, ClientError) as err:
            print(f'Error: {err}')
            return (False, 'Error')
        
    def list_files_in_directory(self, dir: str):
        files = []
        try:
            if dir is None:
                raise Exception()
            for obj in self.bucket.objects.all():
                if obj.key.__contains__(dir):
                    files.append(obj.key)
            
            return (True, files)

        except(Exception, ClientError) as err:
            print(f'Error: {err}')
            return (False, 'Error')

    def check_if_file_exists(self, file_uri: str):
        try:
            for obj in self.bucket.objects.all():
                if obj.key.__contains__(file_uri):
                    print(f'File at {file_uri} exists')
                    return (True, 'File exists')
            
            print(f'File at {file_uri} doesnot exist')
            return (False, 'Error')

        except(Exception, ClientError) as err:
            print(f'Error: {err}')
            return (False, 'Error')

    def create_directory(self, dir: str):
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=(dir+'/'))
            print(f'Directory: {dir}/ succesfully created')
            return (True, 'Directory created')

        except(Exception, ClientError) as err:
            print(f'Error: {err}')
            return (False, 'Error')

    def delete_directory(self, dir: str):
        try:
            for obj in self.bucket.objects.all():
                if obj.key.__contains__(dir):                 
                    self.s3_resource.Object(self.bucket_name, dir).delete()

            print(f'Directory: {dir}/ succesfully deleted')
            return (True, 'Directory deleted')

        except(ClientError, Exception) as e:
            print(e)
            return (False, 'Error')

