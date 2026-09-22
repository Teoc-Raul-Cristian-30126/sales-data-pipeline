import boto3
import os


BUCKET_NAME = "sales-data-pipeline-666398468806"


def upload_directory_to_s3(local_directory, s3_prefix):
    s3 = boto3.client("s3")

    for root, _, files in os.walk(local_directory):
        for file in files:
            local_path = os.path.join(root, file)

            relative_path = os.path.relpath(
                local_path,
                local_directory
            )

            s3_key = f"{s3_prefix}/{relative_path}".replace("\\", "/")

            print(f"Uploading: {local_path} -> s3://{BUCKET_NAME}/{s3_key}")

            s3.upload_file(
                local_path,
                BUCKET_NAME,
                s3_key
            )


def main():
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    raw_directory = os.path.join(
        project_root,
        "data",
        "raw"
    )

    upload_directory_to_s3(
        raw_directory,
        "raw"
    )

    print("\nUpload to S3 completed successfully!")


if __name__ == "__main__":
    main()