import numpy as np
import yaml

import custom_features as custom
import main
import utils

with open('config.yaml') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

if cfg["task"] == 1:
    dict_task_bucket_path = cfg["bucket_paths_next_year"]
elif cfg["task"] == 5:
    dict_task_bucket_path = cfg["bucket_paths_next_year"]

labels = utils.files_in_dir(dict_task_bucket_path["labels"], "label.tif")
features = utils.files_in_dir(dict_task_bucket_path["features"],
                              "urban_feat.tif")

for train_year in cfg["train_years"]:

    train_index = main.return_indexes(features, train_year)
    if cfg["task"] == 1:
        train_index_prev = train_index - 1
    elif cfg["task"] == 5:
        train_index_prev = train_index - 5

    print(features[train_index], features[train_index_prev],
          labels[train_index], labels[train_index_prev])
    train_prev_labels = utils.load_tiff(labels[train_index_prev])
    train_prev_features = utils.load_tiff(features[train_index_prev])
    train_features = utils.load_tiff(features[train_index])
    train_labels = utils.load_tiff(labels[train_index])
    train_profile = train_features.profile

    train_feature = np.concatenate(
        (train_features.data[:10, :, :], train_features.data[11:, :, :],
         train_prev_labels.data),
        axis=0)
    train_label = train_labels.data

    custom.prepare_save_custom_features(dict_task_bucket_path["customs"],
                                        train_year, train_label,
                                        train_prev_features, train_feature,
                                        train_profile)