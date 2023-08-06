""" Functionalities to convert a certain format to hdf5.
    Currently supported:
        - nek5000 (requires "pymech" package)
        - vtk: vtu, pvtu from ALYA solver, vtk unstructured from OpenFOAM (requires "vtk" package)
"""
import sys
import numpy as np
from .generate_h5 import fill_dict_empty_nested

PYMECH_PRESENT = True
try:
    from pymech.dataset import open_dataset
except ImportError:
    PYMECH_PRESENT = False

VTK_PRESENT = True
try:
    import vtk
except ImportError:
    VTK_PRESENT = False


__all__ = ["convert_nek5000","convert_vtu","convert_vtk"]


def _add_values_to_dict_from_dataset_vtu(dict_, dataset_ = None,
                                            skip_list_ = None, add_mesh_ = True):
    """ Function adding vtk unstructured formatted field variables in a given dictionary
        containing variable names.

        Input:
            :dict_ : empty nested dictionary to fill
            :dataset_: vtk file reader output object
            :skip_list_: optional list of type string with dict_ inputs for which
                        to not add the fields
        Output:
            :None: adds fields to the input dict_
    """

    if dataset_ is None:
        print("Please specify the dataset object")
        sys.exit()
    if skip_list_ is None:
        skip_list_ = []

    # Field variables part
    pointdata = dataset_.GetPointData()
    for variter, varname in enumerate(dict_.keys()):
        if not varname in skip_list_:
            array = pointdata.GetArray(variter)
            # Check for multicomponent 1D arrays
            if array.GetNumberOfComponents() > 1:
                # structure in (X0,Y0,Z0) (X1,Y1,Z1) ...
                num_comp =  array.GetNumberOfComponents()
                num_values = array.GetNumberOfValues()
                tmp_data = np.zeros((int(num_values/num_comp),num_comp))

                for ii in range(int(num_values/num_comp)):
                    for jj in range(num_comp):
                        tmp_data[ii][jj] = array.GetValue(ii * num_comp + jj)

                comp_names = []
                for jj in range(num_comp):
                    comp_names.append('Component'+str(jj))
                fill_dict_empty_nested(dict_, nested_key_ = varname, keys_to_add_ = comp_names)

                for kk, component in enumerate(comp_names):
                    dict_[varname][component] = np.array(tmp_data[:,kk])

            else:
                tmp_data = []
                for ii in range(array.GetNumberOfValues()):
                    tmp_data.append(array.GetValue(ii))
                dict_[varname] = np.array(tmp_data )

    if add_mesh_:
        _add_mesh_values_to_dict_from_dataset_vtu(dict_, dataset_)


def _add_mesh_values_to_dict_from_dataset_vtu(dict_, dataset_ = None):
    """ Function to add mesh points info from pvtu or vtu file to the given dictionary

        Input:
            :dict_ : empty nested dictionary to fill
            :dataset_: vtk file reader output object
        Output:
            :None: adds fields to the input dict_
    """
    # Mesh points
    meshpoints = dataset_.GetPoints().GetData()
    num_comp =  meshpoints.GetNumberOfComponents()
    num_values = meshpoints.GetNumberOfValues()
    tmp_data = np.zeros((int(num_values/num_comp),num_comp))

    for ii in range(int(num_values/num_comp)):
        for jj in range(num_comp):
            tmp_data[ii][jj] = meshpoints.GetValue(ii * num_comp + jj)
    comp_names = []
    for jj in range(num_comp):
        comp_names.append('Component'+str(jj))

    dict_['Mesh'] = {}
    fill_dict_empty_nested(dict_, nested_key_ = 'Mesh', keys_to_add_ = comp_names)
    for kk, component in enumerate(comp_names):
        dict_['Mesh'][component] = np.array(tmp_data[:,kk])


def _get_vtkxml_filetype(filename_, readmax_ = 5):
    """ Function returning the filetype of a vtk xml file.

        Input:
            :filename_: input vtk xml file to check
            :readmax_: int, max number of lines of file to search for the type
        Output:
            :myline: str, file type found
            :Exception raised: in case file type not found
    """

    with open(filename_, 'r') as fin:
        for _ in range(readmax_):
            myline = fin.readline()
            if "type=" in myline:
                return myline.split("type=")[1].split(' ')[0].split('"')[1]

        raise ValueError("VTK xml File type not found, did you specify the correct file type?")


def _add_values_to_dict_from_dataset_nek5000(dict_, dataset_ = None, skip_list_ = None):
    """ Function adding nek5000 formatted field variables in a given dictionary
        containing variable names.

        Input:
            :dict_ : empty nested dictionary to fill
            :dataset_: nek5000 dataset object
            :skip_list_: optional list of type string with dict_ inputs for which
                        to not add the fields
        Output:
            :None: adds fields to the input dict_
    """

    if dataset_ is None:
        print("Please specify the dataset object")
        sys.exit()

    if skip_list_ is None:
        skip_list_ = []
    total_len = dataset_.dims['x'] * dataset_.dims['y'] * dataset_.dims['z']

    for key in list(dict_.keys()):
        if not key in skip_list_:
            dict_[key] = np.reshape(dataset_[key].data, total_len)



