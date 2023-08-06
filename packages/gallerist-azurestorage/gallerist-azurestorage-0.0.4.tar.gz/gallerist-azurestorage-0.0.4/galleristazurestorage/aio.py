from io import BytesIO

from azure.storage.blob import ContentSettings
from azure.storage.blob.aio import BlobServiceClient
from gallerist.abc import FileInfo, FileStore


class AzureBlobAsyncFileStore(FileStore):
    def __init__(self, blob_client: BlobServiceClient, container_name: str):
        self.service = blob_client
        self.container_name = container_name

    @classmethod
    def from_connection_string(
        cls, connection_string: str, container_name: str
    ) -> "AzureBlobAsyncFileStore":
        return cls(
            BlobServiceClient.from_connection_string(connection_string),  # type: ignore
            container_name,
        )

    async def read_file(self, file_path: str) -> bytes:
        downloader = await self.service.get_blob_client(
            self.container_name, file_path
        ).download_blob()
        stream = BytesIO()
        await downloader.readinto(stream)
        return stream.getvalue()

    async def write_file(self, file_path: str, data: bytes, info: FileInfo):
        blob_client = self.service.get_blob_client(self.container_name, file_path)
        await blob_client.upload_blob(
            BytesIO(data),
            content_settings=ContentSettings(content_type=info.mime),
        )

    async def delete_file(self, file_path: str):
        blob_client = self.service.get_blob_client(self.container_name, file_path)
        await blob_client.delete_blob()
