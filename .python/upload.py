import os
import mimetypes
import boto3
from datetime import datetime
import subprocess
from pathlib import Path

s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")
cloudfront_client = boto3.client("cloudfront")

base_folder = Path(__file__).parent.resolve()
app_root_folder = os.path.dirname(base_folder)
src_folder = os.path.join(app_root_folder, "src")
local_dist_folder = os.path.join(app_root_folder, "dist")


def run_command(command):
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=app_root_folder,
            shell=True,
        )
        print(result.stdout.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr.decode('utf-8')}")
        raise


def commit_to_git():
    # Add changes to git
    run_command(["git", "add", "."])

    # Commit with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"commit on publish {timestamp}"
    run_command(["git", "commit", "-m", commit_message])

    # Push to main branch
    run_command(["git", "push", "-u", "origin", "main"])


def rewrite_package_json(package_file):
    pack = os.path.join(app_root_folder, package_file)
    with open(pack, encoding="utf-8", mode="r") as f:
        lines = f.readlines()

    # Write back to the file with the modification
    with open(pack, encoding="utf-8", mode="w") as f:
        for line in lines:
            if line.strip().startswith('"homepage"'):
                f.write(manifest_homepage_item)
            else:
                f.write("  " + line)


def rewrite_index_file(index_file):
    pack = os.path.join(local_dist_folder, index_file)
    with open(pack, encoding="utf-8", mode="r") as f:
        lines = f.readlines()

    # Write back to the file with the modification
    with open(pack, encoding="utf-8", mode="w") as f:
        for line in lines:
            if line.strip().__contains__("/assets/"):
                line = line.replace("/assets/", "/react/knowledge-check/assets/")
                f.write(line)
            else:
                f.write("  " + line)


def upload_files_to_s3(bucket_name, local_dist_folder, remote_path):
    print(local_dist_folder)
    for root, dirs, files in os.walk(local_dist_folder):
        for file_name in files:
            local_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(local_path, local_dist_folder)
            s3_key = os.path.join(remote_path, relative_path).replace(
                "\\", "/"
            )  # Normalize path for S3
            content_type = (
                mimetypes.guess_type(file_name)[0] or "application/octet-stream"
            )
            print(
                f"Uploading {local_path} to {s3_key} in bucket {bucket_name} with content type {content_type}"
            )
            s3_client.upload_file(
                local_path,
                bucket_name,
                s3_key,
                ExtraArgs={"ContentType": content_type, "ACL": "public-read"},
            )
    print("Upload completed.")
    print(f"http://{bucket_name}/{remote_path}index.html")


def delete_all_objects(bucket_name, prefix):
    bucket = s3_resource.Bucket(bucket_name)  # type: ignore
    bucket.objects.filter(Prefix=prefix).delete()
    print(f"Deleted all objects in bucket {bucket_name} with prefix {prefix}")


def create_cloudfront_invalidation(distribution_id, path):
    caller_reference = f"invalidation-{datetime.now().isoformat()}"
    invalidation = cloudfront_client.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            "Paths": {"Quantity": 1, "Items": [f"/{path}*"]},
            "CallerReference": caller_reference,
        },
    )
    invalidation_id = invalidation["Invalidation"]["Id"]
    print(f"Invalidation ID: {invalidation_id}")


# Usage example
distribution_id = "E2R80P4OGLMSIV"  # CloudFront distribution ID
bucket_name = "demo.amazoninstructor.info"
local_dist_folder = os.path.join(app_root_folder, "dist")  #'./build/'
remote_path = "react/" + os.path.basename(os.getcwd()) + "/"
manifest_homepage_item = f'"homepage": "/{remote_path}",\n'

rewrite_package_json("package.json")
run_command(["npm", "run", "build"])
rewrite_index_file("index.html")
delete_all_objects(bucket_name, remote_path)
upload_files_to_s3(bucket_name, local_dist_folder, remote_path)
create_cloudfront_invalidation(distribution_id, remote_path)
commit_to_git()
