from pyworks_storage.config import config
from pyworks_storage.aws import AWSS3Storage

class Storage:

    def __init__(self) -> None:
        pass

    def disk(self, disk_name: str='s3'):
        if disk_name == 's3':
            return AWSS3Storage(config.AWS_BUCKET_NAME)
        else:
            raise Exception('Storage provider is not support!')