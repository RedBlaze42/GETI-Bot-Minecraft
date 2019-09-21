import json
import os
from copy import copy

class json_file():

    def __init__(self,file_path="config.json",create_file=True):
        if not os.path.isfile(file_path) and create_file:
            open(file_path,"w").close()
        with open(file_path,"r") as file:
            json_data=file.read()
        self.__dict__ = json.loads(json_data)
        self._file_path=file_path
        
    def _contains(self,name):
        return hasattr(self,name)

    def __setattr__(self,name,value):
        print("saving config",name,value,name=="__dict__" , hasattr(self,"_file_path"))
        if name=="__dict__" and hasattr(self,"_file_path"):
            save_dict=copy(self.__dict__)
            for key in self.__dict__:
                if key.startwith("_"):
                    save_dict.pop(key)
            with open(self._file_path,"w") as file:
                json.dump(save_dict,file)
                
        super().__setattr__(name,value)