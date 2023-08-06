import h5py
import numpy as np
import pandas as pd
import ntpath
import hdf5_exceptions


class HDF5Helper:
    """
    DESCRIPTION
    -----------
    This class contains methods for argument, group, dataset, and duplicate checks as well as other 
    methods that add functionality to HDF5Content and HDF5Components.
    """


    #----------Group Functions----------


    def check_group_name(self, group_names_list, group_name):
        """
        DESCRIPTION
        -----------
        Returns True if "group_name" is a group name in the HDF5 file. 
        Otherwise returns False and raises a GroupNameError.

        PARAMETERS
        ----------
        group_names_list: list
            list of group names in the HDF5 file
        group_name: str
            name of the group to check 
        
        RETURNS
        -------
        True
        -or-
        False
        """

        if group_name not in group_names_list:
            valid_group_name = False
            raise hdf5_exceptions.GroupNameError(group_name=group_name)
        else:
            valid_group_name = True

        return valid_group_name

    def is_group(self, hdf5_obj):
        """
        DESCRIPTION
        -----------
        Returns True if the "hdf5_obj" object a HDF5 group object. Otherwise returns False.
        
        PARAMETERS
        ----------
        hdf5_obj: HDF5 class object
            HDF5 class object to check
        
        RETURNS
        -------
        True
        -or-
        False
        """

        if isinstance(hdf5_obj, h5py._hl.group.Group):  # if hdf5_obj is a group object
            return True
        else:
            return False


    #----------Dataset Functions----------


    def check_dataset_name(self, dataset_names_list, dataset_name):
        """
        DESCRIPTION
        -----------
        Returns True if "dataset_name" is a dataset name in the HDF5 file. 
        Otherwise returns False and raises a DatasetNameError.

        PARAMETERS
        ----------
        dataset_names_list: list
            list of group names in the HDF5 file
        dataset_name: str
            name of the dataset to check 
        
        RETURNS
        -------
        True
        -or-
        False
        """

        if dataset_name not in dataset_names_list:
            valid_dataset_name = False
            raise hdf5_exceptions.DatasetNameError(dataset_name=dataset_name)
        else:
            valid_dataset_name = True

        return valid_dataset_name

    def dup_dataset_check(self, dataset_name):
        """
        DESCRIPTION
        -----------
        Returns True if "dataset_name" is a duplicate dataset in the HDF5 file. Otherwise returns False.

        PARAMETERS
        ----------
        dataset_name: str
            name of the dataset to check 
        
        RETURNS
        -------
        True
        -or-
        False
        """

        dup_dataset_names_list = self.get_dup_dataset_names()  # list of all duplicate dataset names

        if dataset_name in dup_dataset_names_list:  # if duplicate dataset name
            return True
        else:
            return False

    def dup_dataset_prompt(self, dataset_name):
        """
        DESCRIPTION
        -----------
        Prompts the user to choose a dataset path to explicitly select a dataset when
        a duplicate "dataset_name" is passed.
        Returns the HDF5 file path of the selected dataset. 

        PARAMETERS
        ----------
        dataset_name: str
            name of the dataset to check 
        
        RETURNS
        -------
        sel_dataset_path: str
            path of the user-selected dataset
        """

        print(str(dataset_name) + " is a duplicate dataset name. Please select a dataset path:")
        dup_dataset_path_list = self.all_dataset_names_dict[dataset_name]["dataset_paths"]  # list of duplicate dataset paths
        
        for i, dataset_path in enumerate(dup_dataset_path_list):  # for each dataset path 
            print(str(i) + ": " + str(dataset_path))

        sel_num = int(input("Enter the value of the corresponding path: "))  # prompt user to select a dataset path
        sel_dataset_path = dup_dataset_path_list[sel_num]  # dataset path selected by the user 

        return sel_dataset_path

    def zip_datasets(self):
        """
        DESCRIPTION
        -----------
        Returns a zip object of the dataset_path_list, dataset_name_list, and dataset_list.

        PARAMETERS
        ----------
        none
        
        RETURNS
        -------
        zipped_datasets: zip object
            iterator of a tuple of dataset_path_list, dataset_name_list, and dataset_list
        """

        dataset_path_list = self.get_all_dataset_paths()
        dataset_name_list = self.get_all_dataset_names()
        dataset_obj_list = self.get_all_dataset_objs()

        zipped_datasets = zip(dataset_path_list, dataset_name_list, dataset_obj_list)

        return zipped_datasets

    def is_dataset(self, hdf5_obj):
        """
        DESCRIPTION
        -----------
        Returns True if the "hdf5_obj" object a HDF5 group object. Otherwise returns False.
        
        PARAMETERS
        ----------
        hdf5_obj: HDF5 class object
            HDF5 class object to check
        
        RETURNS
        -------
        True
        -or-
        False
        """

        if isinstance(hdf5_obj, h5py._hl.dataset.Dataset):  # if hdf5_obj is a dataset object
            return True
        else:
            return False


    #----------Misc. Functions----------


    def check_args(self, arg_list, req_num_args):
        """
        DESCRIPTION
        -----------
        Raises an ArgumentError if zero or more than req_num_args number of arguments are passed to a function.

        PARAMETERS
        ----------
        arg_list: list
            list of arguments passed to a function
        req_num_args: int
            number of required arguments

        RETURNS
        -------
        none
        """

        # the first arg in arg_list is always self, so the slice taken from [1:] 
        # total number of args that are not None
        if sum(arg is not None for arg in arg_list[1:]) == 0:  # if zero arguments are passed
            raise hdf5_exceptions.ArgumentError(error_message='Arguments are required for this function.')
        elif sum(arg is not None for arg in arg_list[1:]) > req_num_args:  # if more than req_num_args number of args are passed
            raise hdf5_exceptions.ArgumentError(error_message='Too many or invalid arguments were passed to this function.')

    def check_path(self, path_list, path_to_check):
        """
        DESCRIPTION
        -----------
        Returns True if "path_to_check" is a path in the HDF5 file. 
        Otherwise returns False and raises a PathError.

        PARAMETERS
        ----------
        path_list: list
            list of group and dataset paths in the HDF5 file
        path_to_check: str
            name of the path to check 
        
        RETURNS
        -------
        True
        -or-
        False
        """

        if path_to_check not in path_list:
            valid_path = False
            raise hdf5_exceptions.PathError(path=path_to_check)
        else:
            valid_path = True

        return valid_path

