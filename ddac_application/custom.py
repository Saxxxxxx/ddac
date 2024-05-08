from storages.backends.s3boto3 import S3Boto3Storage

class ReadOnlyS3Boto3Storage(S3Boto3Storage):
    def _save(self, name, content):
        return name




        