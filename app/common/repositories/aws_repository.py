from typing import List
from uuid import UUID, uuid4

import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile

from app.common.exceptions import AWSConfigException
from app.core.settings import AWS_BUCKET_NAME


class AWSRepository:
    def __init__(self, base_path: str):
        self.s3 = boto3.client("s3")
        self.AWS_BUCKET_NAME = AWS_BUCKET_NAME
        self.base_path = base_path

    def save_file(self, id_obj: UUID, uploaded_file: UploadFile) -> str:
        if not uploaded_file.filename.startswith("~"):
            try:
                file_name = uuid4().hex + ".jpg"
                file_path = f"{self.base_path}/{str(id_obj)}/images/{file_name}"
                self.s3.upload_fileobj(
                    uploaded_file.file,
                    self.AWS_BUCKET_NAME,
                    file_path,
                )
                return f"https://{self.AWS_BUCKET_NAME}.s3.us-east-1.amazonaws.com/{file_path}"
            except ClientError as e:
                raise AWSConfigException(detail=e.msg)

    def save_multiple_files(self, id_obj: UUID, uploaded_files: List[UploadFile]) -> List[str]:
        return [self.save_file(id_obj, uploaded_file) for uploaded_file in uploaded_files]

    def get_files(self, id_obj: UUID) -> List[str]:
        bucket = self.__get_bucket_data()
        response = []
        if bucket:
            for obj in bucket["Contents"]:
                if obj["Key"].startswith(f"{self.base_path}/{str(id_obj)}/images"):
                    response.append(
                        f"https://{self.AWS_BUCKET_NAME}.s3.us-east-1.amazonaws.com/{obj['Key']}"
                    )
        return response

    def delete_file(self, id_obj: UUID, file_name: str):
        file_path = f"{self.base_path}/{str(id_obj)}/images/{file_name}"
        try:
            self.s3.delete_object(Bucket=self.AWS_BUCKET_NAME, Key=file_path)
        except ClientError as e:
            raise AWSConfigException(detail=e.msg)

    def __get_bucket_data(self) -> dict:
        try:
            response = self.s3.list_objects_v2(
                Bucket=self.AWS_BUCKET_NAME,
                EncodingType="url",
                FetchOwner=True,
                RequestPayer="requester",
            )
            return response
        except ClientError as e:
            raise AWSConfigException(detail=e.msg)
