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
remote_prefix = "knowledge-check/"

coursecode = input("Enter the course code: ") or "GK4504"
moduleNumber = input("Enter the module number: ") or 3
moduleNumber = str(moduleNumber).zfill(2)  # Ensuring moduleNumber is a string and zero-padded
coursecode = coursecode.upper()

# list all items in the source_bucket with prefix remote_prefix
response = s3_client.list_objects_v2(
    Bucket=source_bucket, Prefix=remote_prefix + coursecode
)

for content in response.get("Contents", []):
    print(content["Key"])

course_folder = os.path.join(json_folder, coursecode)

# list all items in the course_folder
for item in os.listdir(course_folder):
    # copy the file that has the moduleNumber in the name
    if moduleNumber in item:
        print(item)
        # copy the file to the current working directory
        shutil.copy(
            os.path.join(course_folder, item),
            os.path.join(json_folder, "questions.json"),
        )

# copy the questions.json to an s3 bucket
s3_client.upload_file(
    os.path.join(json_folder, "questions.json"), target_bucket, "json/questions.json"
)
