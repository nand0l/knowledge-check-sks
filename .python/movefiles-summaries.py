import boto3
import os
from pathlib import Path

base_folder = Path(__file__).parent.resolve()
app_root_folder = os.path.dirname(base_folder)
src_folder = os.path.join(app_root_folder, 'src')

def move_s3_objects_and_generate_links(source_bucket, source_prefix, destination_bucket, destination_prefix, output_file):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    audio_links = []

    for page in paginator.paginate(Bucket=source_bucket, Prefix=source_prefix):
        for obj in page.get('Contents', []):
            source_key = obj['Key']
            filename = source_key.split('/')[-1]
            destination_key = destination_prefix + filename
            
            # Copy the object to the new bucket with the new prefix
            s3.copy_object(
                Bucket=destination_bucket,
                CopySource={'Bucket': source_bucket, 'Key': source_key},
                Key=destination_key
            )
            
            # Delete the object from the source bucket
            s3.delete_object(Bucket=source_bucket, Key=source_key)
            
            # Add the new URL to the list
            audio_url = f"https://{destination_bucket}/{destination_key}"
            audio_links.append(f'"{audio_url}"')
            print(f"Moved {source_key} to {destination_key}")

    # Generate the audioLinks.js file
    with open(output_file, 'w') as f:
        f.write("const audioLinks = [\n")
        f.write(",\n".join(audio_links))
        f.write("\n];\n")
        f.write("\nexport default audioLinks;")
    
    print(f"{output_file} generated successfully.")

# Example usage
'''
destination_bucket = 'amazoninstructor.audio'
destination_prefix = 'polly-output/'
source_bucket = 'amazoninstructor.info'
source_prefix = 'audio/MLS-C01/summaries/'

'''
source_bucket = 'amazoninstructor.audio'
source_prefix = "polly-output-summaries/"
destination_bucket = 'amazoninstructor.info'
destination_prefix = 'audio/MLS-C01/summaries/'


output_file = os.path.join(src_folder,'audioLinks.js')


move_s3_objects_and_generate_links(source_bucket, source_prefix, destination_bucket, destination_prefix, output_file)
