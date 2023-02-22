#!/usr/bin/env python
# coding: utf-8

# --------------------------------------------------------------------------------

import json
import io
import tarfile
from typing import Dict, List, Any

# import logging

from google.cloud.storage.client import Client
from google.cloud.storage.bucket import Bucket

# logger = logging.getLogger('app')


class GCPStorageClient(object):

    client: Client = None
    bucket: Bucket = None
    public_base: str = ""
    project_id: str = ""
    parent: str = ""

    def __init__(cls, project_id: str = "my-project", bucket_name: str = "my-bucket"):
        """
        :param project_id: project id
        :param bucket_name: bucket name
        """
        cls.public_base = "https://storage.googleapis.com"
        cls.project_id = project_id
        cls.parent = f"projects/{cls.project_id}"
        cls.client = Client()
        cls.bucket = cls.client.get_bucket(
            bucket_name if bucket_name else cls.project_id
        )

    def download(cls, blob_name: str, to_file_name: str):
        """
        :param blob_name: the name for the existing file
        :param to_file_name: the name for the new file
        """
        blob = cls.bucket.get_blob(blob_name)
        blob.download_to_filename(to_file_name)
        return cls.bucket

    def upload(cls, blob_name: str, file: str = '', payload: Any = None):
        """
        :param blob_name: the blob name for the new file
        :param file: the name of the file to upload
        :param payload: the payload of the file to upload
        """
        if payload and isinstance(payload, str):
            blob = cls.bucket.blob(blob_name)
            blob.upload_from_string(json.dumps(payload), 'application/json')

        if file and isinstance(file, str):
            blob = cls.bucket.blob(blob_name)
            blob.upload_from_filename(payload)
