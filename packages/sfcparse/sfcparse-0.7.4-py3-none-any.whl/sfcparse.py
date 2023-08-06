"""
Simple File Configuration Parse - by aaronater10

Version 0.7.4

This module allows you to import, export, and append configuration data for your python program or script
in a plain text file. It can be used to export any str data to a file as well. Also conains a feature for
easily formatting data types for clean multiline output when exporting data to files.

Importing [Python only]: returns a class with attributes from the file keeping python's natural recognition
of data types, including comments being ignored.

Exporting/Appending: it simply sends str data to a file. It may be used for any str data file output.

Accepted Imported Data Types: str, int, float, bool, list, dict, tuple, set, nonetype, bytes
"""
#########################################################################################################
# Imports
from ast import literal_eval as __literal_eval__


#########################################################################################################
# MODULE STARTS HERE

# Import File Data
def importfile(filename=str):
    """
    Imports saved python data from any text file.

    Returns a class with attributes. Assign output to var.

    Enter file location as str to import.

    [Example Use]
    importfile('filename.test' or 'path\\to\\filename.test')
    """

    # Validate File Exists
    try:
        with open(filename, 'r'):
            pass        
    except FileNotFoundError as __err:
        return print(__err)

    # Open and Import Config File into Class Object then return the object
    with open(filename, 'r') as f:            
        class file_data:
            
            # Data Build Switches
            __start_data_build_sw = False
            __build_data_sw = False
            __end_data_build_sw = False

            # Markers
            __start_markers = {'[','{','('}
            __end_markers = {']','}',')'}
            __skip_markers = {'',' ','#','\n'}

            # Main File Loop
            for __import_file_data in f.readlines():
                __skip_data = __import_file_data

                # Skip Comments, Blank Lines, and New Lines
                if (__start_data_build_sw == False) and (__skip_data[0] in __skip_markers):
                    continue
                
                # Verify Basic File Syntax, then Import Lines of Data
                try:
                    __syntax_check = __import_file_data.split()[1]
                except:
                    __syntax_check = ''

                if (__syntax_check == '=') or (__start_data_build_sw == True):

                    
                    # Set Data Build Markers

                    # Read/Set START Marker from File
                    try:
                        __start_data_build_marker = __import_file_data.split()[2]
                    except:
                        __start_data_build_marker = ''

                    # Check if a Character is After the Start Marker
                    try:
                        __start_data_build_marker_post_check = __import_file_data.split()[3]
                        __start_data_build_marker_post_check = True
                    except:
                        __start_data_build_marker_post_check = False
                    
                    # Read/Set END Marker from File
                    try:
                        __end_data_build_marker = __import_file_data.strip()
                    except:
                        __end_data_build_marker = ''

                    # Set Data Build Marker Checks
                    __start_data_build_marker_check = (__start_data_build_marker in __start_markers)
                    __end_data_build_marker_check = (__end_data_build_marker in __end_markers)


                    # START DATA BUILD: Check if line of file is a Start Data Build Section
                    if (__start_data_build_marker_check == True) and (__start_data_build_marker_post_check == False):
                        __key_stream = __import_file_data.split()[0]
                        __build_data = __import_file_data.split('=')[1].strip()

                        # Turn ON Data Build Switches
                        __start_data_build_sw = True
                        __build_data_sw = True
                        __end_data_build_sw = True                        
                        continue

                    # END DATA BUILD: Check if line of file is an End Data Build Section, then Import Built Data Type if Valid
                    elif (__end_data_build_sw == True) and (__end_data_build_marker_check == True):
                        __build_data += __import_file_data.strip()
                        locals()[__key_stream] = __literal_eval__(__build_data)

                        # Turn OFF Data Build Swiches
                        __build_data_sw = False
                        __end_data_build_sw = False
                        __start_data_build_sw = False
                        continue

                    # CONT DATA BUILD: Continue to Build Data if Switch is ON    
                    elif __build_data_sw == True:
                        __build_data += __import_file_data


                    # IMPORT SINLGE LINE TYPES: Import Valid Data Types on Lines of File
                    else:
                        __key = __import_file_data.split()[0].strip()
                        __value = __import_file_data.split('=')[1].strip()                            
                        locals()[__key] = __literal_eval__(__value)                            
        
        # Return Final Import
        return file_data()


#########################################################################################################
# Export Data to File
def exportfile(filename=str, *args):
    """
    Exports a new file with the new data.
    
    Enter new filname as str, Pass any data to file as str.
    
    [Example Use]
    exportfile('filename.test' or 'path\\to\\filename.test', 'data1', 'data2')
    """

    # Export data to new file
    with open(filename, 'w') as f:
        for data_to_write in args:
            f.writelines(str(data_to_write))


#########################################################################################################
# Append Data to File
def appendfile(filename=str, *args):
    """
    Appends new data to a file.

    Enter existing filname as str, Pass any data to file as str.

    [Example Use]
    appendfile('filename.test' or 'path\\to\\filename.test', 'data1', 'data2')
    """

    # Append data to file
    try:
        with open(filename, 'r'):
            with open(filename, 'a') as f:
                for data_to_write in args:
                    f.writelines("\n" + str(data_to_write))            
    except FileNotFoundError as __err:
        print(__err)


#########################################################################################################
# Format/Prep Dictionary, List, Tuple, or Set Data for Export
def cleanformat(_datatype_):
    """
    Formats a (single) dictionary, list, tuple, or set to have a clean multiline output for exporting to a file.

    Returned output will be a str.

    Note: Will not work properly if keys or values contain commas

    Accepted data types: dict, list, tuple, set 

    [Example Use]
    var = cleanformat(_datatype_)
    """

    # Data Type Markers
    MARKERS_START = ['{','[','(']
    MARKERS_END = ['}',']',')']

    # Grab data type, Convert data type to str
    __checktype = _datatype_
    _datatype_ = str(_datatype_)

    # Create return data var and set to str
    __build_data = ""

    # Format Data Type and Return as str
    try:
        for data_to_build in _datatype_.split(','):
            # Check if data type is empty or has 1 element, if so format and break
            if not any(__checktype):
                __build_data = _datatype_[0] + '\n'*2 + _datatype_[-1]
                break
            # Tuple Fix: Tuple End Bracket Gets Cut off with single value. Other types do not.
            elif (len(__checktype) == 1) and (type(__checktype) == type(())):
                __build_data = MARKERS_START[2] + '\n ' + data_to_build[1:] + '\n' + MARKERS_END[2]
                break
            elif len(__checktype) == 1:                
                __build_data = data_to_build[0] + '\n ' + data_to_build[1:-1] + '\n' + data_to_build[-1]
                break

            # Format data type with more than 2 elements
            if data_to_build[0] in MARKERS_START:
                __build_data += data_to_build[0] + '\n ' + data_to_build[1:] + ',' + '\n'
                continue    
            if data_to_build[-1] in MARKERS_END:
                __build_data += data_to_build[:-1] + '\n' + data_to_build[-1]
            else:
                __build_data += data_to_build + ',' + '\n'
    
    except TypeError as __err:
        print('Passed in an invalid data type:', __err)

    # Return final built data as str
    return __build_data