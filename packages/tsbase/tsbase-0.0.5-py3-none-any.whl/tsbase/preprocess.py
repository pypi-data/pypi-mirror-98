"""
    Data preprocessing
    -----------------------------
    - Author:   zhf026
    - Email:    zhf026@outlook.com
    - Modified: 2020-11-23
"""

import numpy as np
import pandas as pd

MODEL_TYPE_0 = ['keras', 'LSTM', 'GRU', 'CNN', 'Ensemble', 'Stacking', 'Blending']
MODEL_TYPE_1 = ['LightGBM', 'lightgbm', 'lgb']
MODEL_TYPE_2 = ['sklearn', 'XGBoost', 'xgboost', 'xgb']


def load_from_csv(path, index_col, encoding, features, target_name=None):
    # Read data from .csv file
    df = pd.read_csv(path, index_col=0, encoding=encoding)
    col_names = list(df.columns)
    for k in range(len(col_names)):
        if col_names[k] not in features:
            df = df.drop(col_names[k], axis=1)
    dropped_col_names = list(df.columns)

    # DataFrame to numpy array
    dat_array = df.values  # dtype=float64
    dat = np.zeros(dat_array.shape, dtype='float32')
    dat[:, :] = dat_array[:, :]

    # Get the target f index
    if isinstance(target_name, list):
        target_f_indices = list()
        for m in range(len(target_name)):
            for k in range(len(dropped_col_names)):
                if dropped_col_names[k] == target_name[m]:
                    target_f_indices.append(k)
        return dat, target_f_indices
    elif isinstance(target_name, str):
        target_f_index = None
        for k in range(len(dropped_col_names)):
            if dropped_col_names[k] == target_name:
                target_f_index = k
        return dat, target_f_index


def split_dataset(data, train_rate=None, train_num=None):
    """
    Split data set into training set data and test set data
    Args:
        data (array_like):           Input data, default=None
        train_rate (float):          Rate of training set data
        train_num (int):             Quantity of training set data
    Returns:
        training_set (array_like):   Training set data
        test_set (array_like):       Test set data
    """

    index = None
    if train_rate is not None:
        index = int(len(data) * train_rate)
    elif train_num is not None:
        index = train_num
    else:
        print('Error in split dataset function.')
    training_set = np.copy(data[0:index, :])
    test_set = np.copy(data[index:, :])

    return training_set, test_set


def standardize(data, train_rate=None, train_num=None):
    """
    Standardize the training set data ans test set data
    Args:
        data (array_like):           Input data, default=None
        train_rate (float):          Rate of training set data
        train_num (int):             Quantity of training set data
    Returns:
        training_set (array_like):   standardized  training set data
        test_set (array_like):       Standardized  test set data
        _mean (array_like):          Mean of training set data
        _std (array_like):           Standard deviation of training set data
    """

    training_set, test_set = split_dataset(data, train_rate, train_num)
    # Standardize training set data
    _mean = np.mean(training_set, axis=0)
    training_set -= _mean
    _std = np.std(training_set, axis=0)
    training_set /= _std
    # Standardize test set data
    test_set -= _mean
    test_set /= _std

    return training_set, test_set, (_mean, _std)


def normalize(data, train_rate=None, train_num=None):
    """
    Min-Max Normalization
    Args:
        data (array_like):           Input data, default=None
        train_rate (float):          Rate of training set data
        train_num (int):             Quantity of training set data
    Returns:
        training_set (array_like):   Normalized  training set data
        test_set (array_like):       Normalized  test set data
        min_value (array_like):      Minimum values of training set data
        max_value (array_like):      Maximum values of training set data
    """

    training_set, test_set = split_dataset(data, train_rate, train_num)

    min_value = np.min(training_set, axis=0)
    max_value = np.max(training_set, axis=0)
    training_set = (training_set - min_value) / (max_value - min_value)
    test_set = (test_set - min_value) / (max_value - min_value)

    return training_set, test_set, (min_value, max_value)


