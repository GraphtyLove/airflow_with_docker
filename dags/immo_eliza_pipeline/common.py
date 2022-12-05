import os
from typing import Tuple
from azure.storage.blob import BlobServiceClient



def get_enviroment_variables() -> Tuple[str, str]:
    """
    return the environment variables if they are set. If not, raise an error.
    """

    connection_string = os.getenv("AZURE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_CONTAINER_NAME")
    if not connection_string:
        raise ValueError("AZURE_CONNECTION_STRING not found. Check your .env file")
    elif not container_name:
        raise ValueError("AZURE_CONTAINER_NAME not found. Check your .env file")    

    print("Environment variables are set:")

    return connection_string, container_name


def upload_file(local_file_path: str, blob_name: str) -> None:
    """
    Upload a blob (file) to an Azure Storage container.

    :param local_file_path: The path to the local file to upload.
    :param blob_name: The name to give the blob (file) in the container.
    """
    
    # Load environment variables
    connection_string, container_name = get_enviroment_variables()

    # Initialize the connection to Azure
    blob_service_client =  BlobServiceClient.from_connection_string(connection_string)

    # Create the client to interact with the Azure Storage Container
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    print(f"uploading file: {local_file_path}....")
    
    # Open local file
    with open(local_file_path, "rb") as file:
      # Write local file to blob overwriting any existing data
      blob_client.upload_blob(file, overwrite=True)

    print("file uploaded!")

    return



def download_file(local_file_desired_path: str, blob_name: str) -> str:
    """
    Download a blob (file) from an Azure Storage container and save it to a local file.

    :param local_file_desired_path: The path to the local file to save the blob to.
    :param blob_name: The name of the blob (file) to download.
    :return: The path to the local file.
    """

    # Load environment variables
    connection_string, container_name = get_enviroment_variables()

    # Initialize the connection to Azure Storage Container
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # Create the client to interact with the Azure Storage Container
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    print(f"Downloading file: {blob_name}...")
    
    blob_data = blob_client.download_blob().read().decode("utf-8")

    print("File's data: ", blob_data)


    print("Writing data to local file...")
    # Write data to local file 
    # (Not mandatory if you just want to read the data!)
    with open(local_file_desired_path, "w") as file:
        file.write(blob_data)
    
    print("File downloaded!")
    
    return local_file_desired_path

