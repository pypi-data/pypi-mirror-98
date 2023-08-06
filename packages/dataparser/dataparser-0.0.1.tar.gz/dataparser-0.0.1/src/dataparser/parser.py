import os
import logging
import json

#TODO Set logger    

#Path verification
'''def gen_path(file_name):
    if file_name == '':
        raise EnvironmentError("No path were specified")
    else:
        file_name = "text"
        strip = file_name.split("/")
        directory = file_name.replace(strip[-1], "")
        if not os._exists(file_name):
            os.mkdir(directory)'''

def write_file(file_name: str, data: dict):
    #gen_path(file_name)
    #Get dict
    if not type(data) == dict:
        raise TypeError("Argument: \"data\" must be dictionary type.\nwrite_file(\"file_name\", \"overwrite\" = True, \"data\" = { }")
    elif data.__len__ == 0:
        raise ValueError("\"data\" must not be empty, for erasing data use clear() instead")
    else:
        if os._exists(file_name):
            os.remove(file_name)
        jstream = open(file_name, "w+")
        json.dump(data, jstream)

        jstream.close()

def read_file(file_name: str):
    jstream = open(file_name, "r")
    dt = jstream.read()
    jstream.close()
    
    data = json.loads(dt)

    return data

#file_name = Name of the file, data = tuple to filter, returns a tuple
def get_data(file_name: str, data: tuple):
    DATA = read_file(file_name)
    if data.count == 0:
        return tuple(DATA.values())
    else:
        lData = list()
        for x in data:
            lData.append(DATA[x])
        return tuple(lData)

def update_file(file_name: str, data: dict):
    if file_name == "":
        raise ValueError("\"file_name\" must not be empty")
    elif data.__len__() == 0:
        raise ValueError("\"data\" must contain data to update")
    else:
        DATA = read_file(file_name)
        keys = tuple(data.keys())
        for x in keys:
            DATA[x] = data[x]
        write_file(file_name, DATA)