def form_samples(data, lookback, delay, span=1, target_index=None):
    """
    Args:
        data (array_like):   Input data
        lookback (int):      Number of history points used
        delay (int):         Number of the future points forecasted
        span (int):          Span of adjacent samples
        target_index (int):  Index of target forecasted
    Returns:
        X (array_like):      Samples, (batch, time step, feature)
        y (array_like):      Real target value, (batch, )
    """

    X, y = list(), list()
    # Starting index of input sequences
    input_st_index = 0
    for k in range(len(data)):
        # Ending index of input sequences
        input_end_index = input_st_index + lookback
        # Ending index of output sequences
        output_end_index = input_end_index + delay
        if output_end_index <= len(data):
            X.append(data[input_st_index:input_end_index, :])
            y.append(data[input_end_index:output_end_index, target_index])
            # Inc span
            input_st_index += span
    X, y = np.array(X), np.array(y)
    return X, y


def form_samples_mul_out(data, lookback, delay, span=1, target_index=None):
    X = list()
    y = [list() for k in range(len(target_index))]
    # Starting index of input sequences
    input_st_index = 0
    for k in range(len(data)):
        # Ending index of input sequences
        input_end_index = input_st_index + lookback
        # Ending index of output sequences
        output_end_index = input_end_index + delay
        if output_end_index <= len(data):
            X.append(data[input_st_index:input_end_index, :])
            for m in range(len(y)):
                y[m].append(data[input_end_index:output_end_index, target_index[m]])
            # Inc span
            input_st_index += span
    X, y = np.array(X), np.array(y)

    return X, y


def hold_out_val(tr_x, tr_y, v_rate=None, v_num=None):
    index = None
    if v_rate is not None:
        index = int(len(tr_x) * (1 - v_rate))
    elif v_num is not None:
        index = len(tr_x) - v_num
    # Train set
    p_tr_x = tr_x[0:index, :, :]
    p_tr_y = tr_y[0:index, :]
    # Validation set
    v_x = tr_x[index:, :, :]
    v_y = tr_y[index:, :]

    return (p_tr_x, p_tr_y), (v_x, v_y)


