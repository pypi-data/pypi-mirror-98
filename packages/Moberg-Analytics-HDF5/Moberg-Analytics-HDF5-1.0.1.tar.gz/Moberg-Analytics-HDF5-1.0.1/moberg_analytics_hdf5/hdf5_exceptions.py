# moberg_hdf5 exception classes

class ArgumentError(Exception):
    """
    This Exception is raised to handle invalid function arguments.  
    """
    def __init__(self, error_message):
        self.error_message = error_message
        super().__init__(self.error_message)
        

class PathError(Exception):
    """
    This Exception is raised to handle invalid HDF5 paths.
    """

    def __init__(self, path):
        self.path = path
        self.error_message = f"{self.path} is not a valid path in the HDF5 file."
        super().__init__(self.error_message)


class MatrixTypeError(Exception):
    """
    This Exception is raised to handle invalid matrix type arguments.
    """

    def __init__(self, matrix_type):
        self.matrix_type = matrix_type
        self.error_message = f"{self.matrix_type} is not one of the supported matrix types: 'pandas' or 'numpy'"
        super().__init__(self.error_message)


class DatasetNameError(Exception):
    """
    This Exception is raised to handle invalid HDF5 dataset names.
    """

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.error_message = f"{self.dataset_name} is not a valid dataset name in the HDF5 file."
        super().__init__(self.error_message)


class GroupNameError(Exception):
    """
    This Exception is raised to handle invalid HDF5 group names.
    """

    def __init__(self, group_name):
        self.group_name = group_name
        self.error_message = f"{self.group_name} is not a valid group name in the HDF5 file."
        super().__init__(self.error_message)


class EEGGroupNameError(Exception):
    """
    This Exception is raised to handle invalid EEG group names.
    """

    def __init__(self, group_name):
        self.group_name = group_name
        self.error_message = f"{self.group_name} is one of the valid EEG group names: 'Impedance', 'NeonatalParams', or 'SampleSeries'"
        super().__init__(self.error_message)

