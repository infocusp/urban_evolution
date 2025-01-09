import numpy as np
import rasterio
import gcsfs
import logging
from io import BytesIO, StringIO
from rasterio.io import MemoryFile
from google.cloud import storage
from dataclasses import dataclass
from typing import Any, Dict, List

PROJECT_ID = "ai-sandbox-399505"


@dataclass
class TIFF():
    data: np.ndarray
    metadata: Dict[str, Any]
    bands: List[str]
    profile: Dict[str, Any]


def gcsfs_init():
    """ init gcs file system"""
    return  gcsfs.GCSFileSystem()


def get_storage_client():
    """ fetch gcs storage client"""
    return storage.Client(project=PROJECT_ID)

def get_bucket_name(gcs_path):
    """ 
    Filteres the bucket name and file path 
    from the given gcs path
    """
    if not gcs_path.startswith("gs://"):
        raise ValueError("The path must start with 'gs://'")
    
    stripped_path = gcs_path[5:]
    parts = stripped_path.split('/', 1)

    bucket_name = parts[0]
    file_path = parts[1] if len(parts) > 1 else ""

    return bucket_name, file_path

def rasterio_open(file):
    """ opens a tiff file"""
    with rasterio.open(file) as src:
        tiff_data = src.read()  
        metadata = src.meta 
        bands = src.descriptions  
        profile = src.profile
    return TIFF(tiff_data, metadata, bands, profile)


def load_tiff(gsc_path):
    """loads a tiff object conttaining all information"""
    gcs = gcsfs_init()
    with gcs.open(gsc_path, 'rb') as f:
        file_bytes = BytesIO(f.read())
    
    tif = rasterio_open(file_bytes)
    return tif

def load_tif_data(gcs_tiff_path):
    """loads data present in the tiff"""
    tif = load_tiff(gcs_tiff_path)

    return tif.data

def files_in_dir(bucket_path, file_extension):
    """ lists all the files present at the given path"""
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

def upload_str_to_gcs(output_path, file):
    """ uploads blob string to gcs bucket"""
    client = get_storage_client()
    bucket_name, file_path = get_bucket_name(output_path)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    blob.upload_from_string(file.getvalue(), content_type='text/csv')
    client.close()

def upload_to_gcs(output_path, file):
    """ uploads any file to gcs bucket"""
    client = get_storage_client()
    bucket_name, file_path = get_bucket_name(output_path)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    blob.upload_from_file(BytesIO(file), content_type="image/tiff")
    client.close() 

def write_tiff(out_path: str, tiff_bytes):
    """ saves a tiff file in gcs bucket or locally"""

    if out_path.startswith('gs://'):
        logging.info("uploading to gcs bucket")
        upload_to_gcs(out_path, tiff_bytes)
    else:
        
        with open(out_path, "wb") as file:
            file.write(tiff_bytes)
    logging.info(f"uploaded to {out_path}")

def export_tiff(ouput_path, tgt_profile, data, band_names):
    """creates and saves a tiff file"""

    tgt_profile['count'] = len(band_names)
    tgt_profile['driver'] = "COG"
    with MemoryFile() as memfile:
        with memfile.open(**tgt_profile) as dataset:
            dataset.write(data, 1)  # Write the array to the first band
            for i, band in enumerate(band_names, start=1):
                dataset.set_band_description(i, band)
        # Get the in-memory file as bytes
        tiff_bytes = memfile.read()
        write_tiff(ouput_path, tiff_bytes)
    return 

def export_csv(df, output_path, index=False):
    """saves a dataframe as csv on gcs or locally"""
    if output_path.startswith('gs://'):
        logging.info("uploading to gcs bucket")
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        upload_str_to_gcs(output_path, csv_buffer)
    else:
        df.to_csv(output_path, index=index)
    logging.info(f"uploaded to {output_path}")
    return 