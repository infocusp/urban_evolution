import numpy as np
import rasterio
import gcsfs
from io import BytesIO
from google.cloud import storage
from dataclasses import dataclass
from typing import Any, Dict, Optional, List

PROJECT_ID = "ai-sandbox-399505"


@dataclass
class TIFF():
    data: np.ndarray
    metadata: Dict[str, Any]
    bands: List[str]
    profile: Dict[str, Any]


def gcsfs_init():

    return  gcsfs.GCSFileSystem()


def get_storage_client():

    return storage.Client(project=PROJECT_ID)

def get_bucket_name(gcs_path):

    if not gcs_path.startswith("gs://"):
        raise ValueError("The path must start with 'gs://'")
    
    stripped_path = gcs_path[5:]
    parts = stripped_path.split('/', 1)

    bucket_name = parts[0]
    file_path = parts[1] if len(parts) > 1 else ""

    return bucket_name, file_path

def rasterio_open(file):
    with rasterio.open(file) as src:
        tiff_data = src.read()  
        metadata = src.meta 
        bands = src.descriptions  
        profile = src.profile
    return TIFF(tiff_data, metadata, bands, profile)


def load_tiff(gsc_path):
    gcs = gcsfs_init()
    with gcs.open(gsc_path, 'rb') as f:
        file_bytes = BytesIO(f.read())
    
    tif = rasterio_open(file_bytes)
    return tif

def load_tif_data(gcs_tiff_path):

    tif = load_tiff(gcs_tiff_path)

    return tif.data

def files_in_dir(bucket_path, file_extension):

    all_files = []
    client = get_storage_client()
    bucket_name, file_path = get_bucket_name(bucket_path)
    bucket = client.get_bucket(bucket_name)
    for blob in bucket.list_blobs(prefix = file_path):
        all_files.append(blob.name)
    file_prefix = "gs://" + bucket_name + "/"
    if file_extension:
        fileterd_files = [file_prefix+ file for file in all_files if file.endswith(file_extension)]

    client.close()
        
    return fileterd_files

