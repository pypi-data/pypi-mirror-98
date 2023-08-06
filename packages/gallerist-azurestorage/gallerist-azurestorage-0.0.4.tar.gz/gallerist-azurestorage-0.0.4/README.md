[![Build](https://github.com/Neoteroi/Gallerist-AzureStorage/actions/workflows/build.yml/badge.svg)](https://github.com/Neoteroi/Gallerist-AzureStorage/actions/workflows/build.yml)
[![pypi](https://img.shields.io/pypi/v/gallerist-azurestorage.svg)](https://pypi.python.org/pypi/gallerist-azurestorage)
[![versions](https://img.shields.io/pypi/pyversions/gallerist-azurestorage.svg)](https://github.com/Neoteroi/Gallerist-AzureStorage)
[![license](https://img.shields.io/github/license/Neoteroi/Gallerist-AzureStorage.svg)](https://github.com/Neoteroi/Gallerist-AzureStorage/blob/main/LICENSE)

# Gallerist-AzureStorage
Gallerist classes for Azure Storage: implements reading image files from Azure
Blob Service, and writing of resized pictures to the same.

```bash
$ pip install gallerist-azurestorage
```

This library is used in
[Gallerist-AzureFunctions](https://github.com/Neoteroi/Gallerist-AzureFunctions),
an Azure Functions front-end that uses
[`Gallerist`](https://github.com/Neoteroi/Gallerist) library, to resize
pictures in Azure Storage Blob Service.

# Example: synchronous code resizing pictures on Azure Storage

```python
from gallerist import Gallerist, ImageSize
from galleristazurestorage import AzureBlobFileStore

store = AzureBlobFileStore.from_connection_string(
    "<YOUR_CONNECTION_STRING>",
    "CONTAINER_NAME",
)

gallerist = Gallerist(store)

# configuring sizes by mime (use '*' to match any other mime):
gallerist = Gallerist(
    store,
    sizes={
        "image/jpeg": [ImageSize("a", 1200), ImageSize("b", 600), ImageSize("c", 300)],
        "image/png": [ImageSize("a", 350), ImageSize("b", 250), ImageSize("c", 150)],
    },
)

# the following function call causes the creation of several versions of the
# image in different sizes; note that this operation is CPU bound
metadata = gallerist.process_image("ORIGINAL_FILE_NAME_ALREADY_ON_STORAGE.png")

print(metadata)

```

# Asynchronous example using executors (recommended for async scenarios)

```python
import asyncio
import concurrent.futures

from gallerist import Gallerist, ImageSize

from galleristazurestorage import AzureBlobFileStore

store = AzureBlobFileStore.from_connection_string(
    "<YOUR_CONNECTION_STRING>",
    "CONTAINER_NAME",
)

gallerist = Gallerist(store)

# configuring sizes by mime (use '*' to match any other mime):
gallerist = Gallerist(
    store,
    sizes={
        "image/jpeg": [ImageSize("a", 1200), ImageSize("b", 600), ImageSize("c", 300)],
        "image/png": [ImageSize("a", 350), ImageSize("b", 250), ImageSize("c", 150)],
    },
)


async def main():
    loop = asyncio.get_event_loop()

    with concurrent.futures.ProcessPoolExecutor() as pool:
        metadata = await loop.run_in_executor(
            pool, gallerist.process_image, "EXISTING_FILE_ON_STORAGE.jpg"
        )

        print(metadata)


asyncio.run(main())

```

Alternatively to using an executor explicitly, it is possible to use
`loop.call_soon_threadsafe`:

```python
from gallerist import Gallerist, ImageSize
from galleristazurestorage import AzureBlobFileStore

store = AzureBlobFileStore.from_connection_string(
    "<YOUR_CONNECTION_STRING>",
    "CONTAINER_NAME",
)

gallerist = Gallerist(store)

# configuring sizes by mime (use '*' to match any other mime):
gallerist = Gallerist(
    store,
    sizes={
        "image/jpeg": [ImageSize("a", 1200), ImageSize("b", 600), ImageSize("c", 300)],
        "image/png": [ImageSize("a", 350), ImageSize("b", 250), ImageSize("c", 150)],
    },
)

def process_image(image_path: str):
    # configuring sizes by mime (use '*' to match any other mime):
    gallerist = Gallerist(
        store,
        sizes={
            "image/jpeg": [
                ImageSize("a", 1200),
                ImageSize("b", 600),
                ImageSize("c", 300),
            ],
            "image/png": [
                ImageSize("a", 350),
                ImageSize("b", 250),
                ImageSize("c", 150),
            ],
        },
    )

    metadata = gallerist.process_image(image_path)

    print(metadata)


async def main():
    loop = asyncio.get_event_loop()
    loop.call_soon_threadsafe(process_image, "EXISTING_FILE_ON_STORAGE.jpg")


asyncio.run(main())
```

# Asynchronous example using asynchronous methods from azure-storage-blob.aio

Note: `azure-storage-blob` requires `aiohttp`, and is not compatible with
`concurrent.futures.ProcessPoolExecutor`.

```python
import asyncio
from gallerist import Gallerist, ImageSize
from galleristazurestorage.aio import AzureBlobAsyncFileStore

store = AzureBlobFileStore.from_connection_string(
    "<YOUR_CONNECTION_STRING>",
    "CONTAINER_NAME",
)

gallerist = Gallerist(store)

# configuring sizes by mime (use '*' to match any other mime):
gallerist = Gallerist(
    store,
    sizes={
        "image/jpeg": [ImageSize("a", 1200), ImageSize("b", 600), ImageSize("c", 300)],
        "image/png": [ImageSize("a", 350), ImageSize("b", 250), ImageSize("c", 150)],
    },
)


async def main():
    metadata = await gallerist.process_image_async(
        "EXISTING_FILE_ON_STORAGE.jpg"
    )

    print(metadata)


asyncio.run(main())
```
