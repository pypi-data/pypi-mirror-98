from pymech.neksuite import readnek
from pymech.dataset import open_dataset

from generate_h5 import fill_dict_empty_nested
from write_h5 import write_h5
import numpy as np
import sys
import vtk

# https://nek5000.github.io/NekDoc/problem_setup/case_files.html#restart-output-files-f

#------------------------------------------------------------------#
def fill_dict_empty_nested_from_listkeys(dict_, keys_to_add_ = None):
    """ Function calls fill_dict_empty_nested() for each key in present dictionary
    """
    if keys_to_add_ is None:
        print("Please specify dictionary entries to add")
        sys.exit()

    for item in list(dict_.keys()):
        fill_dict_empty_nested(dict_, nested_key_ = item, keys_to_add_ = keys_to_add_)


def add_values_to_dict_from_dataset(dict_, dataset_ = None, skip_list_ = None):
    """ 

        Input:
            :dict_ : empty nested dictionary to fill

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


#------------------------------------------------------------------#

flag_nek5000 = 0
if flag_nek5000:
    file_loc = "/Users/hoste/tools/coec_wp6/DATA_FORMATS/Nek5000/"
    file_name = "premix0.f00001"
    readfile = readnek(file_loc + file_name) 

    dataset = open_dataset(file_loc + file_name)

    total_len = dataset.dims['x'] * dataset.dims['y'] * dataset.dims['z']
    var_names = list(dataset.data_vars)
    new_dict = dict()
    fill_dict_empty_nested(new_dict, nested_key_ = None, keys_to_add_ = var_names)
    # Variables are listed in (z,y,x) order
    new_temp = np.reshape(dataset['temperature'].data, total_len)

    add_values_to_dict_from_dataset(new_dict, dataset)

#    write_h5(new_dict, save_name_ = 'dump', save_path_='./')


flag_vtk = 1
if flag_vtk:
    # file_loc = "/Users/hoste/JJ_TAU/Cheng_1_1stO_coarse/BK_reac_2ndO_profEilmer_Gerlinger_ctu_2/vtk/"
    # file_name = "solution.pval.922847_hexa.vtu"

    '''
        Useful paper perhaps: Simple visualizations of unstructured grids with VTK
    '''

    # Individual vtu test
    flag_test1 = 0
    if flag_test1:
        file_loc = "/Users/hoste/tools/coec_wp6/DATA_FORMATS/ALYA/ALYA_OUTPUT/VTK_FORMAT/non_prem_box_VarVar_vectorized_00000000/"
        file_name = "non_prem_box_VarVar_vectorized_00000000_0.vtu"
        ''' File info: VTKFile type="UnstructuredGrid" 
                                version="0.1" 
                                byte_order="LittleEndian" 
                                header_type="UInt32" 
                                compressor="vtkZLibDataCompressor">
        '''
        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(file_loc + file_name)
        reader.Update()

        print("Nb of cells = ", reader.GetNumberOfCells())
        reader.GetNumberOfPoints()

        vars_num = reader.GetNumberOfPointArrays() 
        vtkdata = reader.GetOutput() # this is the actual reading output

        # So either one of both if not mistaken, what if vectors? Need to see different possibilities
        pointData = vtkdata.GetPointData()
        vectorData = pointData.GetVectors()

        # Could be pretty interesting
        # https://blog.kitware.com/hdf5-reader-and-writer-for-unstructured-grids/

        new_dict = dict()
        vars_name = []
        for variter in range(vars_num):
            vars_name.append(pointData.GetArrayName(variter).split()[0])

        fill_dict_empty_nested(new_dict, nested_key_ = None, keys_to_add_ = vars_name)

    #    arr.GetNumberOfValues()
        for variter, varname in enumerate(vars_name):
            array = pointData.GetArray(variter)
            tmp_data = []
            for ii in range(array.GetNumberOfValues()):
                tmp_data.append(array.GetValue(ii))
            new_dict[varname] = np.array(tmp_data )

        #write_h5(new_dict, save_name_ = 'vtkdump', save_path_='./')
        #GetNumberOfValues() 

    # with open(file_loc+file_name, 'r') as fin:
    #     readmax = 5
    #     for line in range(readmax):
    #         if "type=" in fin.readline():
    #             print("mytype")

    #NOTE!!
    # SO WOULD BE ADDING A COMPONENT!
    #<PDataArray type="Float64" Name="VELOC" NumberOfComponents="3"/>
    # ALSO I THINK POINT info is also there, for mesh in float32 type

   # Individual pvtu test
    flag_test2 = 0
    if flag_test2:
        ''' Possibly https://github.com/JiaweiZhuang/vtk_experiments/blob/master/vtki_correct_pvtu.ipynb
            https://github.com/mmagnuski/vtki/tree/master/vtki
            But adds even another depedency, would avoid that

            (maybe but less interesting https://github.com/pearu/pyvtk)

        Header:
            <VTKFile type="PUnstructuredGrid"
                            version="0.1" 
                            byte_order="LittleEndian"
                            header_type="UInt32"
                            compressor="vtkZLibDataCompressor">
            <PUnstructuredGrid GhostLevel="0">
            <PPointData>
            <PDataArray type="Float64" Name="CON01"/>
            <PDataArray type="Float64" Name="CON02"/>
        '''

        file_loc = "/Users/hoste/tools/coec_wp6/DATA_FORMATS/ALYA/ALYA_OUTPUT/VTK_FORMAT/"
        file_name = "non_prem_box_VarVar_vectorized_00000000.pvtu"

        # MAYBE THE GHOSTCELL PART GOT AUTOMATICALLY DEALT WITH By THE READER- > would make sense

        # Use XMLP
        reader = vtk.vtkXMLPUnstructuredGridReader()
        reader.SetFileName(file_loc + file_name)
        reader.Update()

        print("Nb of pieces (individual vtu files) = ", reader.GetNumberOfPieces())
        # Reader seems to join all individuals alreadye AND probable 

        vars_num = reader.GetNumberOfPointArrays() 
        vtkdata = reader.GetOutput()
        pointData = vtkdata.GetPointData()

        new_dict = dict()
        vars_name = []
        for variter in range(vars_num):
            vars_name.append(pointData.GetArrayName(variter).split()[0])

        fill_dict_empty_nested(new_dict, nested_key_ = None, keys_to_add_ = vars_name)

        for variter, varname in enumerate(vars_name):
            array = pointData.GetArray(variter)
            if array.GetNumberOfComponents() > 1:
                print("Nb of components = ", array.GetNumberOfComponents())
                print("Size of array = ", array.GetSize())
                #TODO: NEED TO KNOW IF ALL X, Y, Z comp or (X0,Y0,Z0) (X1,Y1,Z1) ...
                # opening in paraview appears to be the second
                tmp_data = np.zeros((int(array.GetNumberOfValues()/array.GetNumberOfComponents()),
                                     array.GetNumberOfComponents()))
                
                for ii in range(int(array.GetNumberOfValues()/array.GetNumberOfComponents())):
                    for jj in range(array.GetNumberOfComponents()):
                        tmp_data[ii][jj] = array.GetValue(ii * array.GetNumberOfComponents() + jj)

                comp_names = []
                for jj in range(array.GetNumberOfComponents()):
                    comp_names.append('Component'+str(jj))
                fill_dict_empty_nested(new_dict, nested_key_ = varname, keys_to_add_ = comp_names)
                
                for kk, component in enumerate(comp_names):
                    new_dict[varname][component] = np.array(tmp_data[:,kk])

            else:
                tmp_data = []
                for ii in range(array.GetNumberOfValues()):
                    tmp_data.append(array.GetValue(ii))
                new_dict[varname] = np.array(tmp_data )

        #STILL NEED TO ADD POINTS!!
        meshPoints = vtkdata.GetPoints().GetData()
       

        num_comp =  meshPoints.GetNumberOfComponents()
        num_values = meshPoints.GetNumberOfValues()
        tmp_data = np.zeros((int(num_values/num_comp),num_comp))
              
        for ii in range(int(num_values/num_comp)):
            for jj in range(num_comp):
                tmp_data[ii][jj] = meshPoints.GetValue(ii * num_comp + jj)
        comp_names = []
        for jj in range(num_comp):
            comp_names.append('Component'+str(jj))

        new_dict['Mesh'] = {}
        fill_dict_empty_nested(new_dict, nested_key_ = 'Mesh', keys_to_add_ = comp_names)
        for kk, component in enumerate(comp_names):
            new_dict['Mesh'][component] = np.array(tmp_data[:,kk])
        write_h5(new_dict, save_name_ = 'vtkparallel', save_path_='./')


    flag_test3 = 1
    if flag_test3:
        file_loc = "/Users/hoste/tools/coec_wp6/DATA_FORMATS/OpenFoam/VTK/"
        file_name = "001_fireII_NR_s_46115.vtk"
        '''
            Possible interest:
            https://discourse.vtk.org/t/python-reading-calculate-write-out/1138/4
            vtk pyvista possible interest

            meshio https://github.com/nschloe/meshio
        '''

        #reader = vtk.vtkDataSetReader()
        reader = vtk.vtkUnstructuredGridReader()
        # #reader = vtk.vtkStructuredPointsReader()
        
        reader.SetFileName(file_loc + file_name)
        # reader.ReadAllVectorsOn()
        # reader.ReadAllScalarsOn() #--> so probably needed to get the vars
        reader.Update()
        vtkdata = reader.GetOutput()
        
        pointData = vtkdata.GetPointData()
        vars_num = pointData.GetNumberOfArrays()

        new_dict = dict()
        vars_name = []
        for variter in range(vars_num):
            vars_name.append(pointData.GetArrayName(variter).split()[0])

        fill_dict_empty_nested(new_dict, nested_key_ = None, keys_to_add_ = vars_name)


        for variter, varname in enumerate(vars_name):
            array = pointData.GetArray(variter)
            if array.GetNumberOfComponents() > 1:
                print("Nb of components = ", array.GetNumberOfComponents())
                print("Size of array = ", array.GetSize())
                #TODO: NEED TO KNOW IF ALL X, Y, Z comp or (X0,Y0,Z0) (X1,Y1,Z1) ...
                # opening in paraview appears to be the second
                tmp_data = np.zeros((int(array.GetNumberOfValues()/array.GetNumberOfComponents()),
                                     array.GetNumberOfComponents()))
                
                for ii in range(int(array.GetNumberOfValues()/array.GetNumberOfComponents())):
                    for jj in range(array.GetNumberOfComponents()):
                        tmp_data[ii][jj] = array.GetValue(ii * array.GetNumberOfComponents() + jj)

                comp_names = []
                for jj in range(array.GetNumberOfComponents()):
                    comp_names.append('Component'+str(jj))
                fill_dict_empty_nested(new_dict, nested_key_ = varname, keys_to_add_ = comp_names)
                
                for kk, component in enumerate(comp_names):
                    new_dict[varname][component] = np.array(tmp_data[:,kk])

            else:
                tmp_data = []
                for ii in range(array.GetNumberOfValues()):
                    tmp_data.append(array.GetValue(ii))
                new_dict[varname] = np.array(tmp_data )



        #STILL NEED TO ADD POINTS!!
        meshPoints = vtkdata.GetPoints().GetData()
       

        num_comp =  meshPoints.GetNumberOfComponents()
        num_values = meshPoints.GetNumberOfValues()
        tmp_data = np.zeros((int(num_values/num_comp),num_comp))
              
        for ii in range(int(num_values/num_comp)):
            for jj in range(num_comp):
                tmp_data[ii][jj] = meshPoints.GetValue(ii * num_comp + jj)
        comp_names = []
        for jj in range(num_comp):
            comp_names.append('Component'+str(jj))

        new_dict['Mesh'] = {}
        fill_dict_empty_nested(new_dict, nested_key_ = 'Mesh', keys_to_add_ = comp_names)
        for kk, component in enumerate(comp_names):
            new_dict['Mesh'][component] = np.array(tmp_data[:,kk])
        write_h5(new_dict, save_name_ = 'vtkparallel', save_path_='./')
        