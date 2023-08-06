from io import BytesIO

from azure.storage.blob import BlobServiceClient, ContentSettings
from gallerist.abc import FileInfo, SyncFileStore


class AzureBlobFileStore(SyncFileStore):
    def __init__(self, blob_client: BlobServiceClient, container_name: str):
        self.service = blob_client
        self.container_name = container_name

    @classmethod
    def from_connection_string(
        cls, connection_string: str, container_name: str
    ) -> "AzureBlobFileStore":
        return cls(
            BlobServiceClient.from_connection_string(connection_string),
            container_name,
        )

    def read_file(self, file_path: str) -> bytes:
        downloader = self.service.get_blob_client(
            self.container_name, file_path
        ).download_blob()
        stream = BytesIO()
        downloader.readinto(stream)
        return stream.getvalue()

    def write_file(self, file_path: str, data: bytes, info: FileInfo):
        blob_client = self.service.get_blob_client(self.container_name, file_path)
        blob_client.upload_blob(
            BytesIO(data),
            content_settings=ContentSettings(content_type=info.mime),
        )

    def delete_file(self, file_path: str):
        blob_client = self.service.get_blob_client(self.container_name, file_path)
        blob_client.delete_blob()
