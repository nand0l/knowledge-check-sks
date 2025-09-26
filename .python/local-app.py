import json
import boto3
import datetime

quiz_sessionID = int(datetime.datetime.now().timestamp())
s3_client = boto3.client("s3")

source_bucket = "amazoninstructor"
target_bucket = "amazoninstructor.info"


def copy_module_data(coursecode="GK4504", module_number="04"):
    # Ensure the course code is uppercase and module number is padded to two digits
    coursecode = coursecode.upper()
    module_number = module_number.zfill(2)

    # S3 copy logic
    source_remote_prefix = "knowledge-check/"
    response = s3_client.list_objects_v2(
        Bucket=source_bucket, Prefix=f"{source_remote_prefix}{coursecode}"
    )

    for content in response.get("Contents", []):
        if module_number in content["Key"]:
            # Get the object from S3
            s3_object = s3_client.get_object(Bucket=source_bucket, Key=content["Key"])

            # Load the object content as JSON
            data = json.loads(s3_object["Body"].read().decode("utf-8"))

            # Add the quiz_sessionID to the JSON
            data["quiz_sessionID"] = quiz_sessionID

            # Put the modified JSON back to the target S3 bucket
            s3_client.put_object(
                Bucket=target_bucket,
                Key="json/questions.json",
                Body=json.dumps(data),
                ContentType="application/json",
            )

            return f"Successfully copied {content['Key']} to {target_bucket}/json/questions.json"

    return "Module not found"


# Example usage
if __name__ == "__main__":
    # Simulate input values
    coursecode = "GK4504"
    module_number = "06"

    result = copy_module_data(coursecode, module_number)
    print(result)
