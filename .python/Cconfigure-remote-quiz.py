import os
from pathlib import Path
import shutil
import boto3

s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")

base_folder = Path(__file__).parent.resolve()
app_root_folder = os.path.dirname(base_folder)
json_folder = os.path.join(app_root_folder, "json")
source_bucket = "amazoninstructor"
target_bucket = "amazoninstructor.info"
source_remote_prefix = "knowledge-check/"
target_objectName = "json/questions.json"

coursecode = input("Enter the course code: ") or "GK4504"
moduleNumber = input("Enter the module number: ") or "3"
moduleNumber = str(moduleNumber).zfill(
    2
)  # Ensuring moduleNumber is a string and zero-padded
coursecode = coursecode.upper()

# list all items in the source_bucket with prefix source_remote_prefix
response = s3_client.list_objects_v2(
    Bucket=source_bucket, Prefix=source_remote_prefix + coursecode
)

for content in response.get("Contents", []):
    if moduleNumber in content["Key"]:
        # copy the content to the target_bucket with the target_objectName
        s3_resource.meta.client.copy(
            {"Bucket": source_bucket, "Key": content["Key"]},
            target_bucket,
            target_objectName,
        )
        print(content["Key"])
