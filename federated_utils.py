from typing import List, Tuple, Union

import numpy as np
from preprocessing import prepare_data
from sklearn.linear_model import LogisticRegression

XY = Tuple[np.ndarray, np.ndarray]
Dataset = Tuple[XY, XY]
LogRegParams = Union[XY, Tuple[np.ndarray]]
XYList = List[XY]


def get_model_parameters(model: LogisticRegression) -> LogRegParams:
    """Returns the paramters of a sklearn LogisticRegression model."""
    if model.fit_intercept:
        params = [
            model.coef_,
            model.intercept_,
        ]
    else:
        params = [
            model.coef_,
        ]
    return params


def set_model_params(model: LogisticRegression, params: LogRegParams) -> LogisticRegression:
    """Sets the parameters of a sklearn LogisticRegression model."""
    model.coef_ = params[0]
    if model.fit_intercept:
        model.intercept_ = params[1]
    return model


def set_initial_params(model: LogisticRegression):
    """Sets initial parameters as zeros Required since model params are uninitialized
    until model.fit is called.

    But server asks for initial parameters from clients at launch. Refer to
    sklearn.linear_model.LogisticRegression documentation for more information.
    """
    n_classes = 41  # MNIST has 41 classes
    n_features = 128  # Number of features in dataset
    model.classes_ = np.array([i for i in range(41)])

    model.coef_ = np.zeros((n_classes, n_features))
    if model.fit_intercept:
        model.intercept_ = np.zeros((n_classes,))


def load_disease_dataset() -> Dataset:
    df_train, df_test = prepare_data()

    TARGET_COLUMN = ["prognosis_encoded", "prognosis"]

    y_train = df_train[TARGET_COLUMN[0]].values.flatten()
    y_test = df_test[TARGET_COLUMN[0]].values.flatten()

    x_train = df_train.drop(TARGET_COLUMN, axis=1)
    x_test = df_test.drop(TARGET_COLUMN, axis=1)

    return (x_train, y_train), (x_test, y_test)



def shuffle(X: np.ndarray, y: np.ndarray) -> XY:
    """Shuffle X and y."""
    rng = np.random.default_rng()
    idx = rng.permutation(len(X))
    return X[idx], y[idx]


def partition(X: np.ndarray, y: np.ndarray, num_partitions: int) -> XYList:
    """Split X and y into a number of partitions."""
    return list(zip(np.array_split(X, num_partitions), np.array_split(y, num_partitions)))