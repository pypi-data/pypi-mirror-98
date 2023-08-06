# H5CROSS

This package provides basic utilities allowing the comparison of hdf5 type files.
This includes the computation of standard statistics on data arrays such as the mean, 
min, max, median and standard deviation. 
An interactive mode is enabled through the use of nobvisual (https://pypi.org/project/nobvisual/). 
Scatter plot comparative capability is enabled through seaborn and matplotlib. 

## Installation

Installation using Pypi:

```bash
> pip install h5cross
```

## Usage

Use the CLI for a basic terminal usage.

```bash
   ---------------    H5CROSS  --------------------

  You are now using the Command line interface of h5cross a Python3 helper
  to explore and compare hdf5 files, created at CERFACS
  (https://cerfacs.fr).

  This is a python package currently installed in your python environement.

Options:
  --help  Show this message and exit.

Commands:
  convert   Conversion to hdf5 of certain file formats.
  diff      Compare the content of two hdf5 files and view interactively...
  dump      Write the content of an hdf5 file into a YAML file.
  generate  Generates an hdf5 file from a random nested dictionary (also...
  scatter   Scatter plot comparison of two hdf5 files.
  stats     Compute statistics of arrays from hdf5 file.
  tree      Print the content of an hdf5 file in terminal.
  view      Show the content of an hdf5 file interactively with nobvisual.

```

## Possibilities

### Console file structure visualization

The command `>h5cross tree `  prints the structure of an HDF5 file in the console. 

![tree_output](https://cerfacs.fr/coop/images/h5cross/tree.png)
### Statistical information of file

The command `>h5cross stats`  computes the mean, min, max, median and standard deviation of every data set for a given HDF5 file.  It is then output into the console (can be optionally deactivated). The result can be optionally saved in a YAML format (.yml). A pretty table output is set to default and can be optionally be deactivated in which case a tree output is given. In a pretty table, the full nested path is shown but can be deactivated. 

![stats_pretty_output](https://cerfacs.fr/coop/images/h5cross/stats_pretty_full.png)

![stats_pretty_output](https://cerfacs.fr/coop/images/h5cross/stats_pretty.png)

![stats_tree_output](https://cerfacs.fr/coop/images/h5cross/stats.png)

### Save file structure

The command `>h5cross dump`  outputs the structure of an HDF5 file in a YAML format (.yml). 



### View file structure

The command `>h5cross view`  allows an interactive view of the structure of an HDF5 file. It relies on the [nobvisual]( https://pypi.org/project/nobvisual/ ) package designed for the visualisation of nested objects.  A temporary .yml file is generated to allow the interactive use.  

![view](https://cerfacs.fr/coop/images/h5cross/view.png)

### Compare file structures

The command `>h5cross diff` compares the structure of two HDF5 files. Similarily to  `>h5cross view` it relies on the [nobvisual]( https://pypi.org/project/nobvisual/ ) package.  It is optionally possible to add the statistical information of both files in this representation. 

![diff](https://cerfacs.fr/coop/images/h5cross/diff.png)

### Compare field data 

The command `>h5cross scatter` allows the scatter plot comparison of selected data fields from two HDF5 files. If the data array lengths of each file differ an histogram representation will be given instead. 
A minimum requirement is the matplotlib package. By default it uses the seaborn package if available but this setting can be optionally deactivated. The density colormap requires the scipy package, if not available a single color will be used.

![seaborn](https://cerfacs.fr/coop/images/h5cross/seaborn_same_T.png)

![plt](https://cerfacs.fr/coop/images/h5cross/plt_same_T.png)

![hist](https://cerfacs.fr/coop/images/h5cross/hist.png)



### Generating a random HDF5 file

A utility is available to generate random nested HDF5 files with random data (currently limited to two nested levels). It is intended to allow the user to quickly and easily test the above functionalities. The associated command is `>h5cross generate` . 

### Converting file types to HDF5 file

It is possible to convert certain file formats to HDF5 with `>h5cross convert` .
Currently supported: nek5000, pvtu, vtu, vtk.

## Acknowledgement

h5cross is a service created in the [EXCELLERAT Center Of Excellence](https://www.excellerat.eu/wp/) and is continued as part of the [COEC Center Of Excellence](https://coec-project.eu/). Both projects are funded by the European community.
![logo](https://www.excellerat.eu/wp-content/uploads/2020/04/excellerat_logo.png)
![logo](https://www.hpccoe.eu/wp-content/uploads/2020/10/cnmlcLiO_400x400-e1604915314500-300x187.jpg)
