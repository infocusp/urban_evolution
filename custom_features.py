import os

import numpy as np
from tqdm import tqdm as tqdm

import utils


def pop_growth(cus_feature, org_feature, prev_feature):
    pop_growth = org_feature[7, :, :] - prev_feature[7, :, :]
    cus_feature = np.concatenate(
        (cus_feature,
         pop_growth.reshape(1, pop_growth.shape[0], pop_growth.shape[1])),
        axis=0)
    return cus_feature


def merge_urban_pix_dis(filter_1, filter_2, filter_3):
    feature = np.concatenate(
        (filter_1.reshape(1, filter_1.shape[0], filter_1.shape[1]),
         filter_2.reshape(1, filter_1.shape[0], filter_1.shape[1]),
         filter_3.reshape(1, filter_1.shape[0], filter_1.shape[1])),
        axis=0)
    return feature


def return_urbaan_pixel_dis(label, filter_size):

    pad = int(filter_size / 2)
    label_padded = np.pad(label,
                          pad_width=pad,
                          mode='constant',
                          constant_values=-1)
    data_points = []
    for i in tqdm(range(pad, label_padded.shape[0] - pad)):
        for j in range(pad, label_padded.shape[1] - pad):
            count = 0

            temp_data = label_padded[i - pad:i + pad + 1, j - pad:j + pad + 1]

            value_static = label_padded[i, j]
            val, freq = np.unique(temp_data, return_counts=True)
            for k in range(len(freq)):
                if val[k] < value_static and val[k] != -1:
                    count += freq[k]
            data_points.append(count)

    return np.array(data_points).reshape(label.shape[0], label.shape[1])


def surr_urban(label):

    urban_pix_6 = return_urbaan_pixel_dis(label.squeeze(0), 6)
    urban_pix_10 = return_urbaan_pixel_dis(label.squeeze(0), 10)
    urban_pix_20 = return_urbaan_pixel_dis(label.squeeze(0), 20)
    feature = merge_urban_pix_dis(urban_pix_6, urban_pix_10, urban_pix_20)

    return feature


def prepare_save_custom_features(data_dir, train_year, train_label,
                                 train_prev_features, train_feature,
                                 train_profile):

    cus_train_feature = surr_urban(train_label)
    cus_train_feature = pop_growth(cus_train_feature, train_feature,
                                   train_prev_features.data)
    utils.export_tiff(
        os.path.join(data_dir, f'{train_year}-01-01/urban_custom_feat.tif'),
        train_profile, cus_train_feature,
        ["urb_6", "urb_10", "urb_20", "pop_growth"])



      







