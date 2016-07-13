#Freme Dataset Tool

A simple tool for interacting with Freme's dataset API. Add information that is
specific to your implementation in the `docs/config.py` file, then use the
freme_datasets.py script to interact with the API.

##Setup

Configure the script for your instance of Freme using the following options:

**freme_url:** The remote location of the Freme instance you want to use. Must
specify the full path and port of the API

**chunk_size:** For large numbers of entities, Freme requires that a dataset be
uploaded in chunks. This variable defines how many entity labels should be
uploaded at a time

**auth_token:** Certain operations such as creating, deleting or updating a
dataset require an API key. You can request this key from the Freme API after
you register an account. They key may then be entered here to enable restricted
behaviours

##Usage

The script defines a number of behaviours which you may perform on Freme. These
are listed below.

###Examine All Datasets

Returns a list of all datasets currently stored by Freme. To do this, run the
script with no arguments

`./freme_datasets.py`

###Examine a Specific Dataset

Returns information about a specific dataset stored by Freme. Run the script
with the -n flag

`./freme_datasets.py -n dataset_name`

###Create a new Dataset

Creates a new instance of a dataset in Freme using the -c flag. Optionally you
can specify a description of the dataset using -D

`./freme_datasets.py -n dataset_name -D optional_dataset_description -c`

###Load data into a Dataset

Loads an existing dataset with information contained in a file using the -l
flag. Note that the list of files does not need to immediately follow the -l
flag. Multiple files may be passed to the script

`./freme_datasets.py -l -n dataset_name file_name [filename ...]`

You can chain the create and load flags so that a dataset may be created and
loaded in a single call to the script. Again, you can optionally specify a
description using -D if you want, but it's not required

`./freme_datasets.py -c -l -n dataset_name file_name [filename ...]`

###Delete a Dataset

You can delete a dataset from freme using the -d flag. This will require that
you enter the dataset name a second time to confirm that you actually want to
delete the target dataset

`./freme_datasets.py -D -n dataset_name`
