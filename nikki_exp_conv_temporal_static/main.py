import rasterio
import numpy as np
from rasterio.windows import Window
from sklearn.model_selection import train_test_split
from tqdm import tqdm as tqdm
from sklearn.metrics import classification_report, confusion_matrix

PROJECT_ID = "ai-sandbox-399505"




def ndarray_tiff(data, src_profile, output_file):
    src_profile.update(
        dtype=rasterio.int32,  # Adjust the data type if needed
        count=1,  # Number of bands
        # compress='lzw'  # Optional: Add compression
    )

    
    with rasterio.open(output_file, 'w', src_profile) as dst:
        dst.write(data, 1)  # Write

def padding(features,labels):
    axis_padwidth={}
    for i in range(1,len(features.shape)):
        if(features.shape[i]<labels.shape[i]):
            axis_padwidth[i]=labels.shape[i]-features.shape[i]
          
        else:
            axis_padwidth[i]=0


    return axis_padwidth



def window(block_coverage, total_blocks, height, width):
    total_pixels = height*width
    pixels_covered = total_pixels*block_coverage
    block_size = int(np.sqrt(pixels_covered/total_blocks))
    print("block size",block_size)

    windows = []
    for i in range(0, height-block_size+1, block_size):
        for j in range(0, width-block_size+1, block_size):
            windows.append(Window(j, i, block_size, block_size))
    return windows


def get_sampled_data(data, windows):
    
    new_data=[]
    nan_indices=np.argwhere(np.isnan(data))

    for window in tqdm(windows):
        row_start = int(window.row_off)
        row_stop = int(window.row_off + window.height)
        col_start = int(window.col_off)
        col_stop = int(window.col_off + window.width)
        for i in range(row_start,row_stop):
            for j in range(col_start, col_stop):
                if [0,i,j] not in nan_indices:
                 
                    new_data.append(data[:,i,j])

                
    return new_data




def get_sampled_test(test_data):
    new_data=[]
    new_label=[]
   
    for i in tqdm(range(2,test_data.shape[1]-2)):
        for j in range(2,test_data.shape[2]-2):
            mean_data=np.concatenate((test_data[1:7,i-2:i+3,j-2:j+3], test_data[8:9,i-2:i+3,j-2:j+3]),axis=0)
            static_data=test_data[1:,i,j]
            
            new_data.append(np.concatenate(((np.nanmean(mean_data,axis=(1,2))),static_data),axis=0 ))
            new_label.append(test_data[0,i,j])
    return new_data, new_label



def get_sampled_spatial_convolve_data(data,windows):
    new_data=[]
    new_label=[]
    
    for window in tqdm(windows):
        row_start = int(window.row_off)
        row_stop = int(window.row_off + window.height)
        col_start = int(window.col_off)
        col_stop = int(window.col_off + window.width)
       
        for i in range(row_start+2,row_stop-2):
            for j in range(col_start+2, col_stop-2):
                    mean_data=np.concatenate((data[1:7,i-2:i+3,j-2:j+3], data[8:9,i-2:i+3,j-2:j+3]),axis=0)
                    static_data=data[1:,i,j]
            new_data.append(np.concatenate(((np.nanmean(mean_data,axis=(1,2))),static_data),axis=0 ))
            new_label.append(data[0,i,j])
               
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
                
                    new_data.append(np.nanmean(temp_data,axis=(0,1,2)))
       
    return new_data



def save_prediction(test_labels, filter_size,pred_label_mask,test_pred,output_path):

    test_profile=test_labels.profile 
    shape=(test_labels.metadata["height"]-filter_size+1,test_labels.metadata["width"]-filter_size+1)
    valid_pred_mask=pred_label_mask.flatten()
    pred_array=np.full((shape[0]*shape[1]),np.nan)
    pred_array[valid_pred_mask] = test_pred
    pred_array = pred_array.reshape((shape[0], shape[1]))
    with rasterio.open(output_path,"w",driver="GTiff",height=shape[0],width=shape[1],count=1,  dtype=pred_array.dtype,crs=test_profile['crs'],transform=test_profile['transform']) as dst:
        dst.write(pred_array, 1)

def eliminate_nan(data,label):
    label=label.reshape(len(label),1)
    concat=np.concatenate((label,data),axis=1)
    mask=~np.isnan(concat).any(axis=1)
    mask=mask.reshape(-1,1)
    data_final=np.where(mask,concat,np.nan)
    x=data_final[:,1:]
    y=data_final[:,0]
    mask=mask.squeeze()
    x=x[mask,:]
    y=y[mask]
    
    return x,y,mask
    
def pre_process(train_features, train_labels,test_features,test_labels, block_coverage, total_blocks,test_size):

    train_labels=np.where(train_labels==-1, np.nan, train_labels)
    test_labels=np.where(test_labels==-1, np.nan,test_labels)


    train_axis_pad=padding(train_features,train_labels)
    test_axis_pad=padding(test_features,test_labels)

    train_features=np.pad(train_features, ((0,0),(0,train_axis_pad[1]),(0,train_axis_pad[2])),mode='constant',constant_values=np.nan)
    test_features=np.pad(test_features,((0,0),(0,test_axis_pad[1]),(0,test_axis_pad[2])),mode='constant',constant_values=np.nan)

    

    train_stacked=np.concatenate((train_labels,train_features),axis=0)
    test_stacked=np.concatenate((test_labels,test_features),axis=0)

    train_valid_mask=~np.isnan(train_stacked).any(axis=0)
    test_valid_mask=~np.isnan(test_stacked).any(axis=0)


    train_stacked=np.where(train_valid_mask,train_stacked,np.nan)
    test_stacked=np.where(test_valid_mask,test_stacked,np.nan)

    train_height, train_width = train_stacked.shape[1], train_stacked.shape[2]
    tr_windows=window(block_coverage,total_blocks,train_height,train_width)
    train_windows, val_windows = train_test_split(tr_windows, test_size=test_size, random_state=42)

    train_final_data,train_final_label= get_sampled_spatial_convolve_data(train_stacked, train_windows)
    val_final_data,val_final_label = get_sampled_spatial_convolve_data(train_stacked, val_windows)
    test_final_data, test_final_label=get_sampled_test(test_stacked)

    

    
    train_final_data,train_final_label=np.array(train_final_data), np.array(train_final_label)
    val_final_data,val_final_label=np.array(val_final_data), np.array(val_final_label)
    test_final_data,test_final_label=np.array(test_final_data), np.array(test_final_label)

    print(train_final_data.shape, train_final_label.shape)
    print(test_final_data.shape, test_final_label.shape)
    print(val_final_data.shape, val_final_label.shape)
    
    x_train,y_train,train_mask= eliminate_nan(train_final_data, train_final_label)
    x_test,y_test,test_mask= eliminate_nan(test_final_data, test_final_label)
    x_val,y_val,val_mask= eliminate_nan(test_final_data, test_final_label)


    return x_train,y_train,x_test,y_test,x_val,y_val,train_mask, test_mask, val_mask




def train(model,x_train,y_train,x_val,y_val):

    model=model.fit(x_train,y_train,eval_set=[(x_val,y_val)])


def predict(model,x_test,y_test):
    y_pred=model.predict(x_test)
    cm = confusion_matrix(y_test, y_pred, labels=[0,1,2,3])
    report = classification_report(y_test, y_pred, labels=[0,1,2,3])
    return y_pred,cm,report






    
