import os
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
            # open the json file and add the quiz_sessionID to the json
            with open(content["Key"], "r") as file:
                data = json.load(file)
                data["quiz_sessionID"] = quiz_sessionID
                # write the data back to the target-json file where Bucket=target_bucket and Key="json/questions.json",
                s3_client.put_object(
                    Bucket=target_bucket,
                    Key="json/questions.json",
                    Body=json.dumps(data),
                )
'''
                with open(content["Key"], "w") as file:
                    json.dump(data, file)
                    

            # Copy the object to the target bucket
            s3_client.copy_object(
                CopySource={"Bucket": source_bucket, "Key": content["Key"]},
                Bucket=target_bucket,
                Key="json/questions.json",
            )
            '''
            return f"Successfully copied {content['Key']} to {target_bucket}/json/questions.json"

    return "Module not found"


# Example usage
if __name__ == "__main__":
    # Simulate input values
    coursecode = "GK4504"
    module_number = "05"

    result = copy_module_data(coursecode, module_number)
    print(result)
