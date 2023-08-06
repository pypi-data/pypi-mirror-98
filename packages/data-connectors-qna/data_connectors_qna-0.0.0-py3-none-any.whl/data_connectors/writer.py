from abc import ABC, abstractmethod

import boto3


class Writer(ABC):
    @abstractmethod
    def write(self, output_path, data):
        pass

    @abstractmethod
    def write_s3(self):
        pass

    @abstractmethod
    def write_local(self):
        pass


class CsvWriter(Writer):
    def write(self, output_path, data):
        # TODO: add exceptions
        if "s3://" in output_path:
            self.write_s3(output_path, data)
        else:
            self.write_local(output_path, data)

    def write_s3(self, output_path, data):
        # boto code to create s3 client
        # write data from to s3 using self.serialized_data
        pass

    def write_local(self, output_path, data):
        # write to local file with context manager
        # and self.serialized_data
        pass
