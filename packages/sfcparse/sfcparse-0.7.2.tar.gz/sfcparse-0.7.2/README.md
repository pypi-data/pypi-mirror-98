# sfcparse Module for Python
### sfcparse = Simple File Configuration Parse
### Current Version 0.7.2
___
### Introduction
This module allows you to easily import, export, and append configuration data for your python program or script
in any plain text file with any file extension. **It can be used to easily export any string data to a file as well**.

### Goal for the Project:
To provide an easy alternative to using .ini files in an attempt to make importing python data and saving any data to files for your projects simple. This also gives you the universal freedom to use any file extension or any made up file type you want.

### Importing (Python only):
Imports stored variable names and their assigned values from any text file.

Returns a class with attributes from the file keeping python's natural recognition of data types, including comment lines being ignored.

**Accepted Imported Data Types:**
str, int, float, bool, list, dict, tuple, set, nonetype, bytes

### Exporting/Appending:
It simply sends string data to a file. It may be used for any string data file output.
___

# Tutorial: Importing
#### Imports Pythonic Data Types from a Text File

**Example test file**
Python data inside a file called **settings.config**.
```ini
# Comment for Single Line Data
saved_str = 'John Doe'
saved_int = 1024
saved_float = 128.75
saved_bool = False
saved_list = [1, 2, 3]
saved_dict = {'key1': 1, 'key2': 2}
saved_tuple = (1,2,3)
saved_set = { 1, 2, 3 }


# Comment for Multiline Data Sets
saved_data_multiline_dict = {
    'key1' : 'value 1',
    'key2' : 'value 2',
    'key3' : 'value 3'
}

saved_data_multiline_tuple = (
    1,
    2,
    3
)
```
### Importing the above file into your python project and accessing the data
```python
import sfcparse

settings_file = sfcparse.importfile('settings.config')

# Access any values imported
settings_file.saved_str
settings_file.saved_list
settings_file.saved_data_multiline_dict
...
```
### That's it!
___
# Tutorial: Exporting - Single Line Values
#### Writes/Overwrites a New File

Exporting data to example file **settings.config**.

**Note** these are just examples to build your data to export.
```python
import sfcparse

export_file = sfcparse.exportfile

# Single Line Values
string_to_save = 'John Doe'
number_to_save = 64
tuple_to_save = (1,2,3)


# Final Data to Export
data_to_save = f'''
# Comment Line
string_to_save = '{string_to_save}'
number_to_save = {number_to_save}
tuple_to_save = {tuple_to_save}
'''

export_file('settings.config', data_to_save)
```
### This will be the expected output stored to the file
```ini
# Comment Line
string_to_save = 'John Doe'
number_to_save = 64
tuple_to_save = (1,2,3)
```
### That's it!
___
# Tutorial: Exporting - Multiline Values
#### Writes/Overwrites a New File

Exporting data to example file **settings.config**.

**Note** these are just examples to build your data to export.
```python
import sfcparse

export_file = sfcparse.exportfile

string_to_save = 'John Doe'
number_to_save = 64

# Multiline Values
dict_to_save = """{

    'key1' : 'value1',
    'key2' : 'value2'    
}
"""

list_to_save = """[

    1,
    2,
    3
]
"""

# Dict with Vars - NOTE: Must escape Curly Braces if using variables via f-string
dict_to_save_vars = f"""{{

    'key1' : '{string_to_save}',
    'key2' : {number_to_save}
}}
"""


# Final Data to Export
data_to_save = f'''
# Comment Line
dict_to_save = {dict_to_save}
list_to_save = {list_to_save}
dict_to_save_vars = {dict_to_save_vars}
'''

export_file('settings.config', data_to_save)
```
### This will be the expected output stored to the file
```ini
# Comment Line
dict_to_save = {

    'key1' : 'value1',
    'key2' : 'value2'    
}

list_to_save = [  

    1,
    2,
    3
]

dict_to_save_vars = {

    'key1' : 'John Doe',
    'key2' : 64
}
```
### That's it!
___
# Tutorial Appending:
#### Writes New Data to a File if it Exists

It is the same syntax as exporting, but here is an example using the same exported output from "Exporting - Single Line" **settings.config**.

**Note** these are just examples to build your data to append.

**Also** Single line appending may be more tedious than multiline, so it is recommended to build your data with multiple lines as shown!
```python
import sfcparse

append_file = sfcparse.appendfile

data_to_append = ['item1', 'item2', 'item3']
data_to_append2 = [1,2,3]

# Single Line Appending
append_file('settings.config', f"data_to_append = {data_to_append}")

# Multiline Appending
final_save_data = f"""
data_to_append = {data_to_append}
data_to_append2 = {data_to_append2}
"""

append_file('settings.config', f"data_to_append = {final_save_data}")
```
### This will be the expected output appended to the file if using the multiline append method
```ini
# Comment Line
string_to_save = 'John Doe'
number_to_save = 64
tuple_to_save = (1,2,3)
data_to_append = ['item1', 'item2', 'item3']
data_to_append2 = [1,2,3]
```
### That's it!
___
# Tutorial Video
Coming soon.
___
# Module Performance
### Importing
Imported a file 1000 times with 100 lines of data in 0.6s.

##### Lab Test Conducted:

```python
from sfcparse import importfile
import time

file_to_import = 'data.test'
num_of_tests = 1000

# Performance Test
start_time = time.time()
for i in range(num_of_tests):
    importfile(file_to_import)
end_time = time.time()

elapsed_time = (end_time - start_time)

print(elapsed_time)
```
##### System: Tested on a 4th-Gen Intel Core i7-4790 at 3.6GHz
___

# Known Limitations
**Importing**
 - Does not support importing unpacked variables and values
 - Does not support importing values with a variable stored inside
 - Does not ignore comments at the end of a value imported

# Future Upgrades
**Importing**
- Add support for importing values with variables inside
- Add support for unpacked variables and values
- Add ability to ignore comments at end of a value
- Add ability to have Sections like a .ini file