class HDF5Content(HDF5Helper):
    """
    DESCRIPTION
    -----------
    This class contains methods that organize the content of the HDF5 file into lists and dictionaries.
    
    PARAMETERS
    ----------
    hdf5_filepath: HDF5 file path
        path to the user-selected HDF5 file
    
    ATTRIBUTES
    ----------
    hdf5file: HDF5 file
        user-selected HDF5 file
    all_group_names_dict: dict
        dictionary of all groups and their associated info
        group names are keys
    all_dataset_names_dict: dict
        dictionary of all datasets and their associated info
        datasetset names are keys
    all_dataset_paths_dict: dict
        dictionary of all datasets and their associated info
        datasetset paths are keys
    """

    def __init__(self, hdf5_filepath):
        super()
        hdf5file = h5py.File(hdf5_filepath, "r")
        self.hdf5file = hdf5file  
        self.all_group_names_dict = self.get_all_group_names_dict()
        self.all_dataset_names_dict = self.get_all_dataset_names_dict()
        self.all_dataset_paths_dict = self.get_all_dataset_paths_dict()  


    # ----------Group Functions----------


    def get_all_group_paths(self):
        """
        DESCRIPTION
        -----------
        Returns a list of all group paths in the HDF5 file (including the Root Group and subgroups).
        
        RETURNS
        -------
        all_group_paths_list: list
            list of all group paths
        """

        all_group_paths_list = []
        all_group_paths_list.append("/")  # add Root Group to list

        def visit_group(path):
            if isinstance(self.hdf5file[path], h5py._hl.group.Group):  # if group
                all_group_paths_list.append(path)  # add group to list

        self.hdf5file.visit(visit_group)  # visit all objects in the HDF5 file

        return all_group_paths_list

    def get_all_group_objs(self):
        """
        DESCRIPTION
        -----------
        Returns a list of all group class objects in the HDF5 file (including the Root Group and subgroups).
        
        RETURNS
        -------
        all_group_objs_list: list
            list of all HDF5 group class objects
        """

        all_group_objs_list = []

        all_group_paths_list = self.get_all_group_paths()  # all group paths

        for group_path in all_group_paths_list:  # for every group path
            all_group_objs_list.append(self.hdf5file[group_path])  # add group object to list

        return all_group_objs_list

    def get_all_group_names(self):
        """
        DESCRIPTION
        -----------
        Returns a list of all group names in the HDF5 file (including the Root Group and subgroups).
        
        RETURNS
        -------
        all_group_names_list: list
            list of all group names
        """
        all_group_names_list = []

        def visit_group(path):
            if isinstance(self.hdf5file[path], h5py._hl.group.Group):  # if group
                all_group_names_list.append(path.split("/")[-1])  # add group name to list

        self.hdf5file.visit(visit_group) # visit all objects in the HDF5 file
        all_group_names_list.insert(0, "/")  # add Root Group to start of list

        return all_group_names_list

    def get_all_group_names_dict(self):
        """
        DESCRIPTION
        -----------
        Returns a dictionary of all group names (including the Root Group and subgroups) and their associated info from the HDF5 file.
            Key - group name
            Value - group info
        
        RETURNS
        ----------
        all_group_names_dict: dict
            dictionary of all group names and their associated info
        """

        all_group_names_list = self.get_all_group_names()
        all_group_paths_list = self.get_all_group_paths()
        all_group_objs_list = self.get_all_group_objs()

        all_group_names_dict = {}

        for i, group_name in enumerate(all_group_names_list):  # for each group name in the list
            group_obj = all_group_objs_list[i]  # group object
            group_path = all_group_paths_list[i]  # group path

            subgroup_list = self.get_subgroups_list(group_path=group_path)  # list of subgroups in the group_path group 
            subgroup_dict = {}

            for subgroup_name in subgroup_list:  # for each subgroup name in the list
                subgroup_path = group_path + "/" + subgroup_name  # subgroup path
                subgroup_obj = self.hdf5file.get(subgroup_path)  # subgroup object

                subgroup_dict.update({subgroup_name: subgroup_obj})
            
            dataset_name_list = self.get_group_dataset_names(group_path=group_path)  # list of dataset names in the group_path group
            dataset_dict = {}

            for dataset_name in dataset_name_list:  # for each dataset name in the list
                dataset_path = group_path + "/" + dataset_name  # dataset path
                dataset_obj = self.hdf5file.get(dataset_path)  # dataset object

                dataset_dict.update({dataset_name: dataset_obj})

            group_and_path_dict = {
                "group_obj": group_obj,
                "group_path": group_path,
                "subgroups": subgroup_dict,
                "datasets": dataset_dict,
            }

            all_group_names_dict.update({group_name: group_and_path_dict})

        return all_group_names_dict

    def get_all_group_objs_dict(self):
        """
        DESCRIPTION
        -----------
        Returns a dictionary of all group objects (including the Root Group and subgroups) and their group name from the HDF5 file.
            Key - group class object
            Value - group name
        
        RETURNS
        -------
        all_group_objs_dict: dict
            dictionary of all group objects and their associated info
        """

        all_group_objs_list = self.get_all_group_objs()
        all_group_names_list = self.get_all_group_names()
        all_group_paths_list = self.get_all_group_paths()

        all_group_objs_dict = {}

        for i, group_obj in enumerate(all_group_objs_list):  # for each group object in the list
            group_name = all_group_names_list[i]  # group name
            group_path = all_group_paths_list[i]  # group path

            group_and_path_dict = {
                "group_name": group_name,
                "group_path": group_path
            }

            all_group_objs_dict.update({group_obj: group_and_path_dict})

        return all_group_objs_dict

    def get_subgroups_list(self, group_path):
        """
        DESCRIPTION
        -----------
        Returns a list of subgroup names within the group at the "group_path" location in the HDF5 file.
        
        PARAMETERS
        ----------
        group_path: str
            path of the group in the HDF5 file
        
        RETURNS
        -------
        subgroup_list: list
            list of subgroups within a group
        """

        try:
            valid_path = self.check_path(path_list=self.get_all_group_paths(), path_to_check=group_path)
            if valid_path:
                subgroup_list = []

                for name, obj in self.hdf5file[group_path].items():  # for each name and object in the group_path group
                    if self.is_group(hdf5_obj=obj):  # if group (subgroup) object
                        subgroup_name = name  # subgroup name
                        subgroup_list.append(subgroup_name)  # add subgroup name to list

                return subgroup_list
        
        except hdf5_exceptions.PathError as e:
            print(e)


    # ----------Dataset Functions----------


    def get_all_dataset_paths(self):
        """
        DESCRIPTION
        -----------
        Returns a list of all dataset paths in the HDF5 file.
        
        RETURNS
        -------
        all_dataset_paths_list: list
            list of all dataset paths
        """

        all_dataset_paths_list = []

        def visit_dataset(path):
            if isinstance(self.hdf5file[path], h5py._hl.dataset.Dataset):  # if dataset
                all_dataset_paths_list.append(path)  # add dataset path to list

        self.hdf5file.visit(visit_dataset)  # visit all objects in the HDF5 file

        return all_dataset_paths_list

    def get_all_dataset_objs(self):
        """
        DESCRIPTION
        -----------
        Returns a list of all dataset class objects in the HDF5 file.
        
        RETURNS
        -------
        all_dataset_objs_list: list
            list of all dataset class objects
        """

        all_dataset_objs_list = []

        all_dataset_paths_list =  self.get_all_dataset_paths()

        for dataset_path in all_dataset_paths_list:  # for each dataset path in the list
            all_dataset_objs_list.append(self.hdf5file[dataset_path])  # add dataset object to list

        return all_dataset_objs_list

    def get_all_dataset_names(self):
        """
        DESCRIPTION
        -----------
        Returns a list of all dataset names in the HDF5 file.
        
        RETURNS
        -------
        all_dataset_names_list: list
            list of all dataset names
        """

        all_dataset_names_list = []

        def visit_dataset(path):
            if isinstance(self.hdf5file[path], h5py._hl.dataset.Dataset):  # if dataset
                all_dataset_names_list.append(path.split("/")[-1])  # add dataset name to list

        self.hdf5file.visit(visit_dataset)  # visit all objects in the HDF5 file

        return all_dataset_names_list

    def get_all_dataset_paths_dict(self):
        """
        DESCRIPTION
        -----------
        Returns a dictionary of every dataset path and its associated info from the HDF5 file.
            Key - dataset path
            Value - dataset info
        
        RETURNS
        -------
        all_dataset_paths_dict: dict
            dictionary of every dataset path and its associated info
        """

        zipped_datasets = self.zip_datasets()  

        all_dataset_paths_dict = {}

        for dataset_path, dataset_name, dataset_obj in zipped_datasets:  # for tuple of dataset_path_list, dataset_name_list, and dataset_list
            all_dataset_paths_dict.update({dataset_path: {"dataset_name": dataset_name, "dataset_obj": dataset_obj}})

        return all_dataset_paths_dict

    def get_all_dataset_names_dict(self):
        """
        DESCRIPTION
        -----------
        Returns a dictionary of every dataset name and its associated info from the HDF5 file.
            Key - dataset name
            Value - dataset info
        
        RETURNS
        -------
        all_dataset_names_dict: dict
            dictionary of every dataset name and its associated info
        """

        zipped_datasets = self.zip_datasets()  

        all_dataset_names_dict = {}

        for dataset_path, dataset_name, dataset_obj in zipped_datasets:  # for tuple of dataset_path_list, dataset_name_list, and dataset_list
            all_dataset_names_dict.update({dataset_name: {"dataset_path": dataset_path, "dataset_obj": dataset_obj}})

        dup_dataset_dict = self.get_dup_dataset_dict()  # dict of duplicate datasets

        for dataset_name, path_and_obj_dict in dup_dataset_dict.items():  # for dataset_name and path_and_obj_dict in the duplicate dataset dict
            all_dataset_names_dict.update({dataset_name: path_and_obj_dict}) 
        
        return all_dataset_names_dict

    def get_group_dataset_names(self, group_name=None, group_path=None):
        """
        DESCRIPTION
        -----------
        Returns a list of dataset names within the group at the "group_path" location in the HDF5 file. Does not include datasets within subgroups.
        
        PARAMETERS
        ----------
        group_name: str
            name of the group in the HDF5 file
        group_path: str
            path of the group in the HDF5 file
        
        RETURNS
        -------
        dataset_name_list: list
            list of all dataset names within the group
        """

        try:
            arg_list = list(locals().values())  # list of arguments 
            self.check_args(arg_list=arg_list, req_num_args=1)  # returns error if 0 or > 1 arguments passed

            if group_name:  # if group_name passed in
                valid_group_name = self.check_group_name(group_names_list=self.get_all_group_names(), group_name=group_name)
                if valid_group_name:
                    group_path = self.get_path(group_name=group_name)
            elif group_path:  # if group_path passed in
                self.check_path(path_list=self.get_all_group_paths(), path_to_check=group_path)

            dataset_name_list = []
            for name, obj in self.hdf5file[group_path].items():  # for each name and object in the group_path group
                if self.is_dataset(hdf5_obj=obj):  # if dataset object
                    dataset_name = name  # dataset name
                    dataset_name_list.append(dataset_name)  # add dataset name to list

            return dataset_name_list

        except hdf5_exceptions.ArgumentError as e:
            print(e)
        except hdf5_exceptions.GroupNameError as e2:
            print(e2)
        except hdf5_exceptions.PathError as e3:
            print(e3)

    def get_dup_dataset_names(self):
        """
        DESCRIPTION
        -----------
        Returns a list of all duplicate dataset names in the HDF5 file.
        
        RETURNS
        -------
        dup_dataset_names_list: list
            list of all duplicate dataset names
        """

        seen_dict = {}
        dup_dataset_names_list = []
        all_dataset_names_list = self.get_all_dataset_names()  # list of all dataset names

        for dataset_name in all_dataset_names_list:  # for each dataset name 
            if dataset_name not in seen_dict:  # if first occurance of dataset name
                seen_dict.update({dataset_name: 1})  # key - dataset_name, value - 1
            else:  # if not first occurance of dataset_name
                if seen_dict[dataset_name] == 1:  # if first time seeing duplicate dataset name
                    dup_dataset_names_list.append(dataset_name)  # add dataset name to list of duplicates
                seen_dict[dataset_name] += 1  # prevents duplicates of dataset names in the list

        return dup_dataset_names_list

    def get_dup_dataset_dict(self):
        """
        DESCRIPTION
        -----------
        Returns a dictionary of every duplicate dataset name and its associated info from the HDF5 file.
            Key - duplicate dataset name
            Value - dataset info
        
        RETURNS
        -------
        dup_dataset_dict: dict
            dictionary of every duplicate dataset name and its associated info
        """

        dup_dataset_dict = {}
        all_dataset_paths = self.get_all_dataset_paths()  # list of all dataset paths
        dup_dataset_names_list = self.get_dup_dataset_names()  # list of all duplicate dataset names

        for dataset_name in dup_dataset_names_list:  # for each duplicate dataset name
            path_and_obj_dict = {}
            dup_dataset_path_list = []
            dup_dataset_list = []

            for dataset_path in all_dataset_paths:  # for each dataset path
                split_path = self.split_hdf5_path(hdf5_path=dataset_path)  # list of HDF5 path components
                if dataset_name == split_path[-1]:  # if dataset path
                    dup_dataset_path_list.append(dataset_path)  # add duplicate dataset path to list
                    dataset_obj = self.hdf5file.get(dataset_path)  # duplicate dataset object
                    dup_dataset_list.append(dataset_obj)  # add duplicate dataset object to list

                path_and_obj_dict.update({"dataset_path": dup_dataset_path_list, "dataset_obj": dup_dataset_list})

            dup_dataset_dict.update({dataset_name: path_and_obj_dict}) 

        return dup_dataset_dict


    # ----------Misc. Functions----------


    def get_path(self, group_name=None, dataset_name=None):
        """
        DESCRIPTION
        -----------
        Returns the HDF5 file path to a group or dataset.

        PARAMETERS
        ----------
        group_name: str
            group name to get the path to
        dataset_name: str
            dataset name to get the path to

        RETURNS
        -------
        hdf5_path: str
            path to the group or dataset location in the HDF5 file
        """

        try:
            arg_list = list(locals().values())  # list of arguments 
            self.check_args(arg_list=arg_list, req_num_args=1)  # returns error if 0 or > 1 arguments passed

            if group_name:  # if group_name passed in
                valid_group_name = self.check_group_name(group_names_list=self.get_all_group_names(), group_name=group_name)
                if valid_group_name:
                    hdf5_path = self.all_group_names_dict[group_name]["group_path"]
            elif dataset_name:  # if dataset_name passed in
                valid_dataset_name = self.check_dataset_name(dataset_names_list=self.get_all_dataset_names(), dataset_name=dataset_name)
                if valid_dataset_name:
                    if self.dup_dataset_check(dataset_name=dataset_name):  # True if dataset_name is a duplicate
                        hdf5_path = self.dup_dataset_prompt(dataset_name=dataset_name)  # prompt user to select a dataset path
                    else:  # if dataset_name is not a duplicate
                        hdf5_path = self.all_dataset_names_dict[dataset_name]["dataset_path"]  

            return hdf5_path
            
        except hdf5_exceptions.ArgumentError as e:
            print(e)
        except hdf5_exceptions.GroupNameError as e2:
            print(e2)
        except hdf5_exceptions.DatasetNameError as e3:
            print(e3)

    def get_metadata(self, group_name=None, dataset_name=None, dataset_path=None):
        """
        DESCRIPTION
        -----------
        Returns a dictionary of metadata attributes.
            Key - attribute name
            Value - attribute value

        PARAMETERS
        ----------
        group_name: str
            group name to get the metadata of
        -or-
        dataset_name: str
            dataset name to get the metadata of
        -or-
        dataset_path: str
            dataset path to get the metadata of
        
        RETURNS
        -------
        metadata_dict: dict
            dictionary of metadata attributes
        """

        try:
            arg_list = list(locals().values())  # list of arguments 
            self.check_args(arg_list=arg_list, req_num_args=1)  # returns error if 0 or > 1 arguments passed

            if group_name:  # if group_name passed in
                valid_group_name = self.check_group_name(group_names_list=self.get_all_group_names(), group_name=group_name)
                if valid_group_name:
                    group_path = self.get_path(group_name=group_name)
                    metadata_dict = dict(self.hdf5file[group_path].attrs) 
            elif dataset_name:  # if dataset_name passed in
                valid_dataset_name = self.check_dataset_name(dataset_names_list=self.get_all_dataset_names(), dataset_name=dataset_name)
                if valid_dataset_name:
                    dataset_path = self.get_path(dataset_name=dataset_name) 
                    metadata_dict = dict(self.hdf5file[dataset_path].attrs)
            elif dataset_path:  # if dataset_path passed in
                valid_path = self.check_path(path_list=self.get_all_dataset_paths(), path_to_check=dataset_path)
                if valid_path:
                    metadata_dict = dict(self.hdf5file[dataset_path].attrs)  
                
            return metadata_dict   

        except hdf5_exceptions.ArgumentError as e:
            print(e)
        except hdf5_exceptions.GroupNameError as e2:
            print(e2)
        except hdf5_exceptions.DatasetNameError as e3:
            print(e3)
        except hdf5_exceptions.PathError as e4:
            print(e4)

    def get_hdf5_filename(self, hdf5_filepath):
        """
        DESCRIPTION
        -----------
        Parses the HDF5 file path and returns the name of the HDF5 file.
        
        PARAMETERS
        ----------
        hdf5_filepath: HDF5 file path
            path to the user-selected HDF5 file
        
        RETURNS
        -------
        hdf5_filename: str
            name of the HDF5 file
        """

        hdf5_filename = ntpath.basename(hdf5_filepath)  # works on Windows and Linux

        return hdf5_filename

    def get_name(self, hdf5_path):
        """
        DESCRIPTION
        -----------
        Returns the group or dataset name from the HDF5 file path.

        PARAMETERS
        ----------
        hdf5_path: str
            HDF5 path to the group or dataset
        
        RETURNS
        -------
        name: str
            name of the group or dataset
        """

        split_path_list = self.split_hdf5_path(hdf5_path=hdf5_path)  # list of HDF5 path components
        name = split_path_list[-1]  # the last index is the name of the group or dataset

        return name

    def split_hdf5_path(self, hdf5_path):
        """
        DESCRIPTION
        -----------
        Parses an HDF5 group or dataset path and creates a list of the path components.

        PARAMETERS
        ----------
        hdf5_path: str
            HDF5 path to the group or dataset
        
        RETURNS
        -------
        split_path: list
            list of path components
        """

        if "/" in hdf5_path:  # if components in path
            split_path = hdf5_path.split("/")  # create list of components
        else:  # if no components in path
            split_path = [hdf5_path]  # create list of the components

        return split_path


