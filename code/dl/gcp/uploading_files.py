from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

if __name__ == "__main__":
    import os
    bucket_name = "dl-data-bucket"
    for filename in os.listdir("./data"):
        file_path = os.path.join("data", filename)
        source_file_name = file_path
        destination_blob_name = filename
        upload_blob(bucket_name, source_file_name, destination_blob_name)
