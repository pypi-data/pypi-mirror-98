from typing import Generator

import numpy as np
import pytest

from dkist_processing_common.libraries import math

rng = np.random.default_rng()


@pytest.fixture()
def numpy_arrays_wrong_shape():
    arrays = [rng.standard_normal((10, 10)), rng.standard_normal((10, 15))]
    return arrays


@pytest.fixture()
def numpy_arrays():
    arrays = [rng.standard_normal((10, 10)), rng.standard_normal((10, 10))]
    return arrays


@pytest.fixture()
def numpy_array():
    array = rng.standard_normal((10, 10))
    return array


@pytest.fixture(params=["multiple", "single"])
def multiple_arrays(request, numpy_arrays):
    if request.param == "multiple":
        return numpy_arrays
    else:
        return numpy_arrays[0]


def test_multiple_arrays_wrong_shape(numpy_arrays_wrong_shape, numpy_array):
    """
    Given: an iterable of numpy arrays that are not all the same shape
    When: averaging, subtracting or dividing arrays
    Then: an error is raised as the shapes are required to be the same
    """
    with pytest.raises(ValueError):
        math.average_numpy_arrays(numpy_arrays_wrong_shape)
    with pytest.raises(ValueError):
        list(math.subtract_array_from_arrays(numpy_arrays_wrong_shape, numpy_array))
    with pytest.raises(ValueError):
        list(math.divide_arrays_by_array(numpy_arrays_wrong_shape, numpy_array))


def test_average_numpy_arrays(multiple_arrays):
    """
    Given: an iterable of numpy arrays that are all the same shape
    When: calculating the average
    Then: a numpy array containing the average is returned
    """
    if isinstance(multiple_arrays, np.ndarray):
        multiple_arrays = [multiple_arrays]
    result = math.average_numpy_arrays(multiple_arrays)
    assert isinstance(result, np.ndarray)
    # Dividing an ndarray by an integer is a floating point division
    # and the result is always dtype=np.float64
    assert result.dtype == np.float64
    assert result.shape == np.shape(multiple_arrays[0])
    np.testing.assert_allclose(result, np.mean(multiple_arrays, axis=0))


def test_average_numpy_arrays_empty_list(empty_list=[]):
    """
    Given: an empty iterable of numpy arrays
    When: calculating the average
    Then: an error is raised
    """
    with pytest.raises(ValueError):
        math.average_numpy_arrays(empty_list)


def test_subtract_array_from_arrays(multiple_arrays, numpy_array):
    """
    Given: an iterable of numpy arrays that are all the same shape
    When: subtracting a fixed array from each array in the iterable
    Then: an Generator of subtracted arrays is returned
    """
    if isinstance(multiple_arrays, np.ndarray):
        multiple_arrays = [multiple_arrays]
    result = math.subtract_array_from_arrays(multiple_arrays, numpy_array)
    assert isinstance(result, Generator)
    for result_array, test_array in zip(result, multiple_arrays):
        test_result = test_array - numpy_array
        assert result_array.shape == np.shape(multiple_arrays[0])
        assert result_array.dtype == np.result_type(test_result)
        np.testing.assert_allclose(result_array, test_result)


def test_divide_arrays_by_array(multiple_arrays, numpy_array):
    """
    Given: an iterable of numpy arrays that are all the same shape
    When: dividing each array in the iterable by a fixed array
    Then: an Generator of divided arrays is returned
    """
    if isinstance(multiple_arrays, np.ndarray):
        multiple_arrays = [multiple_arrays]
    result = math.divide_arrays_by_array(multiple_arrays, numpy_array)
    assert isinstance(result, Generator)
    for result_array, test_array in zip(result, multiple_arrays):
        test_result = test_array / numpy_array
        assert result_array.shape == np.shape(multiple_arrays[0])
        assert result_array.dtype == np.float64
        np.testing.assert_allclose(result_array, test_result)