def processing(file_path=None, index_col=0, encoding=None,
               target_name=None,
               features=None, lookback=None, delay=None, span=1,
               pre_deal=None, train_rate=None, train_num=None,
               is_hold_out=False, v_rate=None, v_num=None,
               model_type=None,
               ):
    """
    Data preprocessing. Default to load data from .csv file with specific format,
    and you can also directly input array data by using parameters of 'data' and 'obj_index'
    Args:
        file_path (str):            Path of input file
        index_col (int):            Index of column in ,csv files
        encoding (str):
        target_name (str):          Name of target feature
        features (list or 'all')    List of name of features or 'all'
        lookback (int):             Number of history points used
        delay (int):                Number of the future points forecasted
        span (int):                 Span of adjacent samples, default=1
        pre_deal (str):             Standardize or normalize, value: 'std' or 'min_max'
        train_rate (float):         Rate of training set data, default=None
        train_num (int):            Quantity of training set data, default=None
        is_hold_out (bool):         Whether to hold out
        v_rate (float):             Rate of validation set data, default=None
        v_num (int):                Quantity of validation set data, default=None
        model_type (str):           Type of model
    Returns:
        tr_x (array_like):          X ot training set
        tr_y (array_like):          y ot training set
        te_x (array_like):          X ot test set
        te_y (array_like):          y ot test set
        v_x (array_like):           X ot validation set
        v_y (array_like):           y of validation set
        pre_a (array_like):         Mean/Minimum values of training set
        pre_b (array_like):         Standard deviation/Maximum values of training set
    """

    # Load data from .csv files
    _data, target_index = load_from_csv(path=file_path, index_col=index_col, encoding=encoding,
                                        features=features, target_name=target_name)

    # Standardize or normalize
    training_set, test_set, (pre_a, pre_b) = None, None, (None, None)
    if pre_deal == 'std':
        training_set, test_set, (pre_a, pre_b) = standardize(_data, train_rate, train_num)
    elif pre_deal == 'min_max':
        training_set, test_set, (pre_a, pre_b) = normalize(_data, train_rate, train_num)
    else:
        print('Please input correct parameter, e.g. [std] or [min_max].')

    # 由于逐点预测，补充训练集后lookback点数据至测试集
    index = None
    if train_rate is not None:
        index = int(len(_data) * train_rate)
    if train_num is not None:
        index = train_num
    test_set = np.concatenate([training_set[index - lookback:, :], test_set], axis=0)

    # Form the samples
    tr_x, tr_y = form_samples(training_set, lookback, delay, span=span,
                              target_index=target_index)
    te_x, te_y = form_samples(test_set, lookback, delay, span=span,
                              target_index=target_index)

    # Print info
    print('-' * 88)
    print('Time sequences preprocessing')
    print('- File path:      {} \n '
          '- Features:       {} \n '
          '- Target feature: {} \n'
          '- Target index:   {} \n'
          '- Lookback:       {} \n'
          '- Delay:          {} \n'
          '- Pre_deal:       {} \n'
          '- Train rate:     {} \n'
          '- Train num:      {} \n'
          '- Is hold out:    {} \n'
          '- Model type:     {} \n'
          '- Mean/Min:       {} \n'
          '- Std/Max:        {}'
          .format(file_path, features, target_name, target_index,
                  lookback, delay, pre_deal, train_rate, train_num,
                  is_hold_out, model_type, pre_a[target_index], pre_b[target_index]))

    if is_hold_out:
        # Hold out
        (p_tr_x, p_tr_y), (v_x, v_y) = hold_out_val(tr_x=tr_x, tr_y=tr_y, v_rate=v_rate, v_num=v_num)
        if model_type in MODEL_TYPE_0:
            pass
        elif model_type in MODEL_TYPE_1:
            # 3-D to 2-D
            p_tr_x = p_tr_x.reshape(p_tr_x.shape[0], p_tr_x.shape[1] * p_tr_x.shape[2])
            v_x = v_x.reshape(v_x.shape[0], v_x.shape[1] * v_x.shape[2])
            te_x = te_x.reshape(te_x.shape[0], te_x.shape[1] * te_x.shape[2])
            # 2-D to 1-D
            p_tr_y = p_tr_y.reshape(p_tr_y.shape[0])
            v_y = v_y.reshape(v_y.shape[0])
            te_y = te_y.reshape(te_y.shape[0])
        elif model_type in MODEL_TYPE_2:
            # 3-D to 2-D
            p_tr_x = p_tr_x.reshape(p_tr_x.shape[0], p_tr_x.shape[1] * p_tr_x.shape[2])
            v_x = v_x.reshape(v_x.shape[0], v_x.shape[1] * v_x.shape[2])
            te_x = te_x.reshape(te_x.shape[0], te_x.shape[1] * te_x.shape[2])
        else:
            print('Please input correct parameter of model_type.')

        print(' - Shape of training set:   {}/{}'.format(p_tr_x.shape, p_tr_y.shape))
        print(' - Shape of validation set: {}/{}'.format(v_x.shape, v_y.shape))
        print(' - Shape of test set:       {}/{}'.format(te_x.shape, te_y.shape))
        print('-' * 88)

        return (p_tr_x, p_tr_y), (v_x, v_y), (te_x, te_y), (pre_a[target_index], pre_b[target_index])
    else:
        if model_type in MODEL_TYPE_0:
            pass
        elif model_type in MODEL_TYPE_1:
            # 3-D to 2-D
            tr_x = tr_x.reshape(tr_x.shape[0], tr_x.shape[1] * tr_x.shape[2])
            te_x = te_x.reshape(te_x.shape[0], te_x.shape[1] * te_x.shape[2])
            # 2-D to 1-D
            tr_y = tr_y.reshape(tr_y.shape[0])
            te_y = te_y.reshape(te_y.shape[0])
        elif model_type in MODEL_TYPE_2:
            # 3-D to 2-D
            tr_x = tr_x.reshape(tr_x.shape[0], tr_x.shape[1] * tr_x.shape[2])
            te_x = te_x.reshape(te_x.shape[0], te_x.shape[1] * te_x.shape[2])
        else:
            print('Please input correct parameter of model_type.')

        print(' - Shape of training set: {}/{}'.format(tr_x.shape, tr_y.shape))
        print(' - Shape of test set:     {}/{}'.format(te_x.shape, te_y.shape))
        print('-' * 88)

        return (tr_x, tr_y), (te_x, te_y), (pre_a[target_index], pre_b[target_index])
