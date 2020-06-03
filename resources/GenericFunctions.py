# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

def decoratorGetPath(function):
    def wrapper(file_name:str):
        from pathlib import Path
        return Path('/tmp', file_name)
    return wrapper
@decoratorGetPath
def getPath(file_name:str):
    """Getting the local Path, deactivate decorator for local testing
    Arguments:
        file_name {str} -- my_file.csv
    Returns:
        Path
    """
    from os import getcwd
    from pathlib import Path
    return Path(getcwd(), file_name)

def decoratorGetWorkBook(function):
    def wrapper():
        from os import environ
        return environ.get('GOOGLE_SHEET')
    return wrapper
@decoratorGetWorkBook
def getWorkBook() -> str:
    """Returns (str) the Google Sheet name

    Argumentes:
        None
    Returns:
        (str): String from variable GOOGLE_SHEET_WORKBOOK
    """
    return 'BMO_Disposition_2020.xlsx'

def decoratorGetBucket(function):
    def wrapper():
        from os import environ
        return environ.get('BUCKET_NAME')
    return wrapper
@decoratorGetBucket
def getBucket() -> str:
    """Returns (str) the variable BUCKET_NAME

    Argumentes:
        None
    Returns:
        (str): String from variable BUCKET_NAME
    """
    return 'appusma206_apps_output'

def upload_blob(bucket_name:str, source_file_name:str, destination_blob_name:str):
    """Uploads object to store objct GCP Storage

    Arguments:
        bucket_name {str} -- "your-bucket-name"
        source_file_name {str} -- "local/path/to/file"
        destination_blob_name {str} -- "storage-object-name"
    """
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

def getWorkingFilePath(file_name: str) -> str:
    """Returns the OS working file path as a str
    
    Arguments:
        file_name (str): File name with extensions E.g: TestingData.csv
    Returns: 
        (str) 
    """
    return '{path_dir}{file_name}'.format(path_dir = getPath(), file_name = file_name)