def convert_nek5000(file_, skip_vars_ = None):
    """ Main function controlling the conversion of a nek5000 file format
        to dictionary for hdf5 output.

        Input:
            :file_: path to nek5000 file
            :skip_vars_: optional list of type string containing fields we wish to
                not consider transferring to the hdf5 output
                (default = None)
        Output:
            :new_dict: python dictionary format structured for hdf5 write output
    """

    if PYMECH_PRESENT:

        if skip_vars_ is None:
            skip_vars_ = []

        dataset = open_dataset(file_)
        var_names = []
        for item in list(dataset.data_vars):
            if item not in skip_vars_:
                var_names.append(item)

        new_dict = dict()
        fill_dict_empty_nested(new_dict, nested_key_ = None, keys_to_add_ = var_names)
        _add_values_to_dict_from_dataset_nek5000(new_dict, dataset)

        # Add some additional info
        new_dict['Parameters'] = {}
        #print(type(dataset.dims['x']))
        new_dict['Parameters']['Dimensions'] = {'Nx':np.array([dataset.dims['x']], dtype = "int32"),
                                                'Ny':np.array([dataset.dims['y']], dtype = "int32"),
                                                'Nz':np.array([dataset.dims['z']], dtype = "int32")}
        new_dict['Parameters']['time'] = np.array([dataset.coords['time'].data], dtype = "float64")

    else:
        raise ImportError("pymech package not available, "
                            + "please install it for the nek5000 convert feature.")

    return new_dict


def convert_vtu(file_, parallel_ = False, skip_vars_ = None):
    """ Main function controlling the conversion of a vtk xml unstructured file format
        to dictionary for hdf5 output.

        NOTE:   Is currently only based on point data and not cell data.
                No connectivity info is added at the moment.

        Input:
            :file_: path to vtk unstructured file
            :skip_vars_: optional list of type string containing fields we wish to
                not consider transferring to the hdf5 output
                (default = None)
            :parallel_: boolean, specification if we are dealing with pvtu of normal vtu file

        Output:
            :new_dict: python dictionary format structured for hdf5 write output
    """

    if VTK_PRESENT:
        if skip_vars_ is None:
            skip_vars_ = []

        # Create reader object
        filetype = _get_vtkxml_filetype(file_)
        if parallel_:
            assert filetype == 'PUnstructuredGrid', "VTK file type does not coincide with user input"
            reader = vtk.vtkXMLPUnstructuredGridReader()
        else:
            assert filetype == 'UnstructuredGrid', "VTK file type does not coincide with user input"
            reader = vtk.vtkXMLUnstructuredGridReader()

        # Read vtk file
        reader.SetFileName(file_)
        reader.Update()

        # Obtain variable names
        vtkdata = reader.GetOutput()
        pointdata = vtkdata.GetPointData()
        vars_num = reader.GetNumberOfPointArrays()
        vars_name = []
        for variter in range(vars_num):
            vars_name.append(pointdata.GetArrayName(variter).split()[0])

        # Create dictionary with structure
        new_dict = dict()
        fill_dict_empty_nested(new_dict, nested_key_ = None, keys_to_add_ = vars_name)

        # Fill dictionary with data
        _add_values_to_dict_from_dataset_vtu(new_dict, vtkdata)
    else:
        raise ImportError("vtk package not available,"
                        + "please install it for the vtk convert features.")

    return new_dict


def convert_vtk(file_, skip_vars_ = None):
    """ Main function controlling the conversion of a vtk file format
        to dictionary for hdf5 output.

        NOTE:   Is currently only based on point data and not cell data.
                No connectivity info is added at the moment.
                Currently only for vtk unstructured.

        Input:
            :file_: path to vtk unstructured file
            :skip_vars_: optional list of type string containing fields we wish to
                not consider transferring to the hdf5 output
                (default = None)

        Output:
            :new_dict: python dictionary format structured for hdf5 write output
    """

    if VTK_PRESENT:
        if skip_vars_ is None:
            skip_vars_ = []

        # Select reader
        reader = vtk.vtkUnstructuredGridReader()

        # Read vtk file
        reader.SetFileName(file_)
        reader.Update()

        # Obtain variable names
        vtkdata = reader.GetOutput()
        pointdata = vtkdata.GetPointData()
        vars_num = pointdata.GetNumberOfArrays()

        vars_name = []
        for variter in range(vars_num):
            vars_name.append(pointdata.GetArrayName(variter).split()[0])

        # Create dictionary with structure
        new_dict = dict()
        fill_dict_empty_nested(new_dict, nested_key_ = None, keys_to_add_ = vars_name)

        # Fill dictionary with data
        _add_values_to_dict_from_dataset_vtu(new_dict, vtkdata)
    else:
        raise ImportError("vtk package not available,"
                        + "please install it for the vtk convert features.")

    return new_dict
