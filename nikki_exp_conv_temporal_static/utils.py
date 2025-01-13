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
    # instantiates a bucket object owned by this client

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


















   

    



def pre_process(train_features, train_labels,test_features,test_labels, block_coverage, total_blocks,test_size):

    train_labels=np.where(train_labels==-1, np.nan, train_labels)
    test_labels=np.where(test_labels==-1, np.nan,test_labels)
    train_axis_pad=padding(train_features,train_labels)
    test_axis_pad=padding(test_features,test_labels)
    train_features=np.pad(train_features, ((0,0),(0,train_axis_pad[1]),(0,train_axis_pad[2])),mode='constant',constant_values=np.nan)
    # print("after padding",train_features)
    test_features=np.pad(test_features,((0,0),(0,test_axis_pad[1]),(0,test_axis_pad[2])),mode='constant',constant_values=np.nan)
    train_stacked=np.concatenate((train_labels,train_features),axis=0)
    test_stacked=np.concatenate((test_labels,test_features),axis=0)
    train_valid_mask=~np.isnan(train_stacked).any(axis=0)
    test_valid_mask=~np.isnan(test_stacked).any(axis=0)
    train_stacked=np.where(train_valid_mask,train_stacked,np.nan)
    test_data=np.where(test_valid_mask,test_stacked,np.nan)
    height, width = train_stacked.shape[1], train_stacked.shape[2]
    windows=window(block_coverage,total_blocks,height,width)
    train_windows, val_windows = train_test_split(windows, test_size=test_size, random_state=42)
    train_final_data,train_final_label= get_sampled_spatial_convolve_data(train_stacked, train_windows)

    val_final_data,val_final_label = get_sampled_spatial_convolve_data(train_stacked, val_windows)
    train_final_data,train_final_label=np.array(train_final_data), np.array(train_final_label)
    val_final_data,val_final_label=np.array(val_final_data), np.array(val_final_label)
    print(train_final_data.shape, train_final_label.shape)
    print(val_final_data.shape, val_final_label.shape)

    # train_data,train_final_data= get_sampled_spatial_temporal_convolve_data(train_stacked, train_windows)

    # val_data,val_final_data = get_sampled_spatial_temporal_convolve_data(train_stacked, val_windows)
    # print(train_final_data.shape)
    # print(val_final_data.shape)
    # train_final_data=np.array(train_final_data)
    # val_final_data=np.array(val_final_data)
    # print(train_final_data.shape)
    # print(val_final_data.shape)
    nan_train_feat = ~np.any(np.isnan(train_final_data),axis=1)
    nan_val_feat=~np.any(np.isnan(val_final_data),axis=1) 
    train_feat_=train_final_data[nan_train_feat]
    val_feat_=val_final_data[nan_val_feat]
    train_label_=train_final_label[nan_train_feat]
    val_label_=val_final_label[nan_val_feat]
    # train_feat_=train_final_data[:,1:]
    # train_label_=train_final_data[:,0]
    # val_feat_=val_final_data[:,1:]
    # val_label_=val_final_data[:,0]
    # print(train_feat_.shape)
    # print(train_label_.shape)
    # print(val_feat_.shape)
    # print(val_label_.shape)


    # train_feat =train_data[1:,:,:]
    # train_label=train_data[0,:,:]
    # val_feat=val_data[1:,:,:]
    # val_label=val_data[0,:,:]
    test_feat=test_data[1:,:,:]
    test_label=test_data[0,:,:]
    test_feat=test_feat[:,test_valid_mask].transpose()
    test_label=test_label[test_valid_mask]


    return train_feat_,train_label_,val_feat_,val_label_,test_feat,test_label,test_valid_mask

    # return x_train, y_train,x_val,y_val,x_test, y_test,test_label_mask,train_feat_, val_feat_, train_label_,val_label_
def get_sampled_spatial_convolve_data(data,windows):
    new_data=[]
    new_label=[]
    # 4 window size
    # data=np.pad(data,((0,0),(4,4),(4,4)),mode='constant',constant_values=np.nan)
    for window in tqdm(windows):
        row_start = int(window.row_off)
        row_stop = int(window.row_off + window.height)
        col_start = int(window.col_off)
        col_stop = int(window.col_off + window.width)
        # row_start=max(row_start,4)
        # col_start=max(col_start,4) 
        for i in range(row_start+2,row_stop-2):
            for j in range(col_start+2, col_stop-2):
                    temp_data=data[1:,i-2:i+3,j-2:j+3]
                    print(temp_data)
                    # print(temp_data)
                    # temp_data=np.where(temp_data==np.nan,0,temp_data)
                    # print(temp_data)
                    # print(temp_data.mean(axis=(1,2)))
                    print(np.nanmean(temp_data,axis=(1,2)))
                    print(data[0,i,j])
                    new_data.append(np.nanmean(temp_data,axis=(1,2)))
                    new_label.append(data[0,i,j])
                    
                # if ~np.isnan(data[0,i,j]):
                    
                    

                # else:
                    
                #     print("nan value",data[:,i,j])
        # if data[0,row_start,col_start]!=np.nan:
        #             new_data.append(data[:,row_start:row_stop,col_start:col_stop].mean(axis=(1,2)))
    return new_data,new_label
def get_sampled_spatial_temporal_convolve_data(data,windows):

    new_data=[]
    for window in tqdm(windows):
        row_start = int(window.row_off)
        row_stop = int(window.row_off + window.height)
        col_start = int(window.col_off)
        col_stop = int(window.col_off + window.width)
        for i in range(row_start+2,row_stop-2):
            for j in range(col_start+2, col_stop-2):
                    temp_data=data[:,i-2:i+2,j-2:j+2]

                    print(temp_data)
                    # print(temp_data)
                    # temp_data=np.where(temp_data==np.nan,0,temp_data)
                    # print(temp_data)
                    # print(temp_data.mean(axis=(1,2)))
                    new_data.append(np.nanmean(temp_data,axis=(0,1,2)))
       
        # if data[0,row_start,col_start]!=np.nan:
        #         new_data.append(data[:,row_start:row_stop,col_start:col_stop].mean(axis=(0,1,2)))
    return new_data





