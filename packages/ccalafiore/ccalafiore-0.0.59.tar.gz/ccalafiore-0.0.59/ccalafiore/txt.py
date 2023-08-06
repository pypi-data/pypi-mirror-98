import numpy as np
import csv
import os
import glob
from . import array as cc_array
from . import directory as cc_directory
from . import format as cc_format
from . import combinations as cc_combinations


def lines_to_csv_file(lines, directory, headers=None):
    with open(directory, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        if headers is not None:
            writer.writerow(headers)
        writer.writerows(lines)


def array_to_csv_files(array_in, axis_rows, axis_columns, conditions_of_directories, headers=None):

    if axis_rows > axis_columns:
        array = np.swapaxes(array_in, axis_rows, axis_columns)
        axis_rows, axis_columns = axis_columns, axis_rows
    elif axis_rows < axis_columns:
        array = array_in
    else:
        raise ValueError('axis_rows, axis_columns')

    shape_array = np.asarray(array.shape, dtype='i')
    n_axes = shape_array.size
    indexes_array = np.empty(n_axes, dtype='O')
    indexes_array[axis_rows] = slice(0, shape_array[axis_rows], 1)
    indexes_array[axis_columns] = slice(0, shape_array[axis_columns], 1)

    axes_array = np.arange(0, n_axes, 1)
    axes_table = np.asarray([axis_rows, axis_columns], dtype='i')
    axes_files = np.where(np.logical_not(cc_array.samples_in_arr1_are_in_arr2(axes_array, axes_table, axis=0)))[0]

    # for combination_indexes_i, combination_directories_i in cc_combinations.conditions_to_combinations_on_the_fly(
    #         conditions_of_directories, dtype='U', order_outputs='iv'):
    for combination_indexes_i, directory_i in cc_directory.conditions_to_directories_on_the_fly(
            conditions_of_directories, order_outputs='iv'):

        indexes_array[axes_files] = combination_indexes_i
        array_i = array[tuple(indexes_array)]

        dirname_i = os.path.dirname(directory_i)
        os.makedirs(dirname_i, exist_ok=True)
        with open(directory_i, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            if headers is not None:
                writer.writerow(headers)
            writer.writerows(array_i)


def csv_file_to_lines(directory):
    with open(directory, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        lines = list(reader)
    return lines


def csv_file_to_array(filename, rows, columns, dtype=None):

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        table = np.asarray(list(reader), dtype=dtype)

    indexes = tuple(cc_format.numeric_indexes_to_slice([rows, columns]))
    array = table[indexes]

    return array


def csv_file_to_arrays(filename, rows, columns, dtype=None):
    try:
        n_arrays_from_rows = len(rows)
    except TypeError:
        rows = [rows]
        n_arrays_from_rows = 1
    try:
        n_arrays_from_columns = len(columns)
    except TypeError:
        columns = [columns]
        n_arrays_from_columns = 1

    if n_arrays_from_rows != n_arrays_from_columns:
        if n_arrays_from_rows == 1:
            rows = list(rows) * n_arrays_from_columns
            n_arrays_from_rows = n_arrays_from_columns
        elif n_arrays_from_columns == 1:
            columns = list(columns) * n_arrays_from_rows
            n_arrays_from_columns = n_arrays_from_rows
        else:
            raise ValueError(
                'The following assumption is not met:\n'
                '\t n_arrays_from_rows' + ' \u003D ' + 'n_arrays_from_columns')

    n_arrays = n_arrays_from_rows
    try:
        n_dtypes = len(dtype)
    except TypeError:
        dtype = [dtype]
        n_dtypes = 1
    if n_arrays != n_dtypes:
        if n_dtypes == 1:
            dtype = list(dtype) * n_arrays
        else:
            raise ValueError(
                'The following assumption is not met:\n'
                '\t(n_dtypes \u003D n_arrays_from_rows) OR (n_dtypes \u003D n_arrays_from_columns)')

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        table = np.asarray(list(reader), dtype='U')

    n_axes_per_text = 2
    arrays = [None] * n_arrays
    for a in range(n_arrays):
        indexes = tuple(cc_format.numeric_indexes_to_slice([rows[a], columns[a]]))
        if (dtype[a] is None) or (dtype[a] == str) or ('U' in dtype[a][:3]):
            arrays[a] = table[indexes]
        else:
            arrays[a] = table[indexes].astype(dtype[a])
    return arrays


def conditions_of_csv_files_to_arrays(conditions_of_directories, rows, columns, dtype=None):

    n_axes_directories = len(conditions_of_directories)
    n_conditions_directories = np.empty(n_axes_directories, dtype=int)
    for i in range(n_axes_directories):
        n_conditions_directories[i] = len(conditions_of_directories[i])
    # logical_indexes_conditions = n_conditions_directories > 1
    combinations_directories = cc_combinations.n_conditions_to_combinations(n_conditions_directories)
    n_combinations_directories = combinations_directories.shape[0]
    axes_directories_squeezed = n_conditions_directories > 1
    n_axes_directories_squeezed = np.sum(axes_directories_squeezed)

    try:
        n_arrays_from_rows = len(rows)
    except TypeError:
        rows = [rows]
        n_arrays_from_rows = 1
    try:
        n_arrays_from_columns = len(columns)
    except TypeError:
        columns = [columns]
        n_arrays_from_columns = 1

    if n_arrays_from_rows != n_arrays_from_columns:
        if n_arrays_from_rows == 1:
            rows = list(rows) * n_arrays_from_columns
            n_arrays_from_rows = n_arrays_from_columns
        elif n_arrays_from_columns == 1:
            columns = list(columns) * n_arrays_from_rows
            n_arrays_from_columns = n_arrays_from_rows
        else:
            raise ValueError(
                'The following assumption is not met:\n'
                '\t n_arrays_from_rows' + ' \u003D ' + 'n_arrays_from_columns')

    n_arrays = n_arrays_from_rows
    try:
        n_dtypes = len(dtype)
    except TypeError:
        dtype = [dtype]
        n_dtypes = 1
    if n_arrays != n_dtypes:
        if n_dtypes == 1:
            dtype = list(dtype) * n_arrays
        else:
            raise ValueError(
                'The following assumption is not met:\n'
                '\t(n_dtypes \u003D n_arrays_from_rows) OR (n_dtypes \u003D n_arrays_from_columns)')

    n_axes_per_csv = 2
    indexes = [None] * n_arrays  # type: list
    arrays = [None] * n_arrays  # type: list
    for a in range(n_arrays):
        indexes[a] = tuple(cc_format.numeric_indexes_to_slice([rows[a], columns[a]]))

    directory_csv_d = os.path.join(*[
        conditions_of_directories[i][0] for i in range(n_axes_directories)])

    with open(directory_csv_d, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # array_csv_d = list(reader)
        array_csv_d = np.asarray(list(reader), dtype='U')

    indexes_out = [None] * n_arrays
    for a in range(n_arrays):
        if dtype[a] is None:
            dtype[a] = 'U'

        array_a_d = array_csv_d[indexes[a]]
        shape_array_a_d = np.asarray(array_a_d.shape, dtype=int)
        shape_array_a = np.append(
            n_conditions_directories[axes_directories_squeezed], shape_array_a_d)

        arrays[a] = np.empty(shape_array_a, dtype=dtype[a])
        n_axes_a = shape_array_a.size
        indexes_out = np.empty(n_axes_a, dtype=object)
        indexes_out[:] = slice(None)

    for d in range(n_combinations_directories):

        directory_csv_d = os.path.join(*[
            conditions_of_directories[i][combinations_directories[d, i]] for i in range(n_axes_directories)])

        with open(directory_csv_d, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            array_csv_d = np.asarray(list(reader), dtype='U')

        indexes_out[slice(0, n_axes_directories_squeezed, 1)] = (
            combinations_directories[d, axes_directories_squeezed])

        for a in range(n_arrays):
            arrays[a][tuple(indexes_out)] = array_csv_d[indexes[a]]  # .astype(dtype[a])

    return arrays


def n_csv_files_to_array_old(
        directories_csv_files, names_csv_files_in_directories=False,
        rows=slice(None), columns=slice(None), data_type=None):

    print('using the funtion n_csv_files_to_array().\n'
          'In the future versions of ccalafiore, it will be removed.\n'
          'Consider using conditions_of_csv_files_to_arrays()')
    array = None

    n_axes_directories = len(directories_csv_files)
    n_conditions_directories = np.empty(n_axes_directories, dtype=int)
    for a in range(n_axes_directories):
        n_conditions_directories[a] = len(directories_csv_files[a])

    logical_indexes_conditions = n_conditions_directories > 1

    combinations_directories = cc_combinations.n_conditions_to_combinations(n_conditions_directories)
    n_combinations_directories = combinations_directories.shape[0]

    for d in range(n_combinations_directories):

        directory = directories_csv_files[0][combinations_directories[d, 0]]
        for a in range(1, n_axes_directories):
            directory = os.path.join(
                directory, directories_csv_files[a][combinations_directories[d, a]])

        if names_csv_files_in_directories:
            files_per_directory = [directory]
        else:
            files_per_directory = glob.glob(os.path.join(directory, '*.csv'))

        n_files_per_directory = len(files_per_directory)

        start_row_f_file = 0
        for f in range(n_files_per_directory):

            array_per_file = np.genfromtxt(files_per_directory[f], delimiter=',', dtype=data_type)[rows, columns]

            if array is None:

                shape_array_per_file = np.asarray(array_per_file.shape, dtype=int)

                shape_array = np.asarray([
                    *n_conditions_directories[logical_indexes_conditions],
                    n_files_per_directory * shape_array_per_file[0],
                    *shape_array_per_file[1:]
                ], dtype=int)

                array = np.empty(shape_array, dtype=data_type)

            end_row_f_file = (f + 1) * shape_array_per_file[0]

            indexes_array = tuple(
                [*combinations_directories[d][logical_indexes_conditions],
                 slice(start_row_f_file, end_row_f_file)])

            array[indexes_array] = array_per_file
            start_row_f_file = end_row_f_file

    return array
