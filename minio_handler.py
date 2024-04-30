import random
from datetime import datetime, timedelta
from config import MINIO_URL,MINIO_ACCESS_KEY,MINIO_SECRET_KEY,MINIO_BUCKET_NAME
import uuid
from pathlib import Path

from minio import Minio
import pdb


class MinioHandler():
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if not MinioHandler.__instance:
            MinioHandler.__instance = MinioHandler()
        return MinioHandler.__instance

    def __init__(self):
        #self.minio_url = 'nrc-file.xcoshop.com:9000'
        self.minio_url = MINIO_URL
        self.access_key = MINIO_ACCESS_KEY
        self.secret_key = MINIO_SECRET_KEY
        self.bucket_name = MINIO_BUCKET_NAME
        self.client = Minio(
            self.minio_url,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=True,
        )
        self.make_bucket()

    def make_bucket(self) -> str:
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
        return self.bucket_name

    def presigned_get_object(self, bucket_name, object_name):
        # Request URL expired after 7 days
        url = self.client.presigned_get_object(
            bucket_name=bucket_name,
            object_name=object_name,
            expires=timedelta(days=7)
        )
   
        return url
    
    def delete_object(self, bucket_name, object_name):
    # Delete the object immediately
        url =self.client.remove_object(
            bucket_name=bucket_name,
            object_name=object_name
        )
        return url

    def check_file_name_exists(self, bucket_name, file_name):
        try:
            self.client.stat_object(bucket_name=bucket_name, object_name=file_name)
            return True
        except Exception as e:
            print(f'[x] Exception: {e}')
            return False

    def put_object(self, bucket_name,  file_data, file_name, content_type):
        try:
            if " " in file_name:
                file_name = file_name.replace(" ", "")
            datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            object_name = f"{datetime_prefix}___{file_name}"
            while self.check_file_name_exists(bucket_name=bucket_name, file_name=object_name):
                random_prefix = random.randint(1, 1000)
                object_name = f"{datetime_prefix}___{random_prefix}___{file_name}"

            self.client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=file_data,
                content_type=content_type,
                length=-1,
                part_size=150 * 1024 * 1024
            )
            url = self.presigned_get_object(bucket_name=bucket_name, object_name=object_name)
            data_file = {
                'bucket_name': bucket_name,
                'file_name': object_name,
                'url': url
            }
            return data_file
        except Exception as e:
            raise Exception(e)
        
    def fput_object(self, bucket_name,  file_data, file_name, content_type):
        try:
           
            if " " in file_name:
                file_name = file_name.replace(" ", "")
            datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            subfolder_path = 'government/filemedia'
            object_name2 = f"{subfolder_path}/{datetime_prefix}___{file_name}"
            object_name = f"{datetime_prefix}___{file_name}"
            while self.check_file_name_exists(bucket_name=self.bucket_name, file_name=object_name):
                random_prefix = random.randint(1, 1000)
                object_name = f"{subfolder_path}/{datetime_prefix}___{random_prefix}___{file_name}"

            self.client.put_object(
                bucket_name=bucket_name,
                object_name=object_name2,
                data=file_data,
                content_type=content_type,
                length=-1,
                part_size=150 * 1024 * 1024
            )
            url = self.presigned_get_object(bucket_name=self.bucket_name, object_name=object_name2)
            data_file = {
                'bucket_name': self.bucket_name,
                'file_name': object_name2,
                'url': url
            }
            return data_file
        except Exception as e:
            raise Exception(e)
        
    def mput_object(self, bucket_name,  file_data, file_name, content_type):
        try:
            if " " in file_name:
                file_name = file_name.replace(" ", "")
            datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            subfolder_path = 'government/filemedia'
            object_name2 = f"{subfolder_path}/{datetime_prefix}___{file_name}"
            object_name = f"{datetime_prefix}___{file_name}"
            while self.check_file_name_exists(bucket_name=self.bucket_name, file_name=object_name):
                random_prefix = random.randint(1, 1000)
                object_name = f"{subfolder_path}/{datetime_prefix}___{random_prefix}___{file_name}"

            self.client.put_object(
                bucket_name=bucket_name,
                object_name=object_name2,
                data=file_data,
                content_type=content_type,
                length=-1,
                part_size=30 * 1024 * 1024
            )
            url = self.presigned_get_object(bucket_name=self.bucket_name, object_name=object_name)
            data_file = {
                'bucket_name': self.bucket_name,
                'file_name': object_name,
                'url': url
            }
            return data_file
        except Exception as e:
            raise Exception(e)
        
    
    def fput_object_song(self, bucket_name,  file_data, file_name, content_type):
        try:
           
            if " " in file_name:
                file_name = file_name.replace(" ", "")
            file_name_with_extension = file_name
            file_path = Path(file_name_with_extension)
            file_extension = file_path.suffix
            file_name = uuid.uuid5(uuid.NAMESPACE_URL, file_name)
            file_name = f"{file_name}_{file_extension}"
            datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            subfolder_path = 'government/filemedia'
            object_name2 = f"{subfolder_path}/{datetime_prefix}___{file_name}"
            object_name = f"{datetime_prefix}___{file_name}"
            while self.check_file_name_exists(bucket_name=self.bucket_name, file_name=object_name):
                random_prefix = random.randint(1, 1000)
                object_name = f"{subfolder_path}/{datetime_prefix}___{random_prefix}___{file_name}"

            self.client.put_object(
                bucket_name=bucket_name,
                object_name=object_name2,
                data=file_data,
                content_type=content_type,
                length=-1,
                part_size=150 * 1024 * 1024
            )
            
            url = self.presigned_get_object(bucket_name=bucket_name, object_name=object_name2)
            data_file = {
                'bucket_name': bucket_name,
                'file_name': object_name2,
                'url': url
            }
            return data_file
        except Exception as e:
            raise Exception(e)
