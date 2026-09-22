import boto3

BUCKET_NAME = "sales-data-pipeline-666398468806"

def main():
    s3 = boto3.client("s3")

    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix="raw/"
    )

    print("Files in S3:")

    for obj in response.get("Contents", []):
        print(obj["Key"])


if __name__ == "__main__":
    main()