class HDF5Components(HDF5Content):
    """
    DESCRIPTION
    -----------
    This class contains methods that return various components of the HDF5 file to the user.
        Groups, datasets, dataset values, NumPy/Pandas matrices of dataset values, metadata, and structured dictionaries.
    
    PARAMETERS
    ----------
    hdf5_filepath: HDF5 file path
        path to the user-selected HDF5 file
    
    ATTRIBUTES
    ----------
    all_group_names_dict: dict
        dictionary of every group and its associated info
        group names are keys
    all_dataset_names_dict: dict
        dictionary of all datasets and their associated info
        datasetset names are keys
    all_dataset_paths_dict: dict
        dictionary of all datasets and their associated info
        datasetset paths are keys
    """

    def __init__(self, hdf5_filepath):
        super().__init__(hdf5_filepath=hdf5_filepath)


    # ----------Group Functions----------


    def get_group_info(self, group_name):
        """
        DESCRIPTION
        -----------
        Returns a dictionary of the group info.
            Key - group item name
            Value - group item value
        
        PARAMETERS
        ----------
        group_name: str
            name of the group to get the info of
        
        RETURNS
        -------
        group_info_dict: dict
            dictionary of group info 
        """

        try:
            valid_group_name = self.check_group_name(group_names_list=self.get_all_group_names(), group_name=group_name)
            if valid_group_name:
                group_path = self.get_path(group_name=group_name) 
                group_metadata = self.get_metadata(group_name=group_name) 

                subgroup_dict = self.all_group_names_dict[group_name]["subgroups"] 
                dataset_dict = self.all_group_names_dict[group_name]["datasets"] 

                group_info_dict = {
                    "group_name": group_name,
                    "group_path": group_path,
                    "group_metadata": group_metadata,
                    "subgroups": subgroup_dict,
                    "datasets": dataset_dict
                }

                return group_info_dict

        except hdf5_exceptions.GroupNameError as e:
            print(e)

    def get_group_obj(self, group_name):
        """
        DESCRIPTION
        -----------
        Returns the HDF5 group class object for the "group_name" group.
        
        PARAMETERS
        ----------
        group_name: str
            name of the group to get HDF5 class object of
        
        RETURNS
        -------
        group_obj: HDF5 group class object
            instance of the HDF5 group class
        """

        try:
            valid_group_name = self.check_group_name(group_names_list=self.get_all_group_names(), group_name=group_name)
            if valid_group_name:
                group_obj = self.all_group_names_dict[group_name]["group_obj"]  

                return group_obj

        except hdf5_exceptions.GroupNameError as e:
            print(e)

    # TODO: test how this handles two levels of subgroups
    def get_group_dict(self, group_name):
        """
        DESCRIPTION
        -----------
        Returns a dictionary of the group info and its subgroups, and datasets.
            Key - group item name
            Value - group item value
        
        PARAMETERS
        ----------
        group_name: str
            name of the group to get
        
        RETURNS
        -------
        group_dict: dict
            dictionary of group info, subgroups, and datasets
        """

        try:
            valid_group_name = self.check_group_name(group_names_list=self.get_all_group_names(), group_name=group_name)
            if valid_group_name:
                group_path = self.get_path(group_name=group_name)

                group_info_dict = self.get_group_info(group_name=group_name)
                subgroup_dict = self.get_subgroup_dict(group_path=group_path)

                group_dict = group_info_dict
                group_dict.update({"subgroup_dict": subgroup_dict})

                full_dataset_dict  = {}
                for dataset_name, dataset_obj in group_info_dict["datasets"].items():  # for each dataset name and dataset object
                    dataset_path = dataset_obj.name[1:]  # removes the "/" at the start of the path string

                    dataset_dict = self.get_dataset_dict(dataset_path=dataset_path)
                    full_dataset_dict.update({dataset_name: dataset_dict})

                group_dict.update({"dataset_dict": full_dataset_dict})
                
                return group_dict
        
        except hdf5_exceptions.GroupNameError as e:
            print(e)

    def get_subgroup_dict(self, group_path):
        """
        DESCRIPTION
        -----------
        Returns a dictionary of subgroup info for each subgroup in the group at the group_path location in the HDF5 file.
            Key - subgroup name
            Value - subgroup info
        
        PARAMETERS
        ----------
        group_path: str
            path of the subgroup in the HDF5 file
        
        RETURNS
        -------
        subgroup_dict: dict
            dictionary of subgroup info for each subgroup in the group
        """

        try:
            valid_path = self.check_path(path_list=self.get_all_group_paths(), path_to_check=group_path)
            if valid_path:
                subgroups_list = self.get_subgroups_list(group_path=group_path)  # list of subgroups in the group_path group

                subgroup_dict = {}
                for subgroup_name in subgroups_list:  # for each subgroup name
                    subgroup_info_dict = self.get_group_info(group_name=subgroup_name)  
                    subgroup_dict.update({subgroup_name: subgroup_info_dict})

                return subgroup_dict

        except hdf5_exceptions.PathError as e:
            print(e)

    def get_parent_group_obj(self, group_name=None, dataset_name=None, dataset_path=None):
        """
        DESCRIPTION
        -----------
        Returns the parent group class object of the dataset or group.

        PARAMETERS
        ----------
        group_name: str
            name of the group to get the parent group of
        -or-
        dataset_name: str
            name of the dataset to get the parent group of
        -or-
        dataset_path: str
            path of the dataset to get the parent group of

        RETURNS
        -------
        parent_group_obj: HDF5 group class object
            instance of the class object of the parent group
        """

        try:
            arg_list = list(locals().values())  # list of arguments 
            self.check_args(arg_list=arg_list, req_num_args=1)  # returns error if 0 or > 1 arguments passed

            if group_name:  # if group_name passed in
                valid_group_name = self.check_group_name(group_names_list=self.get_all_group_names(), group_name=group_name)
                if valid_group_name:
                    if group_name != "/":  # if not the Root Group
                        group_obj = self.get_group_obj(group_name=group_name)
                        parent_group_obj = group_obj.parent  
                    else:
                        parent_group_obj = None  # root group "/" has no parent group
                return parent_group_obj
            elif dataset_name:  # if dataset_name passed in
                valid_dataset_name = self.check_dataset_name(dataset_names_list=self.get_all_dataset_names(), dataset_name=dataset_name)
                if valid_dataset_name:
                    dataset_path = self.get_path(dataset_name=dataset_name)
                    dataset_obj = self.get_dataset_obj(dataset_path=dataset_path)
                    parent_group_obj = dataset_obj.parent 
                    return parent_group_obj      
            elif dataset_path:  # if dataset_path passed in
                valid_dataset_path = self.check_path(path_list=self.get_all_dataset_paths(), path_to_check=dataset_path)
                if valid_dataset_path:
                    dataset_obj = self.get_dataset_obj(dataset_path=dataset_path)
                    parent_group_obj = dataset_obj.parent 
                    return parent_group_obj

        except hdf5_exceptions.ArgumentError as e:
            print(e)
        except hdf5_exceptions.GroupNameError as e2:
            print(e2)
        except hdf5_exceptions.DatasetNameError as e3:
            print(e3)
        except hdf5_exceptions.PathError as e4:
            print(e4)

    def get_parent_group_path(self, group_name=None, dataset_name=None, dataset_path=None):
        """
        DESCRIPTION
        -----------
        Returns the path of the parent group of the dataset or group.

        PARAMETERS
        ----------
        group_name: str
            name of the group to get the parent group of
        -or-
        dataset_name: str
            name of the dataset to get the parent group of
        -or-
        dataset_path: str
            path of the dataset to get the parent group of

        RETURNS
        -------
        parent_group_path: str
            path in HDF5 file to the parent group 
        """

        try:
            arg_list = list(locals().values())  # list of arguments 
            self.check_args(arg_list=arg_list, req_num_args=1)  # returns error if 0 or > 1 arguments passed

            if group_name:  # if group_name passed in
                valid_group_name = self.check_group_name(group_names_list=self.get_all_group_names(), group_name=group_name)
                if valid_group_name:
                    if group_name != "/":  # if not the Root Group
                        group_obj = self.get_group_obj(group_name=group_name)
                        parent_group_path = group_obj.parent.name
                    else:
                        parent_group_path = None  # root group "/" has no parent group path
                return parent_group_path
            elif dataset_name:  # if dataset_name passed in
                valid_dataset_name = self.check_dataset_name(dataset_names_list=self.get_all_dataset_names(), dataset_name=dataset_name)
                if valid_dataset_name:
                    dataset_path = self.get_path(dataset_name=dataset_name)
                    dataset_obj = self.get_dataset_obj(dataset_path=dataset_path)
                    parent_group_path = dataset_obj.parent.name
                    return parent_group_path
            elif dataset_path:  # if dataset_path passed in
                valid_dataset_path = self.check_path(path_list=self.get_all_dataset_paths(), path_to_check=dataset_path)
                if valid_dataset_path:
                    dataset_obj = self.get_dataset_obj(dataset_path=dataset_path)
                    parent_group_path = dataset_obj.parent.name
                    return parent_group_path

        except hdf5_exceptions.ArgumentError as e:
            print(e)
        except hdf5_exceptions.GroupNameError as e2:
            print(e2)
        except hdf5_exceptions.DatasetNameError as e3:
            print(e3)
        except hdf5_exceptions.PathError as e4:
            print(e4)

    def get_parent_group_name(self, group_name=None, dataset_name=None, dataset_path=None):
        """
        DESCRIPTION
        -----------
        Returns the name of the parent group of the dataset or group.

        PARAMETERS
        ----------
        group_name: str
            name of the group to get the parent group of
        -or-
        dataset_name: str
            name of the dataset to get the parent group of
        -or-
        dataset_path: str
            path of the dataset to get the parent group of

        RETURNS
        -------
        parent_group_name: str
            name of the parent group 
        """

        try:
            arg_list = list(locals().values())  # list of arguments 
            self.check_args(arg_list=arg_list, req_num_args=1)  # returns error if 0 or > 1 arguments passed

            all_group_objs_dict = self.get_all_group_objs_dict()

            if group_name:  # if group_name passed in
                valid_group_name = self.check_group_name(group_names_list=self.get_all_group_names(), group_name=group_name)
                if valid_group_name:
                    if group_name != "/":  # if not the Root Group
                        parent_group_obj = self.get_parent_group_obj(group_name=group_name)
                        parent_group_name = all_group_objs_dict[parent_group_obj]["group_name"]
                    else:
                        parent_group_name = None  # root group "/" has no parent group name
                return parent_group_name
            elif dataset_name:  # if dataset_name passed in
                valid_dataset_name = self.check_dataset_name(dataset_names_list=self.get_all_dataset_names(), dataset_name=dataset_name)
                if valid_dataset_name:
                    dataset_path = self.get_path(dataset_name=dataset_name)
                    parent_group_obj = self.get_parent_group_obj(dataset_path=dataset_path)
                    parent_group_name = all_group_objs_dict[parent_group_obj]["group_name"]
                    return parent_group_name
            elif dataset_path:  # if dataset_path passed in
                valid_dataset_path = self.check_path(path_list=self.get_all_dataset_paths(), path_to_check=dataset_path)
                if valid_dataset_path:
                    parent_group_obj = self.get_parent_group_obj(dataset_path=dataset_path)
                    parent_group_name = all_group_objs_dict[parent_group_obj]["group_name"]
                    return parent_group_name

        except hdf5_exceptions.ArgumentError as e:
            print(e)
        except hdf5_exceptions.GroupNameError as e2:
            print(e2)
        except hdf5_exceptions.DatasetNameError as e3:
            print(e3)
        except hdf5_exceptions.PathError as e4:
            print(e4)

    def get_eeg_matrix(self, group_name, matrix_type="pandas", num_points=None):
        """
        DESCRIPTION
        -----------
        Combines all CNS EEG datasets (EEG channels) within a group into one 2D matrix.
        Returns a matrix of all EEG channel values for the following CNS groups:
            Impedance, NeonatalParamas, SampleSeries
        
        PARAMETERS
        ----------
        group_name: str
            name of the CNS group containing the datasets to be converted
        matrix_type: str
            matrix type to convert the dataset values into - "pandas" or "numpy"
            default value: "pandas"
        
        RETURNS
        -------
        eeg_matrix: Pandas DataFrame or NumPy Array
            matrix of all EEG channel values of a group
        """

        try:
            cns_eeg_group_list = ["Impedance", "NeonatalParams", "SampleSeries"]  # list of valid CNS EEG group names

            if group_name not in cns_eeg_group_list:  # if group_name is not in the list of valid CNS EEG group names
                raise hdf5_exceptions.EEGGroupNameError(group_name=group_name)
            else:
                group_path = self.get_path(group_name=group_name)

                eeg_metadata = self.get_metadata(group_name=group_name)
                channel_names_list = eeg_metadata["channel_names"]  # list of EEG channel names

                if matrix_type.lower() == "pandas":  # if the user-selected matrix_type is pandas
                    eeg_matrix = pd.DataFrame(columns=channel_names_list)  # create DataFrame
                    for channel_name in channel_names_list:  # for each channel name
                        if num_points:
                            channel_values = self.hdf5file[group_path].get(channel_name)[0:num_points]
                            eeg_matrix[f"{channel_name}"] =  channel_values # add values to the channel_name col
                        else:
                            channel_values = self.hdf5file[group_path].get(channel_name)
                            eeg_matrix[f"{channel_name}"] = channel_values  # add values to the channel_name col

                elif matrix_type.lower() == "numpy":  # if the user-selected matrix_type is numpy
                    if num_points:
                        num_rows = num_points
                        num_cols = eeg_metadata["num_channels"]  # num of matrix cols is num of channels (each channel is a col)
                        eeg_matrix = np.empty(shape=(num_rows, num_cols), dtype=float)  # create Array
                        for i, channel_name in enumerate(channel_names_list):  # for each channel name
                            eeg_matrix[:, i] = self.hdf5file[group_path].get(channel_name)[0:num_points]  # add values to the channel_name col
                    else:
                        num_rows = eeg_metadata["num_time_slices"]  # num of matrix rows is num of time slices attribute
                        num_cols = eeg_metadata["num_channels"]  # num of matrix cols is num of channels (each channel is a col)
                        eeg_matrix = np.empty(shape=(num_rows, num_cols), dtype=float)  # create Array
                        for i, channel_name in enumerate(channel_names_list):  # for each channel name
                            eeg_matrix[:, i] = self.hdf5file[group_path].get(channel_name)  # add values to the channel_name col

                else:
                    raise hdf5_exceptions.MatrixTypeError(matrix_type=matrix_type)

                return eeg_matrix

        except hdf5_exceptions.EEGGroupNameError as e:
            print(e)
        except hdf5_exceptions.MatrixTypeError as e2:
            print(e2)


    # ----------Dataset Functions----------


    def get_dataset_info(self, dataset_name=None, dataset_path=None):
        """
        DESCRIPTION
        -----------
        Returns a dictionary of the dataset info.
            Key - info name
            Value - info value

        PARAMETERS
        ----------
        dataset_name: str
            name of the dataset to get the info of
        -or-
        dataset_path: str
            path of the dataset to get the info of
        
        RETURNS
        -------
        dataset_info_dict: dict
            dictionary of dataset info
        """

        try:
            arg_list = list(locals().values())  # list of arguments 
            self.check_args(arg_list=arg_list, req_num_args=1)  # returns error if 0 or > 1 arguments passed

            if dataset_name:  # if dataset_name passed in
                valid_dataset_name = self.check_dataset_name(dataset_names_list=self.get_all_dataset_names(), dataset_name=dataset_name)
                if valid_dataset_name:
                    dataset_path = self.get_path(dataset_name=dataset_name)
                    dataset_metadata = self.get_metadata(dataset_path=dataset_path)
                    column_names_list = self.get_column_names(dataset_path=dataset_path)  # list of dataset column names
                    dataset_info_dict = {
                        "dataset_name": dataset_name,
                        "dataset_path": dataset_path,
                        "dataset_metadata": dataset_metadata,
                        "column_names": column_names_list
                    }
                    return dataset_info_dict
            elif dataset_path:  # if dataset_path passed in
                valid_dataset_path = self.check_path(path_list=self.get_all_dataset_paths(), path_to_check=dataset_path)
                if valid_dataset_path:
                    dataset_metadata = self.get_metadata(dataset_path=dataset_path)
                    column_names_list = self.get_column_names(dataset_path=dataset_path)  # list of dataset column names
                    dataset_info_dict = {
                        "dataset_name": dataset_name,
                        "dataset_path": dataset_path,
                        "dataset_metadata": dataset_metadata,
                        "column_names": column_names_list
                    }
                    return dataset_info_dict

        except hdf5_exceptions.ArgumentError as e:
            print(e)
        except hdf5_exceptions.DatasetNameError as e2:
            print(e2)
        except hdf5_exceptions.PathError as e3:
            print(e3)

    def get_dataset_obj(self, dataset_name=None, dataset_path=None):  # returns the HDF5 dataset object
        """
        DESCRIPTION
        -----------
        Returns the HDF5 dataset class object for the "dataset_name" dataset.
        
        PARAMETERS
        ----------
        dataset_name: str
            name of the dataset to get HDF5 class object of
        -or-
        dataset_path: str
            path of the dataset to get HDF5 class object of
        
        RETURNS
        -------
        dataset_obj: HDF5 dataset class object
            instance of the HDF5 dataset class
            can be indexed like a normal array
        """

        try:
            arg_list = list(locals().values())  # list of arguments 
            self.check_args(arg_list=arg_list, req_num_args=1)  # returns error if 0 or > 1 arguments passed

            if dataset_name:  # if dataset_name passed in
                valid_dataset_name = self.check_dataset_name(dataset_names_list=self.get_all_dataset_names(), dataset_name=dataset_name)
                if valid_dataset_name:
                    dataset_path = self.get_path(dataset_name=dataset_name)
                    dataset_obj = self.hdf5file.get(dataset_path)
                    return dataset_obj
            elif dataset_path:  # if dataset_path passed in                                                
                valid_dataset_path = self.check_path(path_list=self.get_all_dataset_paths(), path_to_check=dataset_path)
                if valid_dataset_path:
                    dataset_obj = self.hdf5file.get(dataset_path)
                    return dataset_obj

        except hdf5_exceptions.ArgumentError as e:
            print(e)
        except hdf5_exceptions.DatasetNameError as e2:
            print(e2)
        except hdf5_exceptions.PathError as e3:
            print(e3)

    def get_dataset_dict(self, dataset_name=None, dataset_path=None):
        """
        DESCRIPTION
        -----------
        Returns a dictionary of the dataset info and values.
            Key - item name
            Value - item value

        PARAMETERS
        ----------
        dataset_name: str
            name of the dataset to get
        -or-
        dataset_path: str
            path of the dataset to get 
        
        RETURNS
        -------
        dataset_dict: dict
            dictionary of dataset info and values
        """

        try:
            arg_list = list(locals().values())  # list of arguments 
            self.check_args(arg_list=arg_list, req_num_args=1)  # returns error if 0 or > 1 arguments passed

            if dataset_name:  # if dataset_name passed in
                valid_dataset_name = self.check_dataset_name(dataset_names_list=self.get_all_dataset_names(), dataset_name=dataset_name)
                if valid_dataset_name:
                    dataset_path = self.get_path(dataset_name=dataset_name)
                    dataset_info_dict = self.get_dataset_info(dataset_path=dataset_path)
                    dataset = self.get_dataset_obj(dataset_path=dataset_path)
                    dataset_dict = dataset_info_dict
                    dataset_dict.update({"dataset": dataset})
                    return dataset_dict
            elif dataset_path:  # if dataset_path passed in
                valid_dataset_path = self.check_path(path_list=self.get_all_dataset_paths(), path_to_check=dataset_path)
                if valid_dataset_path:
                    dataset_info_dict = self.get_dataset_info(dataset_path=dataset_path)
                    dataset = self.get_dataset_obj(dataset_path=dataset_path)
                    dataset_dict = dataset_info_dict
                    dataset_dict.update({"dataset": dataset})
                    return dataset_dict

        except hdf5_exceptions.ArgumentError as e:
            print(e)
        except hdf5_exceptions.DatasetNameError as e2:
            print(e2)
        except hdf5_exceptions.PathError as e3:
            print(e3)

    def get_column_names(self, dataset_name=None, dataset_path=None):
        """
        DESCRIPTION
        -----------
        Returns a list of dataset column names.
        
        PARAMETERS
        ----------
        dataset_name: str
            name of the dataset to get the column names from
        -or-
        dataset_path: str
            path of the dataset to get the column names from
        
        RETURNS
        -------
        column_names_list: list
            list of column names
        """

        try:
            arg_list = list(locals().values())  # list of arguments 
            self.check_args(arg_list=arg_list, req_num_args=1)  # returns error if 0 or > 1 arguments passed

            if dataset_name:  # if dataset_name passed in
                valid_dataset_name = self.check_dataset_name(dataset_names_list=self.get_all_dataset_names(), dataset_name=dataset_name)
                if valid_dataset_name:
                    dataset_path = self.get_path(dataset_name=dataset_name)
                    column_names = self.get_dataset_obj(dataset_path=dataset_path).dtype.names
                    if column_names:  # if column names (not None)
                        column_names_list = list(column_names)  # list of dataset column names
                    else:  # if no column names
                        column_names_list = []
                    return column_names_list
            elif dataset_path:  # if dataset_path passed in
                valid_dataset_path = self.check_path(path_list=self.get_all_dataset_paths(), path_to_check=dataset_path)
                if valid_dataset_path:
                    column_names = self.get_dataset_obj(dataset_path=dataset_path).dtype.names
                    if column_names:  # if column names (not None)
                        column_names_list = list(column_names)  # list of dataset column names
                    else:  # if no column names
                        column_names_list = []
                    return column_names_list

        except hdf5_exceptions.ArgumentError as e:
            print(e)
        except hdf5_exceptions.DatasetNameError as e2:
            print(e2)
        except hdf5_exceptions.PathError as e3:
            print(e3)

    def get_values(self, dataset_name=None, dataset_path=None, matrix_type="pandas"):
        """
        DESCRIPTION
        -----------
        Returns a matrix the values in the dataset.
        
        PARAMETERS
        ----------
        dataset_name: str
            name of the dataset to get the NumPy Array from
        -or-
        dataset_path: str
            path of the dataset to get the NumPy Array from
        matrix_type: str
            matrix type get the dataset values in - "pandas" or "numpy"
            default value: "pandas"
        
        RETURNS
        -------
        dataset_values: Pandas DataFrame or NumPy Array
            matrix of dataset values
        """

        try:
            if dataset_name:  # if dataset_name passed in
                valid_dataset_name = self.check_dataset_name(dataset_names_list=self.get_all_dataset_names(), dataset_name=dataset_name)
                if valid_dataset_name:
                    dataset_path = self.get_path(dataset_name=dataset_name)
                    dataset_obj = self.get_dataset_obj(dataset_path=dataset_path)
                    if matrix_type == "pandas":
                        column_names_list = self.get_column_names(dataset_path=dataset_path)  # list of dataset column names
                        if column_names_list:  # if there are column names
                            dataset_values = pd.DataFrame(data=dataset_obj[:], columns=column_names_list)  # Pandas DataFrame of dataset values
                        else:  # if there are no column names
                            dataset_values = pd.DataFrame(data=dataset_obj[:])  # Pandas DataFrame of dataset values
                        return dataset_values
                    elif matrix_type == "numpy":
                        dataset_values = np.array(dataset_obj)  # NumPy Array of dataset values
                        return dataset_values
                    else:
                        raise hdf5_exceptions.MatrixTypeError(matrix_type=matrix_type)
            elif dataset_path:  # if dataset_path passed in
                valid_dataset_path = self.check_path(path_list=self.get_all_dataset_paths(), path_to_check=dataset_path)
                if valid_dataset_path:
                    dataset_obj = self.get_dataset_obj(dataset_path=dataset_path)
                    if matrix_type == "pandas":
                        column_names_list = self.get_column_names(dataset_path=dataset_path)  # list of dataset column names
                        if column_names_list:  # if there are column names
                            dataset_values = pd.DataFrame(data=dataset_obj[:], columns=column_names_list)  # Pandas DataFrame of dataset values
                        else:  # if there are no column names
                            dataset_values = pd.DataFrame(data=dataset_obj[:])  # Pandas DataFrame of dataset values
                        return dataset_values 
                    elif matrix_type == "numpy":
                        dataset_values = np.array(dataset_obj)  # NumPy Array of dataset values
                        return dataset_values
                    else:
                        raise hdf5_exceptions.MatrixTypeError(matrix_type=matrix_type)

        except hdf5_exceptions.DatasetNameError as e:
            print(e)
        except hdf5_exceptions.PathError as e2:
            print(e2)
        except hdf5_exceptions.MatrixTypeError as e3:
            print(e3)

