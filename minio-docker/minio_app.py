from minio import Minio
from minio.error import S3Error

def main():
    client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    source_file = "images_tmp/green pixel anime.jpg"
    bucket_name = "python-bucket"
    destination_file = "pixel_anime.jpg"

    # Make the bucket if it doesn't exist.
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    # Upload the file, renaming it in the process
    client.fput_object(
        bucket_name, destination_file, source_file,
    )
    print(
        source_file, "successfully uploaded as object",
        destination_file, "to bucket", bucket_name,
    )
    url = client.presigned_get_object(bucket_name, destination_file)
    print("URL to download:", url)

if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)