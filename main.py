import numpy as np
import rasterio
from rasterio.windows import Window
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score)
from sklearn.model_selection import GridSearchCV, train_test_split
from tqdm import tqdm as tqdm


def ndarray_tiff(data, src_profile, output_file):
    src_profile.update(
        dtype=rasterio.int32,  # Adjust the data type if needed
        count=1,  # Number of bands
        # compress='lzw'  # Optional: Add compression
    )

    with rasterio.open(output_file, 'w', src_profile) as dst:
        dst.write(data, 1)  # Write


def padding(features, labels):
    axis_padwidth = {}
    for i in range(1, len(features.shape)):
        if (features.shape[i] < labels.shape[i]):
            axis_padwidth[i] = labels.shape[i] - features.shape[i]

        else:
            axis_padwidth[i] = 0

    return axis_padwidth


def window(block_coverage, total_blocks, height, width):
    total_pixels = height * width
    pixels_covered = total_pixels * block_coverage
    block_size = int(np.sqrt(pixels_covered / total_blocks))
    windows = []
    for i in range(0, height - block_size + 1, block_size):
        for j in range(0, width - block_size + 1, block_size):
            windows.append(Window(j, i, block_size, block_size))
    return windows


def get_sampled_data(data, windows):

    new_data = np.full(data.shape, np.nan, data.dtype)
    for window in windows:
        row_start = int(window.row_off)
        row_stop = int(window.row_off + window.height)
        col_start = int(window.col_off)
        col_stop = int(window.col_off + window.width)
        new_data[:, row_start:row_stop,
                 col_start:col_stop] = data[:, row_start:row_stop,
                                            col_start:col_stop].copy()

    return new_data


def get_sampled_test(test_data):
    new_data = []
    new_label = []

    for i in tqdm(range(2, test_data.shape[1] - 2)):
        for j in range(2, test_data.shape[2] - 2):
            mean_data = np.concatenate(
                (test_data[1:7, i - 2:i + 3, j - 2:j + 3],
                 test_data[8:9, i - 2:i + 3, j - 2:j + 3]),
                axis=0)
            static_data = test_data[1:, i, j]

            new_data.append(
                np.concatenate(
                    ((np.nanmean(mean_data, axis=(1, 2))), static_data),
                    axis=0))
            new_label.append(test_data[0, i, j])
    return new_data, new_label


def get_sampled_spatial_convolve_data(data, windows):
    new_data = []
    new_label = []

    for window in tqdm(windows):
        row_start = int(window.row_off)
        row_stop = int(window.row_off + window.height)
        col_start = int(window.col_off)
        col_stop = int(window.col_off + window.width)

        for i in range(row_start + 2, row_stop - 2):
            for j in range(col_start + 2, col_stop - 2):
                mean_data = np.concatenate(
                    (data[1:7, i - 2:i + 3,
                          j - 2:j + 3], data[8:9, i - 2:i + 3, j - 2:j + 3]),
                    axis=0)
                static_data = data[1:, i, j]
            new_data.append(
                np.concatenate(
                    ((np.nanmean(mean_data, axis=(1, 2))), static_data),
                    axis=0))
            new_label.append(data[0, i, j])

    return new_data, new_label


def get_sampled_spatial_temporal_convolve_data(data, windows):

    new_data = []
    for window in tqdm(windows):
        row_start = int(window.row_off)
        row_stop = int(window.row_off + window.height)
        col_start = int(window.col_off)
        col_stop = int(window.col_off + window.width)
        for i in range(row_start + 2, row_stop - 2):
            for j in range(col_start + 2, col_stop - 2):
                temp_data = data[:, i - 2:i + 2, j - 2:j + 2]
                new_data.append(np.nanmean(temp_data, axis=(0, 1, 2)))

    return new_data


def save_prediction(test_labels, filter_size, pred_label_mask, test_pred,
                    output_path):

    test_profile = test_labels.profile
    shape = (test_labels.metadata["height"] - filter_size + 1,
             test_labels.metadata["width"] - filter_size + 1)
    valid_pred_mask = pred_label_mask.flatten()
    pred_array = np.full((shape[0] * shape[1]), np.nan)
    pred_array[valid_pred_mask] = test_pred
    pred_array = pred_array.reshape((shape[0], shape[1]))
    with rasterio.open(output_path,
                       "w",
                       driver="GTiff",
                       height=shape[0],
                       width=shape[1],
                       count=1,
                       dtype=pred_array.dtype,
                       crs=test_profile['crs'],
                       transform=test_profile['transform']) as dst:
        dst.write(pred_array, 1)
    return pred_array


def eliminate_nan(data, label):
    label = label.reshape(len(label), 1)
    concat = np.concatenate((label, data), axis=1)
    mask = ~np.isnan(concat).any(axis=1)
    mask = mask.reshape(-1, 1)
    data_final = np.where(mask, concat, np.nan)
    x = data_final[:, 1:]
    y = data_final[:, 0]
    mask = mask.squeeze()
    x = x[mask, :]
    y = y[mask]

    return x, y, mask


def multiclass_temoral_class_weights(targets):
    count_all = len(targets)
    s_weights = {0: 0, 1: 0, 2: 0, 3: 0}
    for i in targets:
        s_weights[i] += 1
    for key, _ in s_weights.items():
        s_weights[key] = count_all / s_weights[key]
    return s_weights


def train(model, x_train, y_train, x_val, y_val, cat_index_list):

    model = model.fit(x_train,
                      y_train,
                      eval_set=[(x_val, y_val)],
                      categorical_feature=cat_index_list)
    return model


def return_indexes(list_paths, year):

    for i, feat in enumerate(list_paths):
        if str(year) + '-01-01' in feat:
            index = i
    return index


def train_test_index_pair(test_year):
    prediction_years_list = [
        2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022,
        2023, 2024
    ]
    index = prediction_years_list.index(test_year)
    train_test_pairs = [(5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11),
                        (11, 12), (12, 13), (13, 14), (14, 15), (15, 16),
                        (16, 17), (17, 18), (18, 19)]

    return train_test_pairs[index]


def hyper_parameter_train(model, x_train, y_train, x_val, y_val,
                          cat_index_list):
    param_grid = {
        'num_leaves': [100, 150],  # Number of leaves in a tree
        'learning_rate': [0.1, 0.3],  # Learning rate
        'min_child_weight': [0.001, 0.01],
        'min_child_samples': [30, 40],
        'tree_learner': ['voting'],
        'max_depth': [10, 20, 30],  # Maximum depth of trees
        'early_stopping_round': [5]
        # 'subsample': [0.6, 0.8, 1.0],  # Fraction of samples to use for each tree
        # 'colsample_bytree': [0.6, 0.8, 1.0],  # Fraction of features to use for each tree
    }

    # model = lgbm.LGBMClassifier(objective="multiclass", num_class=4, class_weight=s_weights)
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring=
        'roc_auc_ovr',  # Use 'accuracy' for classification or 'neg_mean_squared_error' for regression
        # Cross-validation folds
        # verbose=1,  # Show progress
    )

    grid_search.fit(x_train,
                    y_train,
                    eval_set=[(x_val, y_val)],
                    categorical_feature=cat_index_list)

    best_model = grid_search.best_estimator_

    best_params = grid_search.best_params_
    print("Best hyperparameters found: ", best_params)  # Use all CPUs
    return best_model


def predict(model, x_test, y_test):
    y_pred = model.predict(x_test)
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1, 2, 3])
    report = classification_report(y_test, y_pred, labels=[0, 1, 2, 3])
    y_pred_proba = model.predict_proba(x_test)
    auc_roc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr')
    return y_pred, cm, report, auc_roc


def pre_process(train_features, train_labels, test_features, test_labels,
                block_coverage, total_blocks, test_size):

    train_labels = np.where(train_labels == -1, np.nan, train_labels)
    test_labels = np.where(test_labels == -1, np.nan, test_labels)
    train_stacked = np.concatenate((train_labels, train_features), axis=0)
    test_stacked = np.concatenate((test_labels, test_features), axis=0)
    train_valid_mask = ~np.isnan(train_stacked).any(axis=0)
    test_valid_mask = ~np.isnan(test_stacked).any(axis=0)
    train_stacked = np.where(train_valid_mask, train_stacked, np.nan)
    test_data = np.where(test_valid_mask, test_stacked, np.nan)

    pred_feat = test_data[1:, :, :]
    pred_label = test_data[0, :, :]

    nan_pred_feat = np.any(np.isnan(pred_feat), axis=0)
    nan_pred_label = np.isnan(pred_label)

    pred_label_mask = ~nan_pred_label
    pred_feat_mask = ~nan_pred_feat

    masked_test_labels = pred_label[pred_label_mask]
    masked_test_feat = pred_feat[:, pred_feat_mask]

    height, width = train_stacked.shape[1], train_stacked.shape[2]
    windows = window(block_coverage, total_blocks, height, width)
    train_windows, val_windows = train_test_split(windows,
                                                  test_size=test_size,
                                                  random_state=42)
    train_data = get_sampled_data(train_stacked, train_windows)
    val_data = get_sampled_data(train_stacked, val_windows)

    train_feat = train_data[1:, :, :]
    train_label = train_data[0, :, :]
    val_feat = val_data[1:, :, :]
    val_label = val_data[0, :, :]

    nan_train_feat = np.any(np.isnan(train_feat), axis=0)
    nan_train_label = np.isnan(train_label)
    nan_val_feat = np.any(np.isnan(val_feat), axis=0)
    nan_val_label = np.isnan(val_label)

    train_label_mask = ~nan_train_label
    train_feat_mask = ~nan_train_feat

    val_label_mask = ~nan_val_label
    val_feat_mask = ~nan_val_feat

    masked_train_labels = train_label[train_label_mask]
    masked_train_feat = train_feat[:, train_feat_mask]

    masked_val_labels = val_label[val_label_mask]
    masked_val_feat_data = val_feat[:, val_feat_mask]

    x_train = masked_train_feat.transpose()
    y_train = masked_train_labels

    x_val = masked_val_feat_data.transpose()
    y_val = masked_val_labels

    x_test = masked_test_feat.transpose()
    y_test = masked_test_labels

    return x_train, y_train, x_val, y_val, x_test, y_test, pred_label_mask