from abc import ABC, abstractmethod
import json

import boto3
import botocore


class Reader(ABC):
    @abstractmethod
    def read(self, input_path):
        pass

    @abstractmethod
    def read_s3(self, input_path):
        pass

    @abstractmethod
    def read_local(self, input_path):
        pass


def split_s3_path(s3_path):
    """Credit to: https://stackoverflow.com/questions/42641315/s3-urls-get-bucket-name-and-path"""
    path_parts = s3_path.replace("s3://", "").split("/")
    bucket = path_parts.pop(0)
    key = "/".join(path_parts)
    return bucket, key


class JsonReader(Reader):
    def read(self, input_path):
        if "s3://" in input_path:
            return self.read_s3(input_path)
        else:
            return self.read_local(input_path)

    def read_s3(self, input_path):
        # boto code to create s3 client
        bucket, key = split_s3_path(input_path)

        s3 = boto3.resource('s3')

        try:
            s3.Bucket(bucket).download_file(key, "data.json")
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

        self.read_local("data.json")

    def read_local(self, input_path):
        # read from local file with context manager
        with open(input_path) as f:
            data = json.load(f)
            return data
