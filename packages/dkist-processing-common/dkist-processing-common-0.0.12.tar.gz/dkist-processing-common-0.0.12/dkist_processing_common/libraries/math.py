from typing import Generator
from typing import Iterable
from typing import Union

import numpy as np


def average_numpy_arrays(arrays: Union[Iterable[np.ndarray], np.ndarray]) -> np.ndarray:
    """
    Given an iterable of numpy arrays, calculate the pixel-wise average and return
    it in a numpy array. This will work for a single array as well, just in case...

    Parameters
    ----------
    arrays : Union[Iterable[np.ndarray]
        The arrays to be averaged

    Returns
    -------
    np.ndarray
        The average of the input arrays

    """
    if isinstance(arrays, np.ndarray):
        arrays = [arrays]
    count = 0  # This statement is here only to suppress an uninitialized variable warning
    output = None
    for count, array in enumerate(arrays):
        if output is None:
            output = np.array(array)
        else:
            if array.shape != output.shape:
                raise ValueError(
                    f"All arrays must be the same shape. "
                    f"Shape of initial array = {output.shape} "
                    f"Shape of current array = {array.shape}"
                )
            output += array
    if output is not None:
        return output / (count + 1)
    raise ValueError("data_arrays is empty")


def subtract_array_from_arrays(
    arrays: Union[Iterable[np.ndarray], np.ndarray],
    array_to_subtract: np.ndarray,
) -> Generator[np.ndarray, None, None]:
    """
    Subtract a single array from an iterable of arrays. This will work if
    a single array is used in lieu of an iterable as well.

    Parameters
    ----------
    arrays : Union[Iterable[np.ndarray], np.ndarray]
        The arrays from which to subtract
    array_to_subtract : np.ndarray
        The array to be subtracted

    Returns
    -------
    np.ndarray
        The iterable of modified arrays

    """
    if isinstance(arrays, np.ndarray):
        arrays = [arrays]
    for array in arrays:
        if array.shape != array_to_subtract.shape:
            raise ValueError(
                f"All arrays must be the same shape. "
                f"Shape of subtraction array = {array_to_subtract.shape} "
                f"Shape of current array = {array.shape}"
            )
        yield array - array_to_subtract


def divide_arrays_by_array(
    arrays: Union[Iterable[np.ndarray], np.ndarray],
    array_to_divide_by: np.ndarray,
) -> Generator[np.ndarray, None, None]:
    """
     Divide an iterable of arrays by a single array. This will work if
    a single array is used in lieu of an iterable as well.

    Parameters
    ----------
    arrays : Union[Iterable[np.ndarray], np.ndarray]
        The arrays to be divided
    array_to_divide_by : np.ndarray
        The array ny which to divide

    Returns
    -------
    np.ndarray
        The iterable of modified arrays

    """
    if isinstance(arrays, np.ndarray):
        arrays = [arrays]
    for array in arrays:
        if array.shape != array_to_divide_by.shape:
            raise ValueError(
                f"All arrays must be the same shape. "
                f"Shape of subtraction array = {array_to_divide_by.shape} "
                f"Shape of current array = {array.shape}"
            )
        yield array / array_to_divide